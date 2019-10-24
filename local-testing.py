from lambda_function import lambda_handler

event = {
  "body": "{\n    \"hasher\": {\n        \"data\": [1,2,3,4,5,7,13,15,23],\n        \"rows\": 3,\n        \"columns\": 3\n    },\n    \"message\": \"Hello. My name is Jeff.\"\n}"
}

print(lambda_handler(event, None))