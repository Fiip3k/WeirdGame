from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.utils.html import escape
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from game.models import Character


def login_view(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        password = escape(request.POST['password'])
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'mysite/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'mysite/login.html')


def register_view(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        password = escape(request.POST['password'])
        email = escape(request.POST['email'])
        if User.objects.filter(username=username).exists():
            return render(request, 'mysite/register.html', {'error': 'User already exists!'})
        else:
            try:
                user = User.objects.create_user(username, email, password)
                character = Character(
                    name=username, maxHealth=100, currentHealth=100, damage=10, user=user)
                user.save()
                character.save()
                return redirect('home')
            except:
                return render(request, 'mysite/register.html', {"error": "All fields are required!"})

    else:
        return render(request, 'mysite/register.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')


def reset_password(request):
    # DOESN'T WORK CAUSE EMAIL NOT CONFIGURED
    if request.method == 'POST':
        email = request.POST.get('email', None)
        # Generate reset token
        reset_token = get_random_string(length=32)
        # Save token in the database
        user = User.objects.get(email=email)
        user.reset_token = reset_token
        user.save()
        # Create unique URL
        reset_url = 'http://192.168.0.192:8000/new_password/{}'.format(
            reset_token)
        # Send URL to the user's email
        send_mail(
            'Password Reset Request',
            'Please click on the link {} to reset your password.'.format(
                reset_url),
            'noreply@example.com',  # create email
            [email],
            fail_silently=False,
        )
        return redirect('login')
    return render(request, 'mysite/reset_password.html')


def new_password(request, token):
    if request.method == 'POST':
        if request.user.reset_token == token:
            request.user.password = request.POST['password']
            request.user.reset_token = get_random_string(length=32)
            return redirect('login')
        else:
            return render(request, 'Wrong token!')
