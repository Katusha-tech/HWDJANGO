from .models import Post, Comment, Category, Tag
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

#@method_decorator(cache_page(60 *1), name='get') # Кешируем страницу на 1 минуту
class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    # Оптимизируем запрос - сделаем жадный запрос Категории теги комменты расширение метода get_queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('category', 'author')
        queryset = queryset.prefetch_related('tags', 'comments')
        return queryset



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'