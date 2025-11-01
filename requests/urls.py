from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('reply/<int:request_id>/', views.request_reply, name='request_reply'),
    path('instructions/', views.instruction_list, name='instruction_list'),
]
