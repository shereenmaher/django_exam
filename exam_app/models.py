from django.db import models
import re
import bcrypt
from datetime import date

class UserManager(models.Manager):
    #reg Validation
    def reg_validation(self,postData):

        errors={}

        first_name=postData["first_name"]
        last_name=postData["last_name"]
        email=postData["email"]
        password=postData["password"]
        confirm_pw=postData["confirm_pw"]

        if len(first_name) == 0:
            errors["firstnameerror"] = "first name is required"
        if len(last_name) == 0:
            errors["lastnameerror"] = "last name is required"
        if len(email) == 0:
            errors["emailerror"] = "email is required"
        if len(password) == 0:
            errors["passworderror"] = "password is required"
        if len(first_name) < 2:
            errors["firstnameerror"] = "first name must be at least 2 characters"
        if len(last_name) <2:
            errors["lastnameerror"] = "last name must be at least two characters"
        if len(password) < 8 and len(password) > 0:
            errors["passworderror"] = "Password must be at least 8 characters"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        )

        if email and not EMAIL_REGEX.match(email):
            errors["emailerror"] = "Invalid email address"

        if password != confirm_pw:
            errors["confirm_pwerror"] = "Passwords do not match"

        if User.objects.filter(email=email).exists():
            errors["email"] = "email already exists"

        return errors

    def create_user(self, postData):

        password = postData["password"]

        pw_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        user = User.objects.create(
            firstname=postData["first_name"],
            lastname=postData["last_name"],
            email=postData["email"],
            password=pw_hash.decode()
        )

        return user

    def log_validation(self, postData):

        errors = {}

        email = postData["email"]
        password = postData["password"]

        if len(email) == 0:
            errors["loginemailerror"] = "email is required"

        if len(password) == 0:
            errors["loginpassworderror"] = "Password is required"

        if len(errors) == 0:

            if User.objects.filter(email=email).exists():

                user = User.objects.get(email=email)

                if not bcrypt.checkpw(
                    password.encode(),
                    user.password.encode()
                ):
                    errors["loginerror"] = "Invalid email or password"

            else:
                errors["loginerror"] = "Invalid email or password"

        return errors

    def login_user(self, postData):

        email = postData["email"]
        password = postData["password"]

        user = User.objects.get(email=email)

        if bcrypt.checkpw(
            password.encode(),
            user.password.encode()
        ):
            return user

        return None

class ShowManager(models.Manager):

    def show_validation(self, postData):

        errors = {}

        title = postData["title"]
        network = postData["network"]
        released_date = postData["released_date"]
        comments = postData["comments"]
        if len(title) == 0:
            errors["titleerror"] = "title is required"
        if len(network) == 0:
            errors["networkerror"] = "network is required"
        if len(released_date) == 0:
            errors["releaseddateerror"] = "released_date is required"
        if len(comments) == 0:
            errors["commentserror"] = "comments is required"
        if len(title) < 3 :
            errors["titleerror"] = "title is required"
        if len(network) < 3:
            errors["networkerror"] = "network is required"
        if len(comments) < 3 :
            errors["commentserror"] = "comments is required"

    def create_show(self, postData, user):

        show = Show.objects.create(
            title = postData["title"],
            network = postData["network"],
            released_date = postData["released_date"],
            comments = postData["comments"],
            user=user
        )

        return show

    def update_show(self, show, postData):

        show.title = postData["title"]
        show.network=postData["network"]
        show.released_date=postData["released_date"]
        show.comments=postData["comments"]
        show.save()
        


class User(models.Model):
    firstname = models.CharField( max_length=200)
    lastname = models.CharField(max_length=200 )
    email = models.CharField( max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Show(models.Model):
    title=models.CharField(max_length=200,unique=True)
    network=models.CharField(max_length=200)
    released_date=models.DateField(null=True)
    comments=models.CharField(max_length=200)
    user = models.ForeignKey(User,related_name="shows",on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    object=ShowManager()
        
