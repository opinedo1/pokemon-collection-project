from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('users', views.users),
    path('user/<int:user_id>', views.user_wall),
    path('edit/<int:id>', views.edit),
    path('post_content/<int:wall_id>', views.post_content),
    path('post_liked/<int:post_id>', views.post_liked),
    path('add_comment/<int:post_id>', views.add_comment),
    path('delete_comment/<int:comment_id>', views.delete_comment),
    path('collect_pokemon', views.get_random_pokemon),
    path('pokemon/<int:id>', views.view_pokemon)
]