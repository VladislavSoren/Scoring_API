#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import abc
# import datetime
# import hashlib
import json
import logging
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

# from io import BytesIO
from optparse import OptionParser

from fields import (
    ArgumentsField,
    BirthDayField,
    CharField,
    ClientIDsField,
    DateField,
    EmailField,
    GenderField,
    PhoneField,
)

SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"
OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
INVALID_REQUEST = 422
INTERNAL_ERROR = 500
ERRORS = {
    BAD_REQUEST: "Bad Request",
    FORBIDDEN: "Forbidden",
    NOT_FOUND: "Not Found",
    INVALID_REQUEST: "Invalid Request",
    INTERNAL_ERROR: "Internal Server Error",
}
UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}


class ClientsInterestsRequest:
    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class OnlineScoreRequest:
    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)


# Структура запроса
class MethodRequest:
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


# def check_auth(request):
#     if request.is_admin:
#         digest = hashlib.sha512(datetime.datetime.now().strftime("%Y%m%d%H") + ADMIN_SALT).hexdigest()
#     else:
#         digest = hashlib.sha512(request.account + request.login + SALT).hexdigest()
#     if digest == request.token:
#         return True
#     return False


# Метод определения способа обработки запроса: OnlineScoreRequest/ClientsInterestsRequest
def score_handler(request, ctx, store):
    response, code = None, None

    response = {"response": "score_handler"}
    code = 200

    return response, code


def interests_handler(request, ctx, store):
    response, code = None, None

    response = {"response": "interests_handler"}
    code = 200

    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):
    router = {
        "score": score_handler,
        "interests": interests_handler,
    }
    store = None

    # ping server
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, world!")

    def get_request_id(self, headers):
        return headers.get("HTTP_X_REQUEST_ID", uuid.uuid4().hex)

    def do_POST(self):
        # Объявления дефолтных значений
        response, code = {}, OK
        request_body = None

        # Получение контекста
        context = {"request_id": self.get_request_id(self.headers)}

        # Получаем длину контента в символах и тело запроса в виде строки
        content_length = int(self.headers["Content-Length"])
        data_string = self.rfile.read(content_length)

        # Получение тела запроса
        try:
            request_body = json.loads(data_string)
        except Exception as e:
            code = BAD_REQUEST
            self.wfile.write(b"BAD_REQUEST")
            logging.info("%s: %s %s" % (self.path, e, context["request_id"]))

        if request_body:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, request_body, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request_body, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception(f"Unexpected error: {e}")
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        # отправка заголовков (метаинформации об ответе)
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Формирование тела ответа
        # Сериализация
        json_str_out = json.dumps(response)
        json_bytes_out = json_str_out.encode()

        # Отправка ответа
        self.wfile.write(json_bytes_out)

    # def do_POST(self):
    #     response, code = {}, OK
    #     context = {"request_id": self.get_request_id(self.headers)}
    #     request = None
    #     try:
    #         data_string = self.rfile.read(int(self.headers['Content-Length']))
    #         request = json.loads(data_string)
    #     except:
    #         code = BAD_REQUEST
    #
    #     if request:
    #         path = self.path.strip("/")
    #         logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
    #         if path in self.router:
    #             try:
    #                 response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
    #             except Exception as e:
    #                 logging.exception(f"Unexpected error: {e}")
    #                 code = INTERNAL_ERROR
    #         else:
    #             code = NOT_FOUND
    #
    #     self.send_response(code)
    #     self.send_header("Content-Type", "application/json")
    #     self.end_headers()
    #     if code not in ERRORS:
    #         r = {"response": response, "code": code}
    #     else:
    #         r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
    #     context.update(r)
    #     logging.info(context)
    #     self.wfile.write(json.dumps(r))
    #     return


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

    pass
