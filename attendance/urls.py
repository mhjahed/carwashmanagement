from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/create/', views.note_create, name='note_create'),
]
