from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import SkillProfile
from django.db.models import Q

def home(request):
    search_query = request.GET.get('search', '').strip()
    availability_filter = request.GET.get('availability', '').strip()

    # Base query: only public profiles
    profiles = SkillProfile.objects.filter(is_public=True).order_by('name')

    # Apply search filter on skills offered and wanted
    if search_query:
        profiles = profiles.filter(
            Q(skills_offered__icontains=search_query) |
            Q(skills_wanted__icontains=search_query)
        )

    # Apply availability filter
    if availability_filter:
        profiles = profiles.filter(availability__iexact=availability_filter)

    # Convert skills from comma-separated string to lists
    for profile in profiles:
        profile.skills_offered = [s.strip() for s in profile.skills_offered.split(',') if s.strip()]
        profile.skills_wanted = [s.strip() for s in profile.skills_wanted.split(',') if s.strip()]

    # Pagination
    paginator = Paginator(profiles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'users': page_obj,
        'search_query': search_query,
        'availability_filter': availability_filter,
    }

    return render(request, 'main/home.html', context)


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

def profile_detail(request, id=None):
    user_data = {
        'name': 'John Doe',
        'location': 'Delhi',
        'photo': 'main/default-profile.png',
        'skills_offered': ['Python Programming', 'Video Editing'],
        'skills_wanted': ['UI/UX Design', 'Public Speaking'],
        'availability': 'Weekends & Evenings',
    }
    return render(request, 'main/profile_detail.html', {'user_data': user_data})


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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import SkillProfile, SkillSwapRequest

@login_required
def request_form(request, profile_id):
    receiver_profile = get_object_or_404(SkillProfile, id=profile_id, is_public=True)
    sender_profile = get_object_or_404(SkillProfile, user=request.user)

    if request.method == 'POST':
        skill_offered = request.POST.get('skill_offered')
        skill_requested = request.POST.get('skill_requested')
        message = request.POST.get('message', '')

        SkillSwapRequest.objects.create(
            sender=request.user,
            receiver=receiver_profile.user,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            message=message
        )
        return render(request, 'main/request_form.html', {
            'success': True,
            'receiver': receiver_profile,
            'offered_skills': sender_profile.skills_offered,
            'requested_skills': receiver_profile.skills_wanted
        })

    return render(request, 'main/request_form.html', {
        'receiver': receiver_profile,
        'offered_skills': sender_profile.skills_offered,
        'requested_skills': receiver_profile.skills_wanted
    })
