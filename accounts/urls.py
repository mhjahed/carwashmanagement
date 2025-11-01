from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('signup/employer/', views.employer_signup, name='employer_signup'),
    path('signup/author/', views.author_signup, name='author_signup'),
    path('logout/', views.logout_view, name='logout'),
]
