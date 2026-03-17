from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm


def community_home(request):
    posts = Post.objects.all()
    form = PostForm()
    comment_form = CommentForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request, "Your post was created successfully.")
                return redirect('community_home')
            else:
                messages.error(request, "There was a problem creating your post. Please check the form and try again.")
        else:
            messages.error(request, "You must be logged in to create a post.")
            return redirect('account_login')

    context = {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
    }

    return render(request, 'community/community_home.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post was updated successfully.")
            return redirect('community_home')
        else:
            messages.error(request, "There was a problem updating your post. Please check the form and try again.")
    else:
        form = PostForm(instance=post)

    return render(request, 'community/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Your post was deleted successfully.")
        return redirect('community_home')

    return render(request, 'community/delete_post.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
        else:
            messages.error(request, "There was a problem submitting your comment. Please try again.")

    return redirect('community_home')


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.approved = False
            comment.save()
            messages.success(request, "Your comment was updated and is awaiting approval.")
            return redirect('community_home')
        else:
            messages.error(request, "There was a problem updating your comment. Please try again.")
    else:
        form = CommentForm(instance=comment)

    return render(request, 'community/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Your comment was deleted successfully.")
        return redirect('community_home')

    return render(request, 'community/delete_comment.html', {'comment': comment})