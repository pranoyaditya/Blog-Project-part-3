from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import PostForm, CommentForm
from .models import Post


# Create your views here.

# Add post using class based view.
class AddPostCreateView(LoginRequiredMixin, CreateView):
    model = Post # model to work with.
    form_class = PostForm # form to work with.
    template_name = 'posts/postPage.html' # which template to render.
    success_url = reverse_lazy('profile') # redirects to the url.

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    
# Edit post using class based view.
class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/postPage.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile') 

# Delete post using class based view.
class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/deletePost.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

# Detail post view using class based view.
class DetailPostView(DetailView):
    model = Post
    template_name = 'posts/detailPostView.html'
    pk_url_kwarg = 'id'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments.all()
        comment_form = CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        
        return context