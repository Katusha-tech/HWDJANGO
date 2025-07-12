from django.shortcuts import render
from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView

class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
