from django.urls import path
from .views import RegisterView, UserListView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.decorators import api_view
from rest_framework.response import Response

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('users/', UserListView.as_view(), name='user-list'),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('me/', UserProfileView.as_view(), name='user-profile'),
# ]

@api_view(['GET'])
def accounts_root(request, format=None):
    return Response({
        "register": request.build_absolute_uri('register/'),
        "users": request.build_absolute_uri('users/'),
        "token_obtain_pair": request.build_absolute_uri('token/'),
        "token_refresh": request.build_absolute_uri('token/refresh/'),
        "profile": request.build_absolute_uri('me/'),
    })

urlpatterns = [
    path('', accounts_root, name='accounts-root'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]