from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        return validate_form_post(request, form)

    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        return validate_form_post(request, form)

    form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def validate_form_post(request, form):
    if form.is_valid():
        post = save_form(request, form)
        return redirect('post_detail', pk=post.pk)

def save_form(request, form):
    post = form.save(commit=False)
    post.author = request.user
    post.published_date = timezone.now()
    post.save()

    return post
