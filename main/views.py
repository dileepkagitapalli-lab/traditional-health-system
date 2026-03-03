from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required


# ===================== HOME =====================
def home(request):
    return render(request, 'main/home.html')


# ===================== USER LOGIN =====================
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid user credentials")

    return render(request, 'main/user_login.html')


@login_required
def user_dashboard(request):
    return render(request, 'main/user_dashboard.html')


# ===================== CREATOR LOGIN =====================
def creator_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:
            login(request, user)
            return redirect('home')  # change if you have creator dashboard
        else:
            messages.error(request, "Invalid creator credentials")

    return render(request, 'main/creator_login.html')


# ===================== ADMIN LOGIN =====================
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        security_key = request.POST.get("security_key")

        user = authenticate(request, username=username, password=password)

        if (
            user is not None
            and user.is_superuser
            and security_key == settings.ADMIN_SECURITY_KEY
        ):
            login(request, user)
            return redirect('/admin/')  # Django default admin panel
        else:
            messages.error(request, "Invalid admin credentials or security key")

    return render(request, 'main/admin_login.html')


# ===================== LOGOUT =====================
def logout_view(request):
    logout(request)
    return redirect('home')


# ===================== STATIC PAGES =====================
def ayurveda(request):
    return render(request, 'main/ayurveda.html')


def yoga(request):
    return render(request, 'main/yoga.html')


def remedies(request):
    return render(request, 'main/remedies.html')


def food(request):
    return render(request, 'main/food.html')