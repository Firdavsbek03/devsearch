from django.urls import path
from .views import get_project,get_projects,create_project,update_project,delete_project

urlpatterns=[
    path("",get_projects,name='projects'),
    path("project/<str:pk>/",get_project,name='project'),
    path("create-project/",create_project,name='create_project'),
    path('update-project/<str:pk>/',update_project,name='update_project'),
    path('delete-project/<str:pk>/',delete_project,name='delete_project'),
]