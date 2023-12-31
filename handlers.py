from redis.exceptions import ConnectionError

from config import ClientStatus, StatusCodes
from fields.custom_errors import NoneError, NullError, ValidationError
from scoring import get_interests, get_score
from validators import (
    ClientsInterestsRequest,
    OnlineScoreRequest,
    check_auth,
    get_request_validator,
)


# Метод обработки score запроса
def score_handler(request, ctx, store):
    if not request:
        return {}, StatusCodes.INVALID_REQUEST

    request_body = request["body"]
    response = {}

    request_validator = get_request_validator(request_body)
    status = check_auth(request_validator)

    if status == ClientStatus.admin:
        response = {"score": 42}
        code = StatusCodes.OK

    elif status == ClientStatus.user:
        request_validator = get_request_validator(request_body)
        arguments = request_validator.arguments

        args_validator = OnlineScoreRequest()
        try:
            args_validator.first_name = arguments.get("first_name")
            args_validator.last_name = arguments.get("last_name")
            args_validator.email = arguments.get("email")
            args_validator.phone = arguments.get("phone")
            args_validator.birthday = arguments.get("birthday")
            args_validator.gender = arguments.get("gender")
        except (NoneError, NullError, ValidationError, TypeError, ValueError):
            return response, StatusCodes.INVALID_REQUEST

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
        return response, code

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
    if not request:
        return {}, StatusCodes.INVALID_REQUEST

    request_body = request["body"]
    response = {}

    request_validator = get_request_validator(request_body)
    status = check_auth(request_validator)

    if status == ClientStatus.admin or status == ClientStatus.user:
        arguments = request_validator.arguments

        args_validator = ClientsInterestsRequest()
        try:
            args_validator.client_ids = arguments.get("client_ids")
            args_validator.date = arguments.get("date")
        except (NoneError, NullError, ValidationError, TypeError, ValueError):
            return response, StatusCodes.INVALID_REQUEST

        interests_dict = {}
        for cid in args_validator.client_ids:
            try:
                interests = get_interests(store, cid=cid)
            except ConnectionError:
                return {}, StatusCodes.INTERNAL_ERROR
            else:
                interests_dict[cid] = interests

        response = interests_dict
        code = StatusCodes.OK

    else:
        code = StatusCodes.FORBIDDEN
        return response, code

    # Заполняем контекст
    ctx["nclients"] = len(request_validator.arguments["client_ids"])

    return response, code
