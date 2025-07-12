# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import SkillProfile, SkillSwapRequest


@login_required
def home(request):
    search_query = request.GET.get('search', '').strip()
    availability_filter = request.GET.get('availability', '').strip()

    profiles = SkillProfile.objects.filter(is_public=True).exclude(user=request.user).order_by('name')

    if search_query:
        profiles = profiles.filter(
            Q(skills_offered__icontains=search_query) |
            Q(skills_wanted__icontains=search_query)
        )

    if availability_filter:
        profiles = profiles.filter(availability__iexact=availability_filter)

    paginator = Paginator(profiles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_swaps = SkillSwapRequest.objects.filter(
        allow_general=True,
        receiver__isnull=True
    ).exclude(sender=request.user).order_by('-created_at')[:5]

    context = {
        'users': page_obj,
        'search_query': search_query,
        'availability_filter': availability_filter,
        'recent_swaps': recent_swaps,
    }
    return render(request, 'main/home.html', context)


@login_required
def profile_detail(request):
    profile, created = SkillProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'availability': 'Weekends',
            'skills_offered': ["Python"],
            'skills_wanted': ["Design"],
        }
    )

    return render(request, 'main/profile_detail.html', {
        'user_data': request.user,
        'profile': profile,
    })


@login_required
def my_requests(request):
    swaps = SkillSwapRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')
    return render(request, 'main/my_requests.html', {'swaps': swaps})


@login_required
def swap_requests(request):
    swaps = SkillSwapRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')
    return render(request, 'main/swap_requests.html', {'swaps': swaps})


@login_required
def general_swap_requests(request):
    swaps = SkillSwapRequest.objects.filter(
        receiver__isnull=True,
        status='Pending'
    ).exclude(sender=request.user).order_by('-created_at')
    return render(request, 'main/general_swaps.html', {'swaps': swaps})


@require_POST
@login_required
def handle_swap_action(request, request_id):
    swap_request = get_object_or_404(SkillSwapRequest, id=request_id)
    action = request.POST.get('action')

    # First assign receiver if it's general
    if swap_request.receiver is None:
        swap_request.receiver = request.user

    # Permission check
    if swap_request.receiver != request.user:
        messages.error(request, "You are not authorized to respond to this request.")
        return redirect('swap_requests')

    if action == 'accept':
        swap_request.status = 'Accepted'
        messages.success(request, "Swap request accepted.")
    elif action == 'reject':
        swap_request.status = 'Rejected'
        messages.success(request, "Swap request rejected.")
    else:
        messages.error(request, "Invalid action.")

    swap_request.save()
    return redirect('swap_requests')


@login_required
def send_general_request(request, profile_id):
    receiver_profile = get_object_or_404(SkillProfile, id=profile_id, is_public=True)
    sender_profile = get_object_or_404(SkillProfile, user=request.user)

    offered_skills = sender_profile.skills_offered or ["Python", "Java", "Video Editing"]
    requested_skills = receiver_profile.skills_wanted or ["UI/UX", "Photography", "ML"]

    if request.method == 'POST':
        skill_offered = request.POST.get('skill_offered')
        skill_requested = request.POST.get('skill_requested')
        message = request.POST.get('message', '').strip()

        SkillSwapRequest.objects.create(
            sender=request.user,
            receiver=None,
            skill_offered=skill_offered,
            skill_requested=skill_requested,
            message=message,
            allow_general=True
        )

        return render(request, 'main/request_form.html', {
            'success': True,
            'receiver': receiver_profile,
            'offered_skills': offered_skills,
            'requested_skills': requested_skills,
        })

    return render(request, 'main/request_form.html', {
        'receiver': receiver_profile,
        'offered_skills': offered_skills,
        'requested_skills': requested_skills,
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'main/login.html')


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
            SkillProfile.objects.create(user=user, name=username, availability="Weekends")
            login(request, user)
            return redirect('home')
    return render(request, 'main/signup.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
