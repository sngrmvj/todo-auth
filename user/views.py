from typing import Sequence
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user.models import User
from toDo.settings import SECRET_KEY
import json,jwt,hashlib


### 
# >>>> Helper Functions
###

# >>>> Token generation
def createToken(data):
    tokenDetails = {
        'firstname': data.firstname,
        'lastname': data.lastname,
        'email': data.email
    }
    encoded_token = jwt.encode(tokenDetails,SECRET_KEY,algorithm='HS256')
    return encoded_token
    
# >>>> Hashing the password
def hashedPassword(password):
    t_hashed = hashlib.sha3_512(password.encode())
    t_password = t_hashed.hexdigest()
    return t_password


def validateToken(token):
    encoded_token = jwt.decode(token,SECRET_KEY,algorithm=['HS256'])


###
# Create your views here.
###


@api_view(http_method_names=['PUT'])
def login(request):

    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']
        encoded_password = str(hashedPassword(body['password']))

        userDetails = User.objects.get(email=body['email'])
        if (userDetails.email == body['email'] and userDetails.password == encoded_password):
            token = createToken(userDetails)
            return Response({'message':'Authenticated Successfully','token':token}, status=status.HTTP_200_OK,content_type="application/json")
        else:
            return Response({'message':'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")
    except Exception as error:
        print(error)
        return Response({'error':error}, status=status.HTTP_404_NOT_FOUND,content_type="application/json")




@api_view(http_method_names=['POST'])
def signup(request):

    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        # Inserting data into database
        userDetails = User.objects.get(email=body['email'])
        if userDetails.email == None or userDetails.email == '':
            userDetails = User.createUser(body)
            userDetails.save()
        else:
            return Response({'message':'User already Exists'}, status=status.HTTP_409_CONFLICT,content_type="application/json")
    except Exception as error:
        print(error)
        return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")

    return Response({'message':'User Created Successfully'}, status=status.HTTP_201_CREATED,content_type="application/json")
