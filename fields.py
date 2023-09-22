import datetime

# class OnlineScoreRequest:
#     email = EmailField(required=False, nullable=True)
#     phone = PhoneField(required=False, nullable=True)
#     birthday = BirthDayField(required=False, nullable=True)
#     gender = GenderField(required=False, nullable=True)


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


class EmailField(CharField):
    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, date_value: str):
        # check string properties
        super().__set__(instance, date_value)

        # get attr which was set in parent class
        date_value = getattr(instance, self.value)

        # date_value is None -> escape
        if date_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if date_value == "":
            setattr(instance, self.value, str(date_value))
        else:
            if "@" in date_value:
                setattr(instance, self.value, date_value)
            else:
                raise ValueError("no @")


class DateField(CharField):
    def __init__(self, required: bool, nullable: bool):
        super().__init__(required, nullable)

    def __get__(self, instance, cls):
        return getattr(instance, self.value, self.value)

    def __set__(self, instance, date_value: str):
        # check string properties
        super().__set__(instance, date_value)

        # get attr which was set in parent class
        date_value = getattr(instance, self.value)

        # date_value is None -> escape
        if date_value is None:
            return

        # if empty str -> set this, else -> try to convert and set
        if date_value == "":
            setattr(instance, self.value, str(date_value))
        else:
            try:
                dt_date = datetime.datetime.strptime(date_value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("invalid format")
            else:
                setattr(instance, self.value, str(dt_date))


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
