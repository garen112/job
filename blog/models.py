from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utilities import email_subscriber


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название блога')
    description = models.TextField(verbose_name='Описание блога')
    author = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    sub = models.ManyToManyField(User, related_name='sub', blank=True, symmetrical=False,
                                 verbose_name='Подписчики блога')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    def save(self):
        super(Blog, self).save()
        if not self.slug:
            self.slug = slugify(self.title)
            super(Blog, self).save()

    class Meta:
        verbose_name = 'Блог пользователя'
        verbose_name_plural = 'Блоги пользователей'


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    blog = models.ForeignKey(Blog, verbose_name='Посты блога', on_delete=models.CASCADE)
    read = models.ManyToManyField(User, blank=True, verbose_name='Прочитано', related_name='read')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-created_at']

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        blog_title = instance.title
        post_url = 'http://127.0.0.1:8000/posts/%s' % instance.pk
        user_emails = instance.blog.sub.values_list(
            'email', flat=True)
        for email in user_emails:
            email_subscriber(email, blog_title, post_url)