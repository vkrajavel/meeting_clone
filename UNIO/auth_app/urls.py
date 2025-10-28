from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    RefreshView,
    GoogleLoginView,
    MicrosoftLoginView
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('microsoft/', MicrosoftLoginView.as_view(), name='microsoft_login'),
]