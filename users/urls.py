from django.urls import path
from .views import signup_view, login_view, logout_view
from .views import home_view
from .views import upload_profile_picture
from .views import HomeView

urlpatterns = [
    # path('', home_view, name='home'),
    path('', HomeView.as_view(), name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
]
