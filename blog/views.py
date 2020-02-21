from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Blog, Comment
from django.http import Http404
from blog.forms import CommentForm


def get_blogs(request):
    ctx = {
        'blogs': Blog.objects.all().order_by('-created')
    }
    return render(request, 'blog_list.html', ctx)


def get_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()
        ctx = {
            'blog': blog,
            'comments': blog.comment_set.all().order_by('-created'),
            'form': form
        }
        return render(request, 'blog_detail.html', ctx)

    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)

        return redirect(reverse('blog_get_detail', kwargs={'blog_id': blog_id}))
