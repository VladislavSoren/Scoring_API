import functools
import unittest

from fields import DateField


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)

        return wrapper

    return decorator


class TestFields(unittest.TestCase):
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
