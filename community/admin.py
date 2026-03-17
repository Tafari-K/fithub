from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    actions = ['approved_comments']

    def approved_comments(self, request, queryset):
        queryset.update(approved=True)

    approved_comments.short_description = "Approved selected comments"