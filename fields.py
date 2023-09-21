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
