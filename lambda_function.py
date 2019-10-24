import json
import numpy as np
import re

# Constants
ENCRYPT_OPT = "encrypt"
DECRYPT_OPT = "decrypt"

def my_chr_to_int(s, offset = 64):
    if(ord(s) == 32):
        return 27
    return ord(s) - offset

def my_int_to_chr(i, offset = 64):
    if(i == 27):
        return ' '
    else:
         return chr(i + offset)

def steralize_message(s):
    s = s.upper()
    regex = re.compile(r'[A-Z ]')
    return list(filter(regex.search, s))

def message_to_matrix(message, rows, filter=True):
    message = steralize_message(message) if filter else message
    intlist = [my_chr_to_int(x) for x in message]
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
    flat = [int(round(x)) for x in hashed.flatten('F').tolist()]
    return {
        'numbers': flat,
        'rows': hasher['rows'],
        'columns': hasher['columns'],
        'message': ''.join(my_int_to_chr(x) for x in flat)
    }

def decrypt_message(message, hasher):
    hashmatrix = np.array(hasher['data']).reshape(hasher['rows'], hasher['columns'], order='F')
    unhashmatrix = np.linalg.inv(hashmatrix)
    messagematrix = message_to_matrix(message, hasher['rows'], False)
    hashed = np.dot(unhashmatrix, messagematrix)
    flat = [int(round(x)) for x in hashed.flatten('F').tolist()]
    return {
        'numbers': flat,
        'rows': hasher['rows'],
        'columns': hasher['columns'],
        'message': ''.join(my_int_to_chr(x) for x in flat)
    }
    
def lambda_handler(event, context):
    response = {"error": "Error occured"}

    req = json.loads(event['body'])
    operation = ENCRYPT_OPT if 'operation' not in req else req['operation']

    try:
      if(operation == ENCRYPT_OPT):
        response = encrypt_message(req['message'], req['hasher'])
      elif(operation == DECRYPT_OPT):
        response = decrypt_message(req['message'], req['hasher'])
      else:
        response = {"error": "The requested operation is not supported."}
    except np.linalg.LinAlgError as e:
      response = {"error": str(e)}
    except ValueError:
      response = {"error": "Cannot decrypt unencrypted message..."}
    except Exception:
      response = {"error": "Something went wrong."}

    return {
        'statusCode': 200,
        'body': json.dumps({
          "response": response
        })
    }
