from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .models import Blog, Post


class BlogCreate(LoginRequiredMixin, generic.CreateView):
    """"Создание блога, если блог есть, то HttpResponse"""
    model = Blog
    fields = ['title', 'description']
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            return super().form_valid(form)
        except IntegrityError:
            return HttpResponse('У вас уже есть блог, больше нельзя')


class BlogListView(generic.ListView):
    """"Список блогов"""
    model = Blog
    context_object_name = 'blogs'
    template_name = 'index.html'
    paginate_by = 10


class BlogDetailView(generic.DetailView):
    """"Просмотр блога с постами """
    model = Blog
    context_object_name = 'blogs'
    slug_url_kwarg = 'slug'
    template_name = 'blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(blog__slug=self.kwargs['slug'])
        return context


class PostDetailView(generic.DetailView):
    """"Детальный просмотр постов"""
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'


class SubView(generic.CreateView):
    """"Подписка"""
    def post(self, request, *args, **kwargs):
        user = request.user
        blog = get_object_or_404(Blog, pk=kwargs.get('pk'))
        if not blog.sub.filter(pk=user.pk).exists():
            blog.sub.add(user)
        return render(request, 'help.html')


class UnSubView(generic.CreateView):
    """"Отписка"""
    def post(self, request, *args, **kwargs):
        user = request.user
        blog = get_object_or_404(Blog, pk=kwargs.get('pk'))
        if blog.sub.filter(pk=user.pk).exists():
            blog.sub.remove(user)
        return render(request, 'help.html')


class PostFeedView(generic.ListView):
    """"Моя лента"""
    model = Post
    context_object_name = 'posts'
    template_name = 'post_list.html'

    def get_queryset(self):
        return Post.objects.filter(blog__sub__in=[self.request.user])


class ReadView(generic.CreateView):
    """"Метка о прочтении"""
    def post(self, request, *args, **kwargs):
        user = request.user
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        if not post.read.filter(pk=user.pk).exists():
            post.read.add(user)
        return render(request, 'help.html')
