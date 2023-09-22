import datetime


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


class DateField:
    def __init__(self, required: bool, nullable: bool):
        self.required = required
        self.nullable = nullable
        self.date = "_date"

    def __get__(self, instance, cls):
        return getattr(instance, self.date, self.date)

    def __set__(self, instance, date_str: str):
        # Validation
        # check for emptiness
        # if
        if self.required:
            if date_str is None:
                raise Exception("date string is None, required=True")
        else:
            if date_str is None:
                setattr(instance, self.date, None)
                return

        if not self.nullable and (date_str == ""):
            raise Exception("date string is empty, nullable=False")

        # str check
        if not isinstance(date_str, str):
            raise TypeError("date string must be a str")

        #
        if date_str == "":
            setattr(instance, self.date, str(date_str))
        else:
            try:
                dt_date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("invalid format")
            else:
                setattr(instance, self.date, str(dt_date))


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
