from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, PostCommentForm
from .models import Post, Comment


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {
        'posts': posts
    })


def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    count_comments = len(comments)

    if request.method == 'POST':
        comment_form = PostCommentForm(request.POST)
        try:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.save()
                return redirect('posts:post-details', slug=slug)
        except ValueError:
            return redirect('/accounts/login/')
    else:
        comment_form = PostCommentForm()

    return render(request, 'post_details.html', {
        'post': post,
        'comments': comments,
        'count_comments': count_comments,
        'form': comment_form
    })


def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        try:
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                if new_post.author.is_staff or new_post.author.is_superuser:
                    messages.success(request, "Your post added successfully")
                    new_post.moderation_status = 'Approve'
                    new_post.save()
                else:
                    messages.success(request, "Your post added and waiting for moderation")
                return redirect('posts:posts')
        except ValueError:
            return redirect('/accounts/login/')
    else:
        post_form = PostForm()

    return render(request, 'post_create.html', {
        'form': post_form
    })
