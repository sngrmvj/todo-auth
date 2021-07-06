from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from user.models import User
from toDo.settings import SECRET_KEY
import json,jwt,hashlib,datetime


### 
# >>>> Helper Functions
###

# >>>> Token generation
def createToken(data):

    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=9),
            'iat': datetime.datetime.utcnow(),
            'firstname': data.firstname,
            'lastname': data.lastname,
            'email': data.email
        }
        return jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    except Exception as error:
        print(f"Error ocurred during creation of token - {error}")
        return (f"Error ocurred during creation of token - {error}") 


    
# >>>> Hashing the password
def hashedPassword(password):
    t_hashed = hashlib.sha3_512(password.encode())
    t_password = t_hashed.hexdigest()
    return t_password


# >>>> Token Validation by decoding the token.
def validate_and_decode_token(token):
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'





###
# Create your views here.
###

@api_view(http_method_names=['PUT'])
def login(request):

    """
    Note - The function is for logging the user
    """

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

    """
    Note - This function is to create the user
    """

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




@api_view(http_method_names=['PUT'])
def token_validation(request):

    """
        Note - This function is to validate the user by decoding the token.
    """

    try:
        decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
        if isinstance(decoded_token,str):
            return Response({'error':decoded_token}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json") 
    except Exception as error:
        return Response({'error':error}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")

    try:
        userDetails = User.objects.get(email=decoded_token['email'])
        print(userDetails.email)
    except TypeError:
        return Response({'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json") 
    
    if (userDetails.email == decoded_token['email'] and userDetails.firstname == decoded_token['firstname']):
        return Response({'message':'Authorized Successfully'}, status=status.HTTP_202_ACCEPTED,content_type="application/json")
    else:
        return Response({'message':'Unauthorized action !!'}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")


