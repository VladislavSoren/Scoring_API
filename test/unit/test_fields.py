import unittest
from test.support_functions import cases

from fields.fields import (
    ArgumentsField,
    BirthDayField,
    CharField,
    ClientIDsField,
    DateField,
    EmailField,
    GenderField,
    PhoneField,
)


class TestArgumentsField(unittest.TestCase):
    acceptable_range = GenderField.acceptable_range

    @cases(
        [
            ([1, 2], "must be a dict"),
            ({(1, "a"): "12345"}, "is not a valid json"),
            (None, "value is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            value = ArgumentsField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ([1, 2], "must be a dict"),
            ({(1, "a"): "12345"}, "is not a valid json"),
            ({}, "is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = ArgumentsField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ({"client_ids": {1: 2}, "date": "20.07.2017"}, {"client_ids": {1: 2}, "date": "20.07.2017"}),
            ({"client_ids": [], "date": "20.07.2017"}, {"client_ids": [], "date": "20.07.2017"}),
            ({}, {}),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = ArgumentsField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ({"client_ids": {1: 2}, "date": "20.07.2017"}, {"client_ids": {1: 2}, "date": "20.07.2017"}),
            ({"client_ids": [], "date": "20.07.2017"}, {"client_ids": [], "date": "20.07.2017"}),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = ArgumentsField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


class TestGenderField(unittest.TestCase):
    acceptable_range = GenderField.acceptable_range

    @cases(
        [
            ("123", "value must be an int"),
            (None, "value is None"),
            (5, "not in acceptable_range"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            value = GenderField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("123", "value must be an int"),
            # ("", "string is empty"),
            (5, "not in acceptable_range"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = GenderField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            (0, 0),
            (1, 1),
            # ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = GenderField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            (2, 2),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = GenderField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


class TestCharField(unittest.TestCase):
    @cases(
        [
            (123, "must be a str"),
            (None, "string is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            value = CharField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            (123, "must be a str"),
            ("", "string is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = CharField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("123", "123"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = CharField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ("123", "123"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = CharField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


class TestPhoneField(unittest.TestCase):
    @cases(
        [
            ("19996560820", "does not start with 7 or len != 11"),
            ("799965", "does not start with 7 or len != 11"),
            (None, "string is None"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            value = PhoneField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("19996560820", "does not start with 7 or len != 11"),
            ("799965", "does not start with 7 or len != 11"),
            ("", "string is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = PhoneField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("79996560820", "79996560820"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = PhoneField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ("79996560820", "79996560820"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = PhoneField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


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
            value = EmailField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            (123, "must be a str"),
            ("postmail.com", "no @"),
            ("", "string is empty"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = EmailField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("post@mail.com", "post@mail.com"),
            ("", ""),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = EmailField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ("post@mail.com", "post@mail.com"),
            (None, None),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = EmailField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


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
            value = DateField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [("10.11.201", "invalid format"), ("2019.10.11", "invalid format"), (123, "must be a str"), ("", "string is empty")]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = DateField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

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
            value = DateField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

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
            value = DateField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


class TestBirthDayField(unittest.TestCase):
    age_limit = BirthDayField.age_limit

    @cases(
        [
            ("10.11.201", "invalid format"),
            ("2019.10.11", "invalid format"),
            (123, "must be a str"),
            (None, "string is None"),
            ("10.11.1920", f"age more then {age_limit}"),
        ]
    )
    def test_req_nul_true_fail(self, sample, exception_text):
        class Owner:
            value = BirthDayField("value", required=True, nullable=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("10.11.201", "invalid format"),
            ("2019.10.11", "invalid format"),
            (123, "must be a str"),
            ("", "string is empty"),
            ("10.11.1920", f"age more then {age_limit}"),
        ]
    )
    def test_req_nul_false_fail(self, sample, exception_text):
        class Owner:
            value = BirthDayField("value", required=False, nullable=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ("10.11.2023", "2023-11-10"),
            ("1.5.2023", "2023-05-01"),
            ("01.05.2023", "2023-05-01"),
            ("", ""),
            ("10.11.1970", "1970-11-10"),
        ]
    )
    def test_req_nul_true_success(self, sample, exception_value):
        class Owner:
            value = BirthDayField("value", required=True, nullable=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ("10.11.2023", "2023-11-10"),
            ("1.5.2023", "2023-05-01"),
            ("01.05.2023", "2023-05-01"),
            (None, None),
            ("10.11.1970", "1970-11-10"),
        ]
    )
    def test_req_nul_false_success(self, sample, exception_value):
        class Owner:
            value = BirthDayField("value", required=False, nullable=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


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
            value = ClientIDsField("value", required=True)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            (None, "array must be a list"),
            ((1, 2), "array must be a list"),
            ([1, 1.1], "value in array must be an int"),
        ]
    )
    def test_req_false_fail(self, sample, exception_text):
        class Owner:
            value = ClientIDsField("value", required=False)

        my_owner = Owner()

        with self.assertRaisesRegex(Exception, exception_text):
            my_owner.value = sample

    @cases(
        [
            ([1, 2], [1, 2]),
            ([1], [1]),
        ]
    )
    def test_req_true_success(self, sample, exception_value):
        class Owner:
            value = ClientIDsField("value", required=True)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)

    @cases(
        [
            ([], []),
            ([1, 2], [1, 2]),
            ([1], [1]),
        ]
    )
    def test_req_false_success(self, sample, exception_value):
        class Owner:
            value = ClientIDsField("value", required=False)

        my_owner = Owner()
        my_owner.value = sample

        self.assertEqual(my_owner.value, exception_value)


# if __name__ == "__main__":
#     unittest.main()
