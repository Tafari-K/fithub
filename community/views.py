from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


def community_home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('community_home')
        else:
            return redirect('account_login')
    else:
        form = PostForm()

    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'community/community_home.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community_home')
    else:
        form = PostForm(instance=post)

    return render(request, 'community/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()
        return redirect('community_home')

    return render(request, 'community/delete_post.html', {'post': post})