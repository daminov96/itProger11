from abc import ABC
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import (
        ListView,
        DetailView,
        CreateView,
        UpdateView,
        DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import News


def home(request):
    data = {
        "news": News.objects.all(),
        "title": "Blog home page",
    }
    return render(request, 'blog/home.html', data)


class UpdateNewsView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False


class ShowNewsView(ListView):
    model = News
    template_name = "blog/home.html"
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        ctx = super(ShowNewsView, self).get_context_data(**kwargs)
        ctx['title'] = "Blog home page"
        return ctx


class UserAllNewsView(ListView):
    model = News
    template_name = "blog/user_news.html"
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(avtor=user).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super(UserAllNewsView, self).get_context_data(**kwargs)
        ctx['title'] = f'All articles from the user {self.kwargs.get("username")}'
        return ctx

class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        ctx = super(NewsDetailView, self).get_context_data(**kwargs)
        ctx['title'] = News.objects.filter(pk=self.kwargs['pk']).first()
        return ctx


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        return False


class CreateNewsView(CreateView, LoginRequiredMixin, UserPassesTestMixin, ABC):
    model = News
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)


def contact(request):
    return render(request, "blog/contact.html", {"title": "page about us"})


