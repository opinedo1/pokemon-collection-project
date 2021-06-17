from django.shortcuts import render
import requests, json, random

# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Post, Comment, Pokemon
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        this_user = User.objects.register(request.POST)
        request.session['user_id'] = this_user.id
        messages.success(request, "Registration successful!")
        return redirect('/success')
    
def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    request.session['logged_user_name'] = user.first_name
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': this_user,
        'posts': this_user.user_posts.all,
        'comments':this_user.user_comments.all,
        'pokemons': this_user.user_pokemons.all
    }
    return render(request, 'success.html', context)



def collect_pokemon(request):
    return redirect('/wall')

def user_wall(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=user_id)
    context = {
        'user': this_user,
        'posts': Post.objects.filter(posted_to=User.objects.get(id=user_id)),
        'pokemons': this_user.user_pokemons.all
    }
    return render(request, 'wall.html', context)

def post_content(request, wall_id):
    this_user_id = request.session['user_id']
    Post.objects.create(content=request.POST['content'], posted_by=User.objects.get(id=this_user_id), posted_to=User.objects.get(id=wall_id))
    return redirect('/user/{id}'.format(id=wall_id))

def post_liked(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    this_user = User.objects.get(id=request.session['user_id'])
    liked_post.user_likes.add(this_user)
    wall_id = Post.objects.get(id=post_id).posted_to.id
    return redirect('/user/{id}'.format(id=wall_id))

def add_comment(request, post_id):
    this_user_id = request.session['user_id']
    Comment.objects.create(content=request.POST['content'], user=User.objects.get(id=this_user_id), post=Post.objects.get(id=post_id))
    wall_id = Post.objects.get(id=post_id).posted_to.id
    return redirect('/user/{id}'.format(id=wall_id))

def delete_comment(request, comment_id):
    post_id = Comment.objects.get(id=comment_id).post.id
    wall_id = Post.objects.get(id=post_id).posted_to.id
    comment_to_delete = Comment.objects.get(id=comment_id)
    comment_to_delete.delete()
    return redirect('/user/{id}'.format(id=wall_id))

def users(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'users.html', context)

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')

def get_random_pokemon(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    random_id = random.randrange(1,898)
    print("Random number: " + str(random_id))
    response = requests.get('https://pokeapi.co/api/v2/pokemon/{id}/'.format(id=random_id))
    data = response.json()
    pokemon_name = data['name'].capitalize()
    this_poke_id = data['id']
    sprites_data = data['sprites']
    this_src = sprites_data['front_default']
    print(str(this_src))
    print("Pokemon name: " + pokemon_name)
    print(Pokemon.objects.filter(poke_id=this_poke_id))
    # if pokemon is unique add it to our database
    if not Pokemon.objects.filter(poke_id=this_poke_id):
        Pokemon.objects.create(name=pokemon_name, poke_id=this_poke_id, src=this_src)
    pokemon_captured = Pokemon.objects.get(poke_id=this_poke_id)
    # assign our pokemon to a user
    pokemon_captured.owners.add(this_user)
    return redirect('/success')

def view_pokemon(request, id):
    context = {
        'current': Pokemon.objects.get(id=id),
        'pokemons': Pokemon.objects.all()
    }
    return render(request, 'pokemon.html', context)