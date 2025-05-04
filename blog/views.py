from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.db import connection
from contextlib import closing
from django.shortcuts import render
from django.contrib.auth.decorators import login_required




class HomeView(ListView):
    # Displays a list of all posts on the home page.
    # Requires the user to be logged in (via LoginRequiredMixin).
    # Uses the 'home.html' template to render the posts.
    # If the user is not logged in, redirects them to the login page with an error message.
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-id']
    def handle_no_permission(self):
        # Handles the case where the user is not logged in.
        messages.error(self.request, "You must be logged in to view this page.")
        return redirect('login')


class HomeOnlyView(ListView):
    # Displays a list of all posts on a different home page (e.g., 'Home2.html').
    # Does not require the user to be logged in.
    # Uses the 'Home2.html' template to render the posts.
    model = Post
    template_name = 'Home2.html'
    context_object_name = 'posts'
    ordering = ['added_at']

    def get_queryset(self):
        return Post.objects.all().order_by('added_at')


    def handle_no_permission(self):
        # Handles the case where the user is not logged in.
        messages.error(self.request, "You must be logged in to view this page.")
        return redirect('login')
    
   
class AboutViewWithoutLogin(TemplateView):
    # Displays the "About" page.
    # Requires the user to be logged in without login required
    # Uses the 'about.html' template to render the page.
    template_name = 'about2.html'

   

class AboutView(TemplateView):
    # Displays the "About" page.
    # Requires the user to be logged in (via LoginRequiredMixin).
    # Uses the 'about.html' template to render the page.
    template_name = 'about.html'

    def handle_no_permission(self):
        # Handles the case where the user is not logged in.
        # messages.error(self.request, "You must be logged in to view this page.")
        return redirect('blog-about')


class AddPostView(LoginRequiredMixin, CreateView):
    # Allows logged-in users to create a new blog post.
    # Uses the 'add_post.html' template to render the form.
    # Automatically assigns the logged-in user as the author of the post.
    # Redirects to the 'add-post' page after successfully creating the post.
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        # Sets the logged-in user as the author of the post and saves the form.
        with closing(connection.cursor()) as cursor:
            form.instance.author = self.request.user
            response = super().form_valid(form)
            messages.success(self.request, "Blog post created successfully!")
            cursor.close()
        return redirect(reverse('add-post'))

    def handle_no_permission(self):
        # Handles the case where the user is not logged in.
        messages.error(self.request, "You must be logged in to view this page.")
        return redirect('login')


class EditPostView(LoginRequiredMixin, UpdateView):
    # Allows logged-in users to edit an existing blog post.
    # Uses the 'edit_post.html' template to render the form.
    # Redirects to the home page after successfully editing the post.
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    success_url = reverse_lazy('blog-home')

    def form_valid(self, form):
        # Saves the edited post and displays a success message.
        try:    
            with closing(connection.cursor()) as cursor:
                response = super().form_valid(form)
                cursor.close()
                post = Post.objects.last()
                print(post.image.url)
                messages.success(self.request, "Blog post Edited successfully!")
            return response
        except Exception as e:
            print(e)
            
                        

    def handle_no_permission(self):
        # Handles the case where the user is not logged in.
        messages.error(self.request, "You must be logged in to view this page.")
        return redirect('login')


class DeletePostView(LoginRequiredMixin, DeleteView):
    # Allows logged-in users to delete a blog post.
    # Uses the 'confirm_delete.html' template to confirm the deletion.
    # Redirects to the home page after successfully deleting the post.
    model = Post
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('blog-home')

    def delete(self, request, *args, **kwargs):
        # Checks if the logged-in user is the author of the post before deleting it.
        post = self.get_object()
        if post.author != request.user:
            # If the user is not the author, display an error message and redirect to the home page.
            messages.error(request, "You are not authorized to delete this post.")
            return redirect('blog-home')
        # If the user is the author, delete the post and display a success message.
        messages.success(request, f"The post '{post.title}' has been successfully deleted.")
        return super().delete(request, *args, **kwargs)
    
