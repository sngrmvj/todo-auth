from django.db import models
import hashlib , datetime
from django.db.models.base import Model

# Create your models here.

def hashedPassword(password):
    t_hashed = hashlib.sha3_512(password.encode())
    t_password = t_hashed.hexdigest()
    return t_password

class User(models.Model):
    class Meta:
        db_table = 'credentials'

    firstname = models.CharField(max_length=128,null=False,db_index=True)
    lastname = models.CharField(max_length=128,null=False,db_index=True)
    email = models.CharField(max_length=255,null=False,unique=True,db_index=True)
    password = models.CharField(max_length=256,null=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(max_length=256,null=False,default=datetime.datetime.now())

    @classmethod
    def createUser(cls,userDetails):
        userDetails = cls(firstname=userDetails['firstname'],lastname=userDetails['lastname'],
                        email=userDetails['email'], 
                        password= str(hashedPassword(userDetails['password'])),
                        is_admin= False,
                        date_joined = datetime.datetime.now())
        return userDetails



class Admin(models.Model):
    class Meta:
        db_table = 'admin_credentials'

    firstname = models.CharField(max_length=128,null=False,db_index=True)
    lastname = models.CharField(max_length=128,null=False,db_index=True)
    email = models.CharField(max_length=255,null=False,unique=True,db_index=True)
    password = models.CharField(max_length=256,null=False)
    is_admin = models.BooleanField(default=True)
    date_joined = models.DateTimeField(max_length=256,null=False,default=datetime.datetime.now())

    @classmethod
    def createUser(cls,userDetails):
        userDetails = cls(firstname=userDetails['firstname'],lastname=userDetails['lastname'],
                        email=userDetails['email'], password= str(hashedPassword(userDetails['password'])),
                        is_admin=True,date_joined = datetime.datetime.now())
        return userDetails



class RegisterTokens(models.Model): 

    class Meta:
        db_table = 'register_tokens'

    registered = models.CharField(max_length=512,null=False)
    user_id = models.IntegerField(unique=True,null=False)

    @classmethod
    def register_token(cls,token,userID):
        token_obj = cls(registered=str(token),user_id=userID)
        return token_obj



class BlacklistTokens(models.Model): 

    class Meta:
        db_table = 'blacklist_tokens'

    blacklist = models.CharField(max_length=512,db_index=True)

    @classmethod
    def blacklist_token(cls,tokendetails):
        token_obj = cls(blacklist=tokendetails['refresh'])
        return token_obj
