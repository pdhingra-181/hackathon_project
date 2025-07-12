from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'main/home.html')

def my_requests(request):
    return render(request, 'main/my_requests.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home on successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'main/login.html')

from django.contrib.auth.models import User

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')

    return render(request, 'main/signup.html')


from django.contrib.auth.decorators import login_required

@login_required
def profile_detail(request):
    return render(request, 'main/profile_detail.html', {
        'user_data': request.user
    })


def swap_requests(request):
    swaps = [
        {
            'to': 'John Doe',
            'offer': 'Python Tutoring',
            'want': 'Public Speaking Practice',
            'date': 'July 12, 2025',
            'status': 'Pending',
        },
        {
            'to': 'Jane Smith',
            'offer': 'Video Editing',
            'want': 'UI/UX Design',
            'date': 'July 10, 2025',
            'status': 'Accepted',
        },
    ]
    return render(request, 'main/swap_requests.html', {'swaps': swaps})

def request_form(request):
    if request.method == 'POST':
        offer = request.POST.get('offer')
        want = request.POST.get('want')
        message = request.POST.get('message')
        # You can save this data to your model here if needed
        return render(request, 'main/request_form.html', {'success': True})
    return render(request, 'main/request_form.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')
