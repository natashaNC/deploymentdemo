from django.db import models
import re
import bcrypt

class PostManager(models.Manager):
    def postValidator(self, postData):
        errors= {}
        if len(postData['rant']) < 5:
            errors['rantLength'] = "You must rant harder"
        return errors

class UserManager(models.Manager):
    def loginValidator(self, postData):
        errors= {}
        usersWithemail = User.objects.filter(email= postData['email'])
        #validation if checks here
        #1. fill out the email portion
        if len(postData['email']) == 0:
            errors['emailreq'] = "Email is required to login."

        #2. check if email exists in db
        elif len(usersWithemail) == 0:
            errors['emailnotfound'] = "Email is not found. Please register first."
        
        #3. check if password matches
        else:
            userToCheck = usersWithemail[0]
            print(usersWithemail)
            print(usersWithemail[0])
            print(usersWithemail[0].password)
            if bcrypt.checkpw(postData['pw'].encode(), usersWithemail[0].password.encode()):
                print("password matches")
            else:
                errors['pwmatch'] = "Password is incorrect"

            #     if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
            #         print("password match")
            #     else:
            #         print("failed password")
        return errors
    def regValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        
        #validation if checks
        if len(postData['fname']) == 0:
            errors['fnamereq'] = "First name is required"
        if len(postData['email']) == 0:
            errors['emailreq'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalidemail'] = "Email is not real. Let's be real"
        else:
            repeatEmail = User.objects.filter(email = postData['email'])
            if len(repeatEmail)> 0:
                errors['emailTaken'] = "This email is already taken"
        if len(postData['pw']) < 4:
            errors['pwreq'] = "PW must be at least 4 char"
        if postData['pw'] != postData['cpw']:
            errors['confirmpw'] = "Confirm password must match"
        return errors



# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # objects = models.Manager()

class Post(models.Model):
    content = models.TextField()
    uploader = models.ForeignKey(User, related_name= "posts_uploaded", on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name= "posts_liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PostManager()

