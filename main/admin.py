from django.contrib import admin
from .models import Profile, Post, Like, SavedContent

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'creator', 'status', 'created_at')
    list_filter = ('category', 'status')
    search_fields = ('title', 'content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')

@admin.register(SavedContent)
class SavedContentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
