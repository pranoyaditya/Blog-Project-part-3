from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .forms import PostForm
from .models import Post


# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('homePage')
    else:
        post_form = PostForm()
    return render(request, 'posts/postPage.html', {'form': post_form})

# Add post using class based view.
class AddPostCreateView(LoginRequiredMixin, CreateView):
    model = Post # model to work with.
    form_class = PostForm # form to work with.
    template_name = 'posts/postPage.html' # which template to render.
    success_url = reverse_lazy('homePage') # redirects to the url.

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
    

@login_required
def edit_post(request,id):
    post = Post.objects.get(pk=id)
    post_form = PostForm(instance=post)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('homePage')
    return render(request, 'posts/postPage.html', {'form': post_form})

@login_required
def delete_post(reuqest, id):
    post = Post.objects.get(pk = id)
    post.delete()
    return redirect('homePage')
