from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/', views.request_form, name='request_form'),
    path('swaps/', views.swap_requests, name='swap_requests'),
    path('profile/', views.profile_detail, name='profile_detail'),  # ✅ no <int:id>
]
