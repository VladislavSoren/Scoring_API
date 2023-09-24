#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import abc
import datetime
import hashlib
import json
import logging
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

# from io import BytesIO
from optparse import OptionParser

from config import ADMIN_SALT, ERRORS, SALT, ClientStatus, StatusCodes
from scoring import get_interests, get_score
from validators import (
    ClientsInterestsRequest,
    OnlineScoreRequest,
    get_request_validator,
)


def check_auth(request):
    if request.is_admin:
        info_for_hash_bytes = (datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).encode("utf-8")
        digest = hashlib.sha512(info_for_hash_bytes).hexdigest()
        if digest == request.token:
            return ClientStatus.admin
    else:
        info_for_hash_bytes = (request.account + request.login + SALT).encode("utf-8")
        digest = hashlib.sha512(info_for_hash_bytes).hexdigest()
        if digest == request.token:
            return ClientStatus.user

    return ClientStatus.forbidden


# Метод обработки score запроса
def score_handler(request, ctx, store):
    request_body = request["body"]
    response = {}

    request_validator = get_request_validator(request_body)
    status = check_auth(request_validator)

    if status == ClientStatus.admin:
        response = 42
        code = StatusCodes.OK

    elif status == ClientStatus.user:
        request_validator = get_request_validator(request_body)
        arguments = request_validator.arguments

        args_validator = OnlineScoreRequest()
        args_validator.first_name = arguments.get("first_name")
        args_validator.last_name = arguments.get("last_name")
        args_validator.email = arguments.get("email")
        args_validator.phone = arguments.get("phone")
        args_validator.birthday = arguments.get("birthday")
        args_validator.gender = arguments.get("gender")

        score = get_score(
            store,
            phone=args_validator.phone,
            email=args_validator.email,
            birthday=args_validator.birthday,
            gender=args_validator.gender,
            first_name=args_validator.first_name,
            last_name=args_validator.last_name,
        )

        response = {"score": score}
        code = StatusCodes.OK

    else:
        code = StatusCodes.FORBIDDEN

    # Заполняем контекст
    has_fields = []
    fields_vals_dict = vars(request_validator)
    for field, val in fields_vals_dict.items():
        if val != "":
            has_fields.append(field)
    ctx["has"] = has_fields

    return response, code


# Метод обработки interests запроса
def interests_handler(request, ctx, store):
    request_body = request["body"]
    response = {}

    request_validator = get_request_validator(request_body)
    status = check_auth(request_validator)

    if status == ClientStatus.admin or status == ClientStatus.user:
        arguments = request_validator.arguments

        args_validator = ClientsInterestsRequest()
        args_validator.client_ids = arguments.get("client_ids")
        args_validator.date = arguments.get("date")

        interests_dict = {}
        for cid in args_validator.client_ids:
            interests = get_interests(store, cid=cid)
            interests_dict[cid] = interests

        response = interests_dict
        code = StatusCodes.OK

    else:
        code = StatusCodes.FORBIDDEN

    # Заполняем контекст
    ctx["nclients"] = len(request_validator.arguments["client_ids"])

    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "score": score_handler,
        "interests": interests_handler,
    }
    store = None

    # ping server
    def do_GET(self):
        self.send_response(StatusCodes.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def get_request_id(self, headers):
        return headers.get("HTTP_X_REQUEST_ID", uuid.uuid4().hex)

    def do_POST(self):
        # Объявления дефолтных значений
        response_body, code = {}, StatusCodes.OK
        request = None
        error_text = "Unknown"

        # Получение контекста
        context = {"request_id": self.get_request_id(self.headers)}

        # Получаем длину контента в символах и тело запроса в виде строки
        content_length = int(self.headers["Content-Length"])
        data_string = self.rfile.read(content_length)

        # Десериализация (получение тела запроса в python объект)
        try:
            request = json.loads(data_string)
        except Exception as e:
            code = StatusCodes.BAD_REQUEST
            self.wfile.write(b"BAD_REQUEST")
            logging.info("%s: %s %s" % (self.path, e, context["request_id"]))

        # Получение ответа на запрос
        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, request, context["request_id"]))
            if path in self.router:
                try:
                    response_body, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception(f"Error: {e}")
                    error_text = e
                    code = StatusCodes.INTERNAL_ERROR
            else:
                code = StatusCodes.NOT_FOUND

        # отправка заголовков (метаинформации об ответе)
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # проверка на ошибки
        if code not in ERRORS:
            response = {"response": response_body, "code": code}
        else:
            error_message = response_body or ERRORS.get(code, "Unknown Error")
            if code == StatusCodes.INTERNAL_ERROR:
                error_message = f"{error_message}: {error_text}"

            response = {"error": error_message, "code": code}

        # логируем контекст
        context.update(response)
        logging.info(context)

        # Сериализация
        json_str_out = json.dumps(response)
        json_bytes_out = json_str_out.encode("utf-8")

        # Отправка ответа
        self.wfile.write(json_bytes_out)


def pars_comline_args():
    op = OptionParser()
    op.add_option("-p", "--port", action="store", type=int, default=8080)
    op.add_option("-l", "--log", action="store", default="logs.log")
    opts, args = op.parse_args()
    return opts, args


def run_server():
    server = HTTPServer(("localhost", opts.port), MainHTTPHandler)
    logging.info("Starting server at %s" % opts.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == "__main__":
    # парсим аргументы из командной строки
    opts, args = pars_comline_args()

    # настройка логирования
    logging.basicConfig(
        filename=opts.log, level=logging.INFO, format="[%(asctime)s] %(levelname).1s %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
    )

    # Запускаем сервер
    run_server()
