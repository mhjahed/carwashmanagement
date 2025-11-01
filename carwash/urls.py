from django.urls import path
from . import views

app_name = 'carwash'

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.ticket_create, name='ticket_create'),
    path('preview/<int:ticket_id>/', views.ticket_preview, name='ticket_preview'),
    path('update/<int:ticket_id>/', views.ticket_update, name='ticket_update'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/update/<int:customer_id>/', views.customer_update, name='customer_update'),
    path('get-service-price/', views.get_service_price, name='get_service_price'),
]
