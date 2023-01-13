from django.urls import path
from .views import get_routes,get_projects,get_project,vote_project,removeTag
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',get_routes),
    path("projects/",get_projects),
    path("projects/<str:pk>/",get_project),
    path("projects/<str:pk>/vote/",vote_project),
    path('remove-tag/',removeTag),
]