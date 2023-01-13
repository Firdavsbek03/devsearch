from django.urls import path
from .views import (
    get_profiles,
    get_profile,
    login_user,
    logout_user,
    register_user,
    user_account,
    edit_account,
    update_skill,
    create_skill,
    delete_skill,
    inbox,
    view_message,
    create_message,
)

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path("", get_profiles, name='profiles'),
    path("profile/<str:pk>/", get_profile, name='user_profile'),
    path("account/", user_account, name='account'),
    path("edit-account/", edit_account, name='edit-account'),
    path("create-skill/",create_skill,name='create-skill'),
    path("edit-skill/<str:pk>/",update_skill,name='edit-skill'),
    path("delete-skill/<str:pk>/",delete_skill,name='delete-skill'),
    path('inbox/',inbox,name='inbox'),
    path('message/<str:pk>/',view_message,name='message'),
    path('create-message/<str:pk>/',create_message,name='create-message'),
]
