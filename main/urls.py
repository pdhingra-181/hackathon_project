# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('swap-requests/', views.swap_requests, name='swap_requests'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/<int:profile_id>/request/', views.send_general_request, name='request_form'),
    path('general-requests/', views.general_swap_requests, name='general_swaps'),
    path('swap/<int:request_id>/action/', views.handle_swap_action, name='handle_swap_action'),
]
