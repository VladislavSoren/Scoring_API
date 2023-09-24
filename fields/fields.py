import datetime
import json

from .custom_errors import NoneError, NullError, ValidationError


def timedelta_to_years(delta: datetime.timedelta) -> int:
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)


class BaseField:
    def __init__(self, name: str, required: bool, nullable: bool):
        self.required = required
        self.nullable = nullable
        self.name = "_" + name
        self.default = None


class ArgumentsField(BaseField):
    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise NoneError(f"{self.name} - value is None, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # type check
        if not isinstance(value, dict):
            raise TypeError(f"{self.name} - must be a dict")

        # empty error if nullable=False
        if not self.nullable and (value == {}):
            raise NullError(f"{self.name} - is empty, nullable=False")

        # check valid property
        try:
            _ = json.dumps(value)  # get json_string
        except TypeError:
            raise TypeError(f"{self.name} - is not a valid json")
        else:
            setattr(instance, self.name, value)
        # json_dict = json.loads(json_string)


class IntegerField(BaseField):
    def __init__(self, name: str, required: bool, nullable: bool):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise NoneError(f"{self.name} - value is None, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # type check
        if not isinstance(value, int):
            raise TypeError(f"{self.name} - value must be an int")

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
            raise ValidationError(f"{self.name} - not in acceptable_range")


class CharField(BaseField):
    def __init__(self, name, required, nullable):
        super().__init__(name, required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        # Validation
        if self.required:
            if value is None:
                raise NoneError(f"{self.name} - string is None, required=True")
        else:
            if value is None:
                setattr(instance, self.name, None)
                return

        # empty error if nullable=False
        if not self.nullable and (value == ""):
            raise NullError(f"{self.name} - string is empty, nullable=False")

        # str type check
        if not isinstance(value, str):
            raise TypeError(f"{self.name} - string must be a str")

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
                raise ValidationError(f"{self.name} - does not start with 7 or len != 11")


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
                raise ValueError(f"{self.name} - no @")


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
                raise ValueError(f"{self.name} - invalid format")
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
            raise ValueError(f"{self.name} - age more then {self.age_limit}")
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
            raise NoneError(f"{self.name} - array is empty")

        # list check
        if not isinstance(value, list):
            raise TypeError(f"{self.name} - array must be a list")

        # values in list check
        for int_value in value:
            if not isinstance(int_value, int):
                raise TypeError(f"{self.name} - value in array must be an int")

        setattr(instance, self.name, value)
