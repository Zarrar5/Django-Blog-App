from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import BlogPost, Comment
from django.contrib.auth import authenticate, login, logout
from .forms import BlogPostForm, CommentForm

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "myapp/user.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "myapp/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "myapp/login.html")

def logout_view(request):
    logout(request)
    return render(request, "myapp/login.html", {
        "message": "Logged out"
    })

def blog_posts(request):
    posts = BlogPost.objects.all().order_by('-date_posted')
    return render(request, 'myapp/blog_posts.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog_posts')
        
    else:
        form = BlogPostForm()
    return render(request, 'myapp/create_post.html', 
                  {'form': form}
                  )

def update_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('blog_posts')
        
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'myapp/update_post.html', 
                  {'form': form, 'post': post}
                  )

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.method == 'POST':
        post.delete()
        return redirect('blog_posts')
    
    return render(request, 'myapp/delete_post.html', {'post': post})


def like_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if request.user.is_authenticated:
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            post.likes_count += 1
            post.save()
        else:
            post.liked_by.remove(request.user)
            post.likes_count -= 1
            post.save()

    return redirect('blog_posts')


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
        
    return render(request, 'myapp/post_detail.html', 
                  {'post': post, 'comments': comments, 'comment_form': comment_form}
                  )