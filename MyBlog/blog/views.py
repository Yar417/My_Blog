from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from .forms import ContactForm
from .models import News, Contact
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError


# def home(request):
#     data = {
#         'news': News.objects.all(),
#         'title': 'Главная страница',
#     }
#     return render(request, 'blog/home.html', data)
#
#


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
    fields = ['title', 'img', 'text']

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

    fields = ['title', 'text', 'img']

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


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your message successfully posted!')
            # For sending messages to the owner of site or another e-mail
            try:
                subject = f'MyBlog. Theme: {form.cleaned_data["theme"]} '
                plain_message = f' Message: {form.cleaned_data["message"]}'
                from_email = f'From {form.cleaned_data["email"]}'
                to = 'mypost@gmail.com'
                send_mail(subject, plain_message, from_email, [to])
            except BadHeaderError:
                return print('Uncorrected')
        return redirect('home')

    else:
        form = ContactForm()
    return render(request, 'blog/contacts.html', {'title': 'Contact us', 'form': form})
