from django.urls import path, include
from django.contrib.auth.decorators import login_required


from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.BlogListView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('blog/<slug:slug>/', login_required(views.BlogDetailView.as_view()), name='blog_detail'),
    path('blog/add/', views.BlogCreate.as_view(), name='blog_form'),
    path('re/<int:pk>/sub', views.SubView.as_view(), name='sub'),
    path('re/<int:pk>/unsub', views.UnSubView.as_view(), name='unsub'),
    path('ri/<int:pk>/read', views.ReadView.as_view(), name='read'),
    path('feed/', views.PostFeedView.as_view(), name='post_list'),
]
