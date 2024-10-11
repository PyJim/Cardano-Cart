from django.urls import path
from .views import AllUsersView, RegisterView, LoginView, UserProfileView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:id>/', UserProfileView.as_view(), name='user_profile'),
    path('', AllUsersView.as_view(), name='all_users'),
    path('me/', CurrentUserView.as_view(), name='current-user'),  # New endpoint for current user

]
