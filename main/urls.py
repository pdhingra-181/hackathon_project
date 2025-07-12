from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-requests/', views.my_requests, name='my_requests'),  # 🔥 This line fixes your error
    path('login/', views.login_view, name='login'),
    path('profile/<int:id>/', views.profile_detail, name='profile_detail'),
    path('request/', views.request_form, name='request_form'),
    path('swaps/', views.swap_requests, name='swap_requests'),
    path('request/<int:profile_id>/', views.request_form, name='request_form'),
]

