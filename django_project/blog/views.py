from django.shortcuts import render, get_object_or_404,  redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)
from .models import *
from django.template.defaultfilters import slugify


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

def PostDetailView(request, id):
    post = Post.objects.get(id = id)
    user = request.user
    like_toll = False
    if Like.objects.filter(user = user, post =post).exists():
        like_toll =True
    like_count = Like.objects.filter(post = post).count()
    print(like_toll)
    return render(request, 'blog/post_detail.html', {'object': post, 'like_toll':like_toll, 'like_count':like_count})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def edit_like(request, id):
    try:
        post = get_object_or_404(Post, pk=id)
    except:
        return HttpResponse("Such id does not exist")
    user = request.user
    if Like.objects.filter(post = post, user = user).exists():
        like = Like.objects.get(post = post, user = user)
        like.delete()
    else:
        like = Like.objects.create(post = post, user =user)
        like.save()
    return HttpResponseRedirect(reverse('post-detail', args=(post.id, )))

