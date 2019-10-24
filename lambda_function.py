import json
import numpy as np
import re

reqexample = '''
{
    "hasher": {
        "data": [1,2,3,4,5,7,13,15,23],
        "rows": 3,
        "columns": 3
    },
    "message": "Hello. My name is Jeff."
}
'''

def my_chr_to_int(s, offset = 64):
    if(ord(s) is 32):
        return 27
    return ord(s) - offset

def my_int_to_chr(i, offset = 64):
    if(i is 27):
        return ' '
    else:
         return chr(i + offset)

def steralize_message(s):
    s = s.upper()
    regex = re.compile(r'[A-Z ]')
    return list(filter(regex.search, s))

def message_to_matrix(message, rows):
    intlist = [my_chr_to_int(x) for x in steralize_message(message)]
    # Add elements if the length is not divisible by the number of rows.
    diff = len(intlist) % rows
    if(diff != 0):
        for i in range(rows - diff):
            intlist.append(27) # TODO: Abstract this away
    matrix = np.array(intlist).reshape((rows, int(len(intlist) / rows)), order='F')
    return matrix
    
    
def encrypt_message(message, hasher):
    hashmatrix = np.array(hasher['data']).reshape(hasher['rows'], hasher['columns'], order='F')
    messagematrix = message_to_matrix(message, hasher['rows'])
    hashed = np.dot(hashmatrix, messagematrix)
    flat = hashed.flatten('F').tolist()
    return {
        'numbers': flat,
        'rows': hasher['rows'],
        'columns': hasher['columns'],
        'message': ''.join(my_int_to_chr(x) for x in flat)
    }
    
def lambda_handler(event, context):
    
    req = json.loads(event['body'])

    response = {
        "response": encrypt_message(req['message'], req['hasher']),
        "event": event
    }
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
