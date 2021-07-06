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

    firstname = models.CharField(max_length=20,null=False)
    lastname = models.CharField(max_length=20,null=False)
    email = models.CharField(max_length=128,null=False,unique=True)
    password = models.CharField(max_length=256,null=False)
    date_joined = models.DateTimeField(max_length=256,null=False,default=datetime.datetime.now())

    @classmethod
    def createUser(cls,userDetails):
        userDetails = cls(firstname=userDetails['firstname'],lastname=userDetails['lastname'],
                        email=userDetails['email'], password= str(hashedPassword(userDetails['password'])),
                        date_joined = datetime.datetime.now())
        return userDetails
