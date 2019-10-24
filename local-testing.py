from lambda_function import lambda_handler

decryptevent = {
  "body": '''
{
    "hasher": {
        "data": [1,2,3,4,5,7,13,15,23],
        "rows": 3,
        "columns": 3
    },
    "message": "øĝƏǧȸ̺Ȑɬ΃ûĤƜĦŘǛŁƃȜ«Âă",
    "operation": "decrypt"
}
'''
}

encryptevent = {
  "body": '''
{
    "hasher": {
        "data": [1,2,3,4,5,7,13,15,23],
        "rows": 3,
        "columns": 3
    },
    "message": "Hello. My name is Jeff.",
    "operation": "encrypt"
}
'''
}

encrypteventError = {
  "body": '''
{
    "hasher": {
        "data": [1,2,3,4,5,7,13,15,23],
        "rows": 3,
        "columns": 3
    },
    "message": "Hello. My name is Jeff.",
    "operation": "decrypt"
}
'''
}

print(lambda_handler(encrypteventError, None))