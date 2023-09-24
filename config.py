SALT = "Otus"
ADMIN_LOGIN = "admin"
ADMIN_SALT = "42"


class StatusCodes:
    OK = 200
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    INVALID_REQUEST = 422
    INTERNAL_ERROR = 500


class ClientStatus:
    admin = "admin"
    user = "user"
    forbidden = StatusCodes.FORBIDDEN


ERRORS = {
    StatusCodes.BAD_REQUEST: "Bad Request",
    StatusCodes.FORBIDDEN: "Forbidden",
    StatusCodes.NOT_FOUND: "Not Found",
    StatusCodes.INVALID_REQUEST: "Invalid Request",
    StatusCodes.INTERNAL_ERROR: "Internal Server Error",
}

UNKNOWN = 0
MALE = 1
FEMALE = 2
GENDERS = {
    UNKNOWN: "unknown",
    MALE: "male",
    FEMALE: "female",
}

accounts = [
    {
        "account": "admin",
        "login": "admin",
        # token обновляется каждый час
        "token": "8003417a60c6fc434d2acab0a0584bca8d1f34a42285e878febd6810ba4d563163cb14cb7ff23bfe995387c245ea1ebd34b34284fb65315fde3851c9873fa15e",
    },
    {
        "account": "user",
        "login": "user",
        "token": "aa34e991ff440298f58c8021c8ce0d337fdc01e75488f6fbae94a16e7c8c2ed49514e8da4df2ec398bcdd67ca5bd9a3600d2b09c698a27c6e0a2dad8eee9a634",
    },
    {
        "account": "user",
        "login": "",
        "token": "9dc1a0d136748c1becca284bab940a63a21bf55d37667b2afe9949cda228c6b25ec64a1c3fe2ea134b6f4cdfe7dc79deed8a7d1e2454cc483077d9b85b872f93",
    },
]
