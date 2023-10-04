import json
import unittest
from test import cases

from config import StatusCodes, accounts, store_params_ok  # store_params_fail,
from db.store import Store
from handlers import interests_handler, score_handler


class TestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # get store
        cls.store = Store(store_params=store_params_ok)

        # set valid admin
        admin_data = json.dumps(accounts["admin"])
        cls.store.set("admin", admin_data)

        # set valid user
        pass

    def setUp(self):
        self.context = {}
        self.headers = {}
        self.settings = {}

    def test_empty_request_score(
        self,
    ):
        _, code = score_handler(request={}, ctx={}, store=None)
        self.assertEqual(StatusCodes.INVALID_REQUEST, code)

    def test_empty_request_interests(
        self,
    ):
        _, code = interests_handler(request={}, ctx={}, store=None)
        self.assertEqual(StatusCodes.INVALID_REQUEST, code)

    @cases(
        [
            {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
            {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd", "arguments": {}},
            {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
        ]
    )
    def test_bad_auth_score(self, request):
        _, code = score_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )
        self.assertEqual(StatusCodes.FORBIDDEN, code)

    @cases(
        [
            {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "", "arguments": {}},
            {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "token": "sdd", "arguments": {}},
            {"account": "horns&hoofs", "login": "admin", "method": "online_score", "token": "", "arguments": {}},
        ]
    )
    def test_bad_auth_interests(self, request):
        _, code = interests_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )
        self.assertEqual(StatusCodes.FORBIDDEN, code)

    @cases(
        [
            # {},
            {"phone": "791750020401"},
            {"phone": "89175002040", "email": "stupnikov@otus.ru"},
            {"phone": "79175002040", "email": "stupnikovotus.ru"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": -1},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": "1"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.1890"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "XXX"},
            {"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1},
            {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru",
                "gender": 1,
                "birthday": "01.01.2000",
                "first_name": "s",
                "last_name": 2,
            },
            {"email": "stupnikov@otus.ru", "gender": 1, "last_name": 2},
        ]
    )
    def test_invalid_score_request(self, arguments):
        request = {
            "account": accounts["user"]["account"],
            "login": accounts["user"]["login"],
            "token": accounts["user"]["token"],
            "method": "online_score",
            "arguments": arguments,
        }
        response, code = score_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )
        self.assertEqual(StatusCodes.INVALID_REQUEST, code)

    @cases(
        [
            {},
            {"date": "20.07.2017"},
            {"client_ids": [], "date": "20.07.2017"},
            {"client_ids": {1: 2}, "date": "20.07.2017"},
            {"client_ids": ["1", "2"], "date": "20.07.2017"},
            {"client_ids": [1, 2], "date": "XXX"},
        ]
    )
    def test_invalid_interests_request(self, arguments):
        request = {
            "account": accounts["user"]["account"],
            "login": accounts["user"]["login"],
            "token": accounts["user"]["token"],
            "method": "online_score",
            "arguments": arguments,
        }
        response, code = interests_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )
        self.assertEqual(StatusCodes.INVALID_REQUEST, code)

    @cases(
        [
            {"phone": "79175002040", "email": "stupnikov@otus.ru"},
            {"gender": 1, "birthday": "01.01.2000", "first_name": "a", "last_name": "b"},
            {"gender": 0, "birthday": "01.01.2000"},
            {"gender": 2, "birthday": "01.01.2000"},
            {"first_name": "a", "last_name": "b"},
            {
                "phone": "79175002040",
                "email": "stupnikov@otus.ru",
                "gender": 1,
                "birthday": "01.01.2000",
                "first_name": "a",
                "last_name": "b",
            },
        ]
    )
    def test_ok_score_request(self, arguments):
        request = {
            "account": accounts["user"]["account"],
            "login": accounts["user"]["login"],
            "token": accounts["user"]["token"],
            "method": "online_score",
            "arguments": arguments,
        }
        response, code = score_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )

        self.assertEqual(StatusCodes.OK, code)
        score = response.get("score")
        self.assertTrue(isinstance(score, (int, float)) and score >= 0, arguments)

    @cases(
        [
            {"client_ids": [1, 2], "date": "19.07.2017"},
            {"client_ids": [0]},
        ]
    )
    def test_ok_interests_request(self, arguments):
        request = {
            "account": accounts["user"]["account"],
            "login": accounts["user"]["login"],
            "token": accounts["user"]["token"],
            "method": "online_score",
            "arguments": arguments,
        }
        response, code = interests_handler(
            request={"body": request, "headers": self.headers},
            ctx=self.context,
            store=None,
        )

        self.assertEqual(StatusCodes.OK, code)
        self.assertEqual(len(arguments["client_ids"]), len(response))
        self.assertTrue(
            all(v and isinstance(v, list) and all(isinstance(i, (bytes, str)) for i in v) for v in response.values())
        )
        self.assertEqual(self.context.get("nclients"), len(arguments["client_ids"]))

    # def test_ok_score_admin_request(self):
    #     arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
    #     request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": arguments}
    #     self.set_valid_auth(request)
    #     response, code = self.get_response(request)
    #     self.assertEqual(api.OK, code)
    #     score = response.get("score")
    #     self.assertEqual(score, 42)
    #
    #


if __name__ == "__main__":
    unittest.main()
