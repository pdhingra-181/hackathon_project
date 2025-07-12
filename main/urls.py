from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-requests/', views.my_requests, name='my_requests'),  # 🔥 This line fixes your error
    path('login/', views.login_view, name='login'),
]
