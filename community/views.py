from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm


def community_home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('community_home')
    else:
        form = PostForm()

    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'community/community_home.html', context)