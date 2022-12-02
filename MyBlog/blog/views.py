from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import News
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# def home(request):
#     data = {
#         'news': News.objects.all(),
#         'title': 'Главная страница',
#     }
#     return render(request, 'blog/home.html', data)
#
#
def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Страница контакты'})


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    # html context for jinja {{ news }}
    context_object_name = 'news'
    # sort
    ordering = ['-date']
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(ShowNewsView, self).get_context_data(**kwargs)
        ctx['title'] = 'MyBlog'
        return ctx


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(UserAllNewsView, self).get_context_data(**kwargs)
        ctx['title'] = f'@{self.kwargs.get("username")} - Blog'
        return ctx


class NewsDetailView(DetailView):
    model = News
    # default name for html = news-detail.html. Class news, DETAILview
    template_name = 'blog/news-detail.html'
    # default name for context_object_name = 'obj'
    context_object_name = 'el'


class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title', 'text']

    def get_context_data(self, **kwargs):
        ctx = super(CreateNewsView, self).get_context_data(**kwargs)

        ctx['title'] = 'Add News'
        ctx['btn_text'] = 'Publish the news'
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title', 'text']

    def get_context_data(self, **kwargs):
        ctx = super(UpdateNewsView, self).get_context_data(**kwargs)

        ctx['title'] = 'Update News'
        ctx['btn_text'] = 'Publish the updated news'
        return ctx

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = News
    success_url = '/'
    template_name = 'blog/delete-news.html'

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False
