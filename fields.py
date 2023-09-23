import datetime
import json


def timedelta_to_years(delta: datetime.timedelta) -> int:
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)


class ArgumentsField:
    def __init__(self, name: str, required: bool, nullable: bool):
        self.required = required
        self.nullable = nullable
        self.name = "_" + name
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise Exception("value is None, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # type check
        if not isinstance(value, dict):
            raise TypeError("must be a dict")

        # empty error if nullable=False
        if not self.nullable and (value == {}):
            raise Exception("is empty, nullable=False")

        # check valid property
        try:
            _ = json.dumps(value)  # get json_string
        except Exception:
            raise Exception("is not a valid json")
        else:
            setattr(instance, self.name, value)
        # json_dict = json.loads(json_string)


class IntegerField:
    def __init__(self, name: str, required: bool, nullable: bool):
        self.required = required
        self.nullable = nullable
        self.name = "_" + name
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise Exception("value is None, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # type check
        if not isinstance(value, int):
            raise TypeError("value must be an int")

        setattr(instance, self.name, value)


class GenderField(IntegerField):
    acceptable_range = (0, 1, 2)

    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.name)

        # input_value is None -> escape
        if input_value is None:
            return

        if input_value in self.acceptable_range:
            setattr(instance, self.name, input_value)
        else:
            setattr(instance, self.name, None)
            raise Exception("not in acceptable_range")


class CharField:
    def __init__(self, name, required, nullable):
        self.required = required
        self.nullable = nullable
        self.name = "_" + name
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise Exception(f"string is None in {self.name}, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # empty error if nullable=False
        if not self.nullable and (value == ""):
            raise Exception(f"string is empty in {self.name}, nullable=False")

        # str type check
        if not isinstance(value, str):
            raise TypeError(f"string must be a str in {self.name}")

        setattr(instance, self.name, value)


class PhoneField(CharField):
    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.name)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.name)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.name, str(input_value))
        else:
            if input_value.startswith("7") and len(input_value) == 11:
                setattr(instance, self.name, input_value)
            else:
                raise ValueError("does not start with 7 or not len != 11")


class EmailField(CharField):
    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.name)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.name, str(input_value))
        else:
            if "@" in input_value:
                setattr(instance, self.name, input_value)
            else:
                raise ValueError("no @")


class DateField(CharField):
    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.name)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.name, str(input_value))
        else:
            try:
                dt_date = datetime.datetime.strptime(input_value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("invalid format")
            else:
                setattr(instance, self.name, str(dt_date))


class BirthDayField(DateField):
    age_limit = 70

    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.name)

        # input_value is None or "" -> escape
        if input_value is None:
            return
        if input_value == "":
            return

        birth_date = datetime.datetime.strptime(input_value, "%Y-%m-%d").date()
        current_date = datetime.datetime.now().date()
        delta_time = current_date - birth_date
        delta_years = timedelta_to_years(delta_time)

        if delta_years > self.age_limit:
            setattr(instance, self.name, "")
            raise ValueError(f"age more then {self.age_limit}")
        else:
            setattr(instance, self.name, input_value)


class ClientIDsField:
    def __init__(self, name: str, required: bool):
        self.required = required
        self.name = "_" + name
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        # check for emptiness
        if self.required and not value:
            raise Exception("array is empty")

        # list check
        if not isinstance(value, list):
            raise TypeError("array must be a list")

        # values in list check
        for int_value in value:
            if not isinstance(int_value, int):
                raise TypeError("value in array must be an int")

        setattr(instance, self.name, value)


#     @cases([
#         {},
#         {"date": "20.07.2017"},
#         {"client_ids": [], "date": "20.07.2017"},
#         {"client_ids": {1: 2}, "date": "20.07.2017"},
#         {"client_ids": ["1", "2"], "date": "20.07.2017"},
#         {"client_ids": [1, 2], "date": "XXX"},
#     ])
#     def test_invalid_interests_request(self, arguments):
#         request = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
#         self.set_valid_auth(request)
#         response, code = self.get_response(request)
#         self.assertEqual(api.INVALID_REQUEST, code, arguments)
#         self.assertTrue(len(response))
