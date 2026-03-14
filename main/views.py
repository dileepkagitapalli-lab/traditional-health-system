from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from .models import Profile, Post, Like, SavedContent
from .forms import UserRegistrationForm, CreatorRegistrationForm, PostForm

# ================= HOME & PUBLIC VIEWS =================
def home(request):
    featured_posts = Post.objects.filter(status='approved').order_by('-created_at')[:6]
    context = {'featured_posts': featured_posts}
    return render(request, 'main/home.html', context)

# ================= AUTHENTICATION VIEWS =================
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, role='user') # Automatically create Profile
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/user_login.html', {'register_form': form})

def creator_register(request):
    if request.method == 'POST':
        form = CreatorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, role='creator')
            messages.success(request, 'Creator Registration successful. You can now log in.')
            return redirect('creator_login')
    else:
        form = CreatorRegistrationForm()
    return render(request, 'main/creator_login.html', {'register_form': form})

def admin_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        security_key = request.POST.get("security_key")
        
        if security_key != settings.ADMIN_SECURITY_KEY:
            messages.error(request, 'Invalid Admin Security Key.')
            return render(request, 'main/admin_register.html', {'register_form': form})
            
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = True
            user.is_staff = True
            user.save()
            Profile.objects.create(user=user, role='admin')
            messages.success(request, 'Admin Registration successful. You can now log in.')
            return redirect('admin_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/admin_register.html', {'register_form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:
            if hasattr(user, 'profile') and user.profile.role == 'user':
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, "Please use the creator login page for creator accounts.")
        else:
            messages.error(request, "Invalid user credentials")

    return render(request, 'main/user_login.html', {'login_form_active': True})

def creator_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:
            if hasattr(user, 'profile') and user.profile.role == 'creator':
                login(request, user)
                return redirect('creator_dashboard')
            else:
                 messages.error(request, "Please use the user login page for regular user accounts.")
        else:
            messages.error(request, "Invalid creator credentials")

    return render(request, 'main/creator_login.html', {'login_form_active': True})

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
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials or security key")

    return render(request, 'main/admin_login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# ================= DASHBOARD VIEWS =================
@login_required
def user_dashboard(request):
    # Only users. Default to admin dashboard if they are superuser.
    if getattr(request.user, 'is_superuser', False):
        return redirect('admin_dashboard')
    
    if getattr(request.user, 'profile', None) and request.user.profile.role != 'user':
         return redirect('home')

    liked_posts = Like.objects.filter(user=request.user).select_related('post')
    saved_posts = SavedContent.objects.filter(user=request.user).select_related('post')

    context = {
        'liked_posts': [like.post for like in liked_posts],
        'saved_posts': [save.post for save in saved_posts]
    }
    return render(request, 'main/user_dashboard.html', context)


@login_required
def creator_dashboard(request):
    if getattr(request.user, 'is_superuser', False):
        return redirect('admin_dashboard')
        
    if getattr(request.user, 'profile', None) and request.user.profile.role != 'creator':
         return redirect('home')

    my_posts = Post.objects.filter(creator=request.user).order_by('-created_at')
    
    context = {
        'my_posts': my_posts,
    }
    return render(request, 'main/creator_dashboard.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    total_users = Profile.objects.filter(role='user').count()
    total_creators = Profile.objects.filter(role='creator').count()
    total_posts = Post.objects.count()
    pending_posts = Post.objects.filter(status='pending').order_by('-created_at')
    approved_posts = Post.objects.filter(status='approved').order_by('-created_at')

    context = {
        'total_users': total_users,
        'total_creators': total_creators,
        'total_posts': total_posts,
        'pending_posts': pending_posts,
        'approved_posts': approved_posts
    }

    return render(request, 'main/admin_dashboard.html', context)

# ================= ACTION VIEWS =================
@login_required
def create_post(request):
    if getattr(request.user, 'is_superuser', False) or (hasattr(request.user, 'profile') and request.user.profile.role != 'creator'):
        messages.error(request, "Only creators can create posts.")
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            messages.success(request, 'Post submitted for approval!')
            return redirect('creator_dashboard')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form': form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete() # Toggle like
        messages.info(request, "Post unliked.")
    else:
        messages.success(request, "Post liked!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved, created = SavedContent.objects.get_or_create(user=request.user, post=post)
    if not created:
         saved.delete() # Toggle save
         messages.info(request, "Post removed from saved content.")
    else:
         messages.success(request, "Post saved to your dashboard!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def approve_post(request, post_id):
    if not getattr(request.user, 'is_superuser', False):
         return redirect('home')
    post = get_object_or_404(Post, id=post_id)
    post.status = 'approved'
    post.save()
    messages.success(request, f"Post '{post.title}' approved.")
    return redirect('admin_dashboard')

@login_required
def reject_post(request, post_id):
    if not getattr(request.user, 'is_superuser', False):
         return redirect('home')
    post = get_object_or_404(Post, id=post_id)
    post.status = 'rejected'
    post.save()
    messages.warning(request, f"Post '{post.title}' rejected.")
    return redirect('admin_dashboard')


# ================= CATEGORY PAGES =================
def ayurveda(request):
    posts = Post.objects.filter(status='approved', category='ayurveda').order_by('-created_at')
    return render(request, 'main/ayurveda.html', {'posts': posts})

def yoga(request):
    posts = Post.objects.filter(status='approved', category='yoga').order_by('-created_at')
    return render(request, 'main/yoga.html', {'posts': posts})

def remedies(request):
    posts = Post.objects.filter(status='approved', category='remedies').order_by('-created_at')
    return render(request, 'main/remedies.html', {'posts': posts})

def food(request):
    posts = Post.objects.filter(status='approved', category='foods').order_by('-created_at')
    return render(request, 'main/food.html', {'posts': posts})
