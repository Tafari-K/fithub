from django.shortcuts import render
from .models import Post

def community_home(request):
    posts = Post.objects.all()
    return render(request, 'community/community_home.html', {'posts': posts})