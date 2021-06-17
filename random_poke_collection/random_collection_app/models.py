from django.db import models
import bcrypt
import re	# the regex module

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First name must be longer than 3 letters."
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last name must be longer than 3 letters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        email_check = self.filter(email=form['email']) # checks to make sure its unique
        if email_check:
            errors['email'] = "Email already in use"
        # password validation
        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors



    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            password = pw
    )

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    content = models.CharField(max_length=255)
    posted_to = models.ForeignKey(User, related_name='user_wall', on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    poke_id = models.IntegerField(unique=True)
    owners = models.ManyToManyField(User, related_name='user_pokemons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)