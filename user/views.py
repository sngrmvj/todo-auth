import user
from django.http.response import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse

from user.models import User,RegisterTokens,BlacklistTokens
from user.admin import GENERATED_OTP, REFRESH_TOKEN_NAME,ACCESS_TOKEN_NAME
from toDo.settings import SECRET_KEY
import json,jwt,hashlib,datetime,random,math


### 
# >>>> Helper Functions
###

def create_refresh_token(id):
    try:
        payload ={
            'token_type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'project': 'to-do',
            'userID': id
        }
        
        return jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    except Exception as error:
        print(f"Error ocurred during creation of token - {error}")
        return (f"Error ocurred during creation of token - {error}") 

# >>>> Token generation
def createToken(data):

    if data.is_admin == False:
        role = 'user'
        permissions = 'only_task'
    else:
        role = 'admin'
        permissions = 'admin_access'

    try:
        payload = {
            'token_type': 'access',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=10),
            'firstname': data.firstname,
            'lastname': data.lastname,
            'email': data.email,
            'roles': role,
            'permissions': permissions
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

# >>>> Generate OTP
def generate_otp():

    digits = [i for i in range(0, 10)]
    random_str = "P-"
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    return random_str




# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------





###
# Create your views here.
###



# ---------------------------------------------------------------------------------------------------------

#>>>> Login Page

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

        userDetails = User.objects.filter(email=body['email'])
        if not userDetails:
            return Response({'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json")
        userDetails = userDetails[0]
        if (userDetails.email == body['email'] and userDetails.password == encoded_password):
            access_token = createToken(userDetails)
            is_reg_token_avail = RegisterTokens.objects.filter(user_id=userDetails.id)
            if is_reg_token_avail:
                is_reg_token_avail.delete()
            refresh_token = create_refresh_token(userDetails.id)
            token_register = RegisterTokens.register_token(refresh_token,userDetails.id)
            token_register.save()
            headers={"access-control-expose-headers": "Set-Cookie"}
            response = Response({'message':'Successfully Logged In',"admin":userDetails.is_admin,'id':userDetails.id}, status=status.HTTP_200_OK,content_type="application/json",headers=headers)
            # If we don't keep expires in set_cookie() it gets deleted automatically when browser gets closed.
            response.set_cookie(key= REFRESH_TOKEN_NAME,value=refresh_token,httponly=True,expires=datetime.datetime.utcnow() + datetime.timedelta(days=30))
            response.set_cookie(key= ACCESS_TOKEN_NAME,value=access_token,httponly=True,expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=10))
            return response
        else:
            return Response({'message':'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during login - {error}")
        return Response({'error':f"Error ocurred during login - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")


# ---------------------------------------------------------------------------------------------------------








# ---------------------------------------------------------------------------------------------------------

# >>>> Sign Up page
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
        userDetails = User.objects.filter(email=body['email'])
        if not userDetails:
            userDetails = User.createUser(body)
            userDetails.save()
        else:
            return Response({'message':'User already Exists'}, status=status.HTTP_409_CONFLICT,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during signup - {error}")
        return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST,content_type="application/json")

    return Response({'message':'User Created Successfully'}, status=status.HTTP_201_CREATED,content_type="application/json")



# ---------------------------------------------------------------------------------------------------------







# ---------------------------------------------------------------------------------------------------------


# # >>>> Token Verification
# @api_view(http_method_names=['PUT'])
# def authorization(request):

#     """
#         Note - This function is to validate the user by decoding the token.
#         * This is not required. We never decode the token and verify the values of it.
#         There are a lot of ways to implement JWT token authentication.
#     """

#     try:
#         decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
#         if isinstance(decoded_token,str):
#             return Response({'error':decoded_token}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json") 
#     except Exception as error:
#         return Response({'error':error}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")

#     try:
#         userDetails = User.objects.get(email=decoded_token['email'])
#         print(userDetails.email)
#     except TypeError:
#         return Response({'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json") 
    
#     if (userDetails.email == decoded_token['email'] and userDetails.firstname == decoded_token['firstname']):
#         return Response({'message':'Authorized Successfully'}, status=status.HTTP_202_ACCEPTED,content_type="application/json")
#     else:
#         return Response({'message':'Unauthorized action !!'}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")




# ---------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------

# >>>> Important not to access the planners without valid refresh token

@api_view(http_method_names=['GET'])
def check_your_authorization(request):

    try:  
        registered_tokens = RegisterTokens.objects.get(registered= request.COOKIES['todo-refreshToken'])
    except Exception as error:
        print(f"Error ocurred during fetch of the registered tokens - {error}")
        return Response({'error':f"Error ocurred during fetch of the registered tokens - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")

    try:
        refresh_token =  request.COOKIES[REFRESH_TOKEN_NAME] 
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        if decoded_token['project'] == 'to-do':
            # Get the current time in seconds
            present_time = int(datetime.datetime.utcnow().timestamp())
            # Check whether the expiry time is more than the present time
            if (decoded_token['exp'] - present_time) < 1:
                registered_tokens.delete()
                # Ask the user to Login again
                return Response({'message':'Please login again !!!','flag':False}, status=status.HTTP_200_OK,content_type="application/json")
            else:
                return Response({'message':'You are good. No worries'}, status=status.HTTP_200_OK,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during check of authorization - {error}")
        return Response({'error':f"Error ocurred during check of authorization - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")




# ---------------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------------


# >>>> Refresh Token
@api_view(http_method_names=['GET'])
def get_access_token(request):

    """
        Note -
        Here we refresh the access token using the refresh token. 
        We are storing the refresh token along with the user id in database.
        If the refresh token expires we are creating the new refresh token and access token.
        If the refresh token doesn't exist in the database we navigate to login page.
    """

    # # Query Parameter
    # check_default = request.query_params.get('blacklist')
    # check_default = check_default.capitalize()
    # registered_tokens.delete()
    # blacklist = BlacklistTokens.blacklist_token(body)
    # blacklist.save()
    # return Response({'message':'Please Login again','flag':False}, status=status.HTTP_403_FORBIDDEN,content_type="application/json")

    # Fetching the registered tokens
    try:  
        registered_tokens = RegisterTokens.objects.get(registered= request.COOKIES['todo-refreshToken'])
    except Exception as error:
        print(f"Error ocurred during fetch of the registered tokens - {error}")
        return Response({'error':f"Error ocurred during fetch of the registered tokens - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")

    if not registered_tokens:
        return Response({'message':'Unauthorized access. Please try to Login','flag':False}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")

    try:

        # Getting the content of the body
        refresh_token =  request.COOKIES[REFRESH_TOKEN_NAME] 
        # Decode the Refresh Token
        decoded_token = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        print(">>>> The refresh token is valid")
        # Get the current time in seconds
        present_time = int(datetime.datetime.utcnow().timestamp())
        # Check whether the expiry time is more than the present time
        if (decoded_token['exp'] - present_time) < 1:
            # Deleting the refresh token for the particular user
            registered_tokens.delete()
            # Ask the user to Login again
            return Response({'message':'Please login again !!!','flag':False}, status=status.HTTP_200_OK,content_type="application/json")


        # So we fetch the details of the user using the user id from the refresh token.
        userDetails = User.objects.get(id=decoded_token['userID'])
        # Creatng the access token using the userdetails that we get from above.
        access_token = createToken(userDetails)

        headers={"access-control-expose-headers": "Set-Cookie"}
        response = Response({'message':'Token successfully deployed','flag':True}, status=status.HTTP_200_OK,content_type="application/json",headers=headers)
        response.set_cookie(key= ACCESS_TOKEN_NAME,value=access_token,httponly=True,expires=datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=10))
        return response
    except Exception as error:
        print(f"Error ocurred during refresh of the access token - {error}")
        return Response({'error':f"Error ocurred during refresh of the access token - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")
        

# ---------------------------------------------------------------------------------------------------------






# ---------------------------------------------------------------------------------------------------------


def blacklistTokens():
    pass



# ---------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------

# >>>> make A person Admin
@api_view(http_method_names=['PUT'])
def makeAdmin(request):
    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        if body['email'] != "":
            User.objects.get(id=body['email']).update(is_admin=True)
        else:
            raise Exception("Email to be updated is empty")

        return Response({'message':'Successfully Updated'},status=status.HTTP_200_OK,content_type="application/json")

    except Exception as error:
        print(f"Error ocurred during fetching details of is admin - {error}")
        return Response({'error':f"Error ocurred during fetching details of is admin - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")


# ---------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------

# >>>> Get All User details
@api_view(http_method_names=['GET'])
def get_all_user_details(request):

    try:
        user_list = User.objects.all()
        all_users = {}
        for user in user_list:
            all_users[user.id] = {'firstname':user.firstname,'lastname':user.lastname,'email':user.email,'isadmin':user.is_admin}
        return Response({'message':all_users},status=status.HTTP_200_OK,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during fetching of all user details - {error}")
        return Response({'error':f"Error ocurred during fetching of all user details - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")


# ---------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------

# >>>> Get one user
@api_view(http_method_names=['GET'])
def get_user(request):

    try:
        id = request.query_params.get('id')
        user_list = User.objects.filter(id=id)
        user = user_list[0]
        if user_list:
            all_users = {}
            all_users['content'] = {'id':user.id,'firstname':user.firstname,'lastname':user.lastname,'email':user.email,'isadmin':user.is_admin}
            return Response({'message':all_users},status=status.HTTP_200_OK,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during fetching of all user details - {error}")
        return Response({'error':f"Error ocurred during fetching of all user details - {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")


# ---------------------------------------------------------------------------------------------------------









# ---------------------------------------------------------------------------------------------------------

# >>>> Generate OTP
@api_view(http_method_names=['PUT'])
def send_otp(request):

    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        userDetails = User.objects.get(email=body['email'])
        if not userDetails:
            return Response({'message':'User Not Found'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json")
        else:
            global GENERATED_OTP
            GENERATED_OTP = generate_otp()
    except Exception as error:
        print(f"Error ocurred during sending of token - {error}")
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")



# ---------------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------------

# >>>>  OTP VERIFICATION
@api_view(http_method_names=['PUT'])
def otp_verify(request):

    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        if body['otp'] is None:
            return Response({'message':'OTP did not match'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json")
        elif body['otp'] == GENERATED_OTP:
            return Response({'message':'OTPs Matched','flag':True}, status=status.HTTP_200_OK,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during verification of OTP - {error}")
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")


# ---------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------

# >>>>  CHANGE PASSWORD
@api_view(http_method_names=['PUT'])
def change_password(request):

    """
        Note - 
        Here we used refresh token for finding the user. Refresh token contains the user id.
        Using the user id we can query the DB to update the user password.
    """


    try:
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']
        try:
            decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
            if isinstance(decoded_token,str):
                return Response({'error':decoded_token}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json") 
        except Exception as error:
            return Response({'error':error}, status=status.HTTP_401_UNAUTHORIZED,content_type="application/json")

        userDetails = User.objects.get(id=decoded_token['userID'])
        if userDetails:
            userDetails = User.objects.filter(id=decoded_token['userID']).update(password=body['password'])
            userDetails.save()
            return Response({'message':'Password successfully Updated','flag':True}, status=status.HTTP_200_OK,content_type="application/json")
        else:
            return Response({'message':'User not found'}, status=status.HTTP_404_NOT_FOUND,content_type="application/json")
    except Exception as error:
        print(f"Error ocurred during changing password - {error}")
        return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")





# ---------------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------------

# >>>>  Update USER Email
@api_view(http_method_names=['PUT'])
def update_user_email(request):
    
    """
        Note - 
        Mostly to update the email.
    """

    try:
    
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        #refresh token
        decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
        if body['email'] != "":
            User.objects.get(id=decoded_token['userID']).update(email=body['email'])
        else:
            raise Exception("Email to be updated is empty")

        return Response({'message':'Email successfully Updated','flag':True}, status=status.HTTP_200_OK,content_type="application/json")

    except Exception as error:
        print(f"Error ocurred during updating of user details - {error}")
        return Response({"error":error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")



# ---------------------------------------------------------------------------------------------------------








# ---------------------------------------------------------------------------------------------------------

# >>>>  Update USER Firstname
@api_view(http_method_names=['PUT'])
def update_user_firstname(request):
    
    """
        Note - 
        Mostly to update the email.
    """

    try:
    
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        #refresh token
        decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
        if body['firstname'] != "":
            User.objects.get(id=decoded_token['userID']).update(firstname=body['firstname'])
        else:
            raise Exception("Firstname to be updated is empty")

        return Response({'message':'Firstname successfully Updated','flag':True}, status=status.HTTP_200_OK,content_type="application/json")

    except Exception as error:
        print(f"Error ocurred during updating of user details - {error}")
        return Response({"error":error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")




# ---------------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------------


# >>>> Update USER Lastname
@api_view(http_method_names=['PUT'])
def update_user_lastname(request):
    
    """
        Note - 
        Mostly to update the Lastname.
    """

    try:
    
        body = request.body.decode('utf-8')
        body = json.loads(body)
        body = body['content']

        #refresh token
        decoded_token = validate_and_decode_token(request.headers.get('Authorization', None))
        if body['lastname'] != "":
            User.objects.get(id=decoded_token['userID']).update(lastname=body['lastname'])
        else:
            raise Exception("Lastname to be updated is empty")

        return Response({'message':'Lasttname successfully Updated','flag':True}, status=status.HTTP_200_OK,content_type="application/json")

    except Exception as error:
        print(f"Error ocurred during updating of user details - {error}")
        return Response({"error":error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")





# ---------------------------------------------------------------------------------------------------------







# ---------------------------------------------------------------------------------------------------------


# >>>>  DELETE USER (Admin Page)
@api_view(http_method_names=['DELETE'])
def delete_user(request):
    
    
    try:
        token = request.headers.get('Authorization', None)
        decoded_token = validate_and_decode_token(token)

        # Removing the Bearer string from the token
        token = token.split(" ")[1] 
        registered_tokens = RegisterTokens.objects.get(registered=token)
        # if the token exists we can delete the token
        if registered_tokens:
            body = {
                'refresh': token
            }
            registered_tokens.delete()
            blacklist = BlacklistTokens.blacklist_token(body)
            blacklist.save()
        
        # Deleting the user with the user id
        User.objects.get(id=decoded_token['userID']).delete()
        
        return Response({'message':'User deleted Successfully','flag':True}, status=status.HTTP_200_OK,content_type="application/json")

    except Exception as error:
        return Response({'error':error,'flag':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type="application/json")




# ---------------------------------------------------------------------------------------------------------













