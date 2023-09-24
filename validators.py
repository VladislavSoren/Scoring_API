from config import ADMIN_LOGIN
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


class ClientsInterestsRequest:
    client_ids = ClientIDsField("client_ids", required=True)
    date = DateField("date", required=False, nullable=True)


class OnlineScoreRequest:
    first_name = CharField("first_name", required=False, nullable=True)
    last_name = CharField("last_name", required=False, nullable=True)
    email = EmailField("email", required=False, nullable=True)
    phone = PhoneField("phone", required=False, nullable=True)
    birthday = BirthDayField("birthday", required=False, nullable=True)
    gender = GenderField("gender", required=False, nullable=True)


# Структура запроса
class MethodRequest:
    account = CharField("account", required=False, nullable=True)
    login = CharField("login", required=True, nullable=True)
    token = CharField("token", required=True, nullable=True)
    arguments = ArgumentsField("arguments", required=True, nullable=True)
    method = CharField("method", required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN


def get_request_validator(request_body):
    request_validator = MethodRequest()
    request_validator.account = request_body.get("account")
    request_validator.login = request_body.get("login")
    request_validator.token = request_body.get("token")
    request_validator.arguments = request_body.get("arguments")
    request_validator.method = request_body.get("method")
    return request_validator
