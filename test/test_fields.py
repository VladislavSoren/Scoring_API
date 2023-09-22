import unittest
from test.support_functions import cases

from fields import CharField, ClientIDsField, DateField, EmailField


class TestCharField(unittest.TestCase):
    @cases(
        [
            (123, "must be a str"),
            (None, "string is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            date = CharField(required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            (123, "must be a str"),
            ("", "string is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            date = CharField(required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            ("123", "123"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            date = CharField(required=True, nullable=True)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)

    @cases(
        [
            ("123", "123"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            date = CharField(required=False, nullable=False)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)


class TestEmailField(unittest.TestCase):
    @cases(
        [
            (123, "must be a str"),
            ("postmail.com", "no @"),
            (None, "string is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            date = EmailField(required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            (123, "must be a str"),
            ("postmail.com", "no @"),
            ("", "string is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            date = EmailField(required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            ("post@mail.com", "post@mail.com"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            date = EmailField(required=True, nullable=True)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)

    @cases(
        [
            ("post@mail.com", "post@mail.com"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            date = EmailField(required=False, nullable=False)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)


class TestDateField(unittest.TestCase):
    @cases(
        [
            ("10.11.201", "invalid format"),
            ("2019.10.11", "invalid format"),
            (123, "must be a str"),
            (None, "string is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            date = DateField(required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [("10.11.201", "invalid format"), ("2019.10.11", "invalid format"), (123, "must be a str"), ("", "string is empty")]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            date = DateField(required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            ("10.11.2023", "2023-11-10"),
            ("1.5.2023", "2023-05-01"),
            ("01.05.2023", "2023-05-01"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            date = DateField(required=True, nullable=True)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)

    @cases(
        [
            ("10.11.2023", "2023-11-10"),
            ("1.5.2023", "2023-05-01"),
            ("01.05.2023", "2023-05-01"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            date = DateField(required=False, nullable=False)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)


class TestClientIDsField(unittest.TestCase):
    @cases(
        [
            ([], "array is empty"),
            (None, "array is empty"),
            ((1, 2), "array must be a list"),
            ([1, 1.1], "value in array must be an int"),
        ]
    )
    def test_req_true_fail(self, sample, exception_text):
        class Owner:
            date = ClientIDsField(required=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            (None, "array must be a list"),
            ((1, 2), "array must be a list"),
            ([1, 1.1], "value in array must be an int"),
        ]
    )
    def test_req_false_fail(self, sample, exception_text):
        class Owner:
            date = ClientIDsField(required=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.date = sample

    @cases(
        [
            ([1, 2], [1, 2]),
            ([1], [1]),
        ]
    )
    def test_req_true_success(self, sample, exception_value):
        class Owner:
            date = ClientIDsField(required=True)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)

    @cases(
        [
            ([], []),
            ([1, 2], [1, 2]),
            ([1], [1]),
        ]
    )
    def test_req_false_success(self, sample, exception_value):
        class Owner:
            date = ClientIDsField(required=False)

        my_owner = Owner()
        my_owner.date = sample

        self.assertEqual(my_owner.date, exception_value)


# if __name__ == "__main__":
#     unittest.main()
