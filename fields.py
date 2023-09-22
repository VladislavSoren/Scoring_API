import datetime


def timedelta_to_years(delta: datetime.timedelta) -> int:
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)


# class OnlineScoreRequest:
#     gender = GenderField(required=False, nullable=True)


class IntegerField:
    def __init__(self, required, nullable):
        self.required = required
        self.nullable = nullable
        self.value = "_value"
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise Exception("value is None, required=True")
        else:
            if value is None:
                setattr(instance, self.value, None)
                return

        # type check
        if not isinstance(value, int):
            raise TypeError("value must be an int")

        setattr(instance, self.value, value)


class GenderField(IntegerField):
    acceptable_range = (0, 1, 2)

    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.value)

        # input_value is None -> escape
        if input_value is None:
            return

        if input_value in self.acceptable_range:
            setattr(instance, self.value, input_value)
        else:
            setattr(instance, self.value, None)
            raise Exception("not in acceptable_range")


class CharField:
    def __init__(self, required, nullable):
        self.required = required
        self.nullable = nullable
        self.value = "_value"
        self.default = None

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise Exception("string is None, required=True")
        else:
            if value is None:
                setattr(instance, self.value, None)
                return

        # empty error if nullable=False
        if not self.nullable and (value == ""):
            raise Exception("string is empty, nullable=False")

        # str type check
        if not isinstance(value, str):
            raise TypeError("string must be a str")

        setattr(instance, self.value, value)


class PhoneField(CharField):
    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.value)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.value, str(input_value))
        else:
            if input_value.startswith("7") and len(input_value) == 11:
                setattr(instance, self.value, input_value)
            else:
                raise ValueError("does not start with 7 or not len != 11")


class EmailField(CharField):
    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.value)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.value, str(input_value))
        else:
            if "@" in input_value:
                setattr(instance, self.value, input_value)
            else:
                raise ValueError("no @")


class DateField(CharField):
    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.value)

        # input_value is None -> escape
        if input_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if input_value == "":
            setattr(instance, self.value, str(input_value))
        else:
            try:
                dt_date = datetime.datetime.strptime(input_value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("invalid format")
            else:
                setattr(instance, self.value, str(dt_date))


class BirthDayField(DateField):
    age_limit = 70

    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, input_value: str):
        # check string properties
        super().__set__(instance, input_value)

        # get attr which was set in parent class
        input_value = getattr(instance, self.value)

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
            setattr(instance, self.value, "")
            raise ValueError(f"age more then {self.age_limit}")
        else:
            setattr(instance, self.value, input_value)


class ClientIDsField:
    def __init__(self, required):
        self.required = required
        self.client_ids = "_client_ids"

    def __get__(self, instance, cls):
        return getattr(instance, self.client_ids, self.client_ids)

    def __set__(self, instance, ints_list):
        # Validation
        # check for emptiness
        if self.required and not ints_list:
            raise Exception("array is empty")

        # list check
        if not isinstance(ints_list, list):
            raise TypeError("array must be a list")

        # values in list check
        for int_value in ints_list:
            if not isinstance(int_value, int):
                raise TypeError("value in array must be an int")

        setattr(instance, self.client_ids, ints_list)


# response = {
#     'client_ids': [1, 2],
#     'date': '2023-09-21'
# }
#
# ClientsInterestsRequest = ClientsInterestsRequest
# try:
#     ClientsInterestsRequest.client_ids = response['client_ids']
#     # ClientsInterestsRequest.date = response['date']
# except Exception as e:
#     print(e)
#
# pass
