from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def user_login(request):
    return render(request, 'main/user_login.html')

def creator_login(request):
    return render(request, 'main/creator_login.html')

def admin_login(request):
    return render(request, 'main/admin_login.html')

def ayurveda(request):
    return render(request, 'main/ayurveda.html')

def yoga(request):
    return render(request, 'main/yoga.html')

def remedies(request):
    return render(request, 'main/remedies.html')
