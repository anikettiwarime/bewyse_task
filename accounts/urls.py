from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/view/', views.ViewProfile.as_view(), name='profile'),
    path('profile/edit/', views.update_profile, name='edit-profile'),
    # path('profile/edit/', views.EditProfile.as_view(), name='edit-profile'),

]
