from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm
from django.contrib.auth.models import Group  # Import Group for role assignment
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.models import User







from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
import re  # For email format validation

def register(request):
    '''This method is used to register the new user in the database'''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Validate email format (optional, if not already handled by the form)
            email = request.POST.get('email', '')
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messages.error(request, '❌ Invalid email format.')
                return render(request, 'users/register.html', {'form': form})

            # Save the user if everything is valid
            user = form.save()
            messages.success(request, '✅ Account created successfully!')
            return redirect('login')
        else:
            # Collect form errors and display them as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {field.capitalize()}: {error}")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})



# logintrack=True
class SignInView(LoginView):
    template_name = 'users/login.html'  # Specify the login template
    authentication_form = LoginForm  # Use the custom LoginForm
    # success_url = reverse_lazy("login")
    # def dispatch(self, request, *args, **kwargs):
    #     # Redirect authenticated users to the home page
    #     if request.user.is_authenticated:
    #         messages.info(request, "You are already logged in.")
    #         return redirect('blog-home')  # Redirect to the home page
    #     return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
            username = self.request.POST.get('username', '').strip()
            password = self.request.POST.get('password', '').strip()

            if not username:
                messages.error(self.request, "❌ Username field cannot be empty.")
            elif not password:
                messages.error(self.request, "❌ Password field cannot be empty.")
            else:
                messages.error(self.request, "❌ Invalid username or password.")
            return super().form_invalid(form)

    def form_valid(self, form):
        # Add a success message upon successful login
        print('form valid')
        messages.success(self.request, f"Hi {form.get_user().username.title()}, welcome back!")
        return super().form_valid(form)


class SignOutView(LogoutView):
    logintrack=True
    next_page = 'login'  # Redirect to the login page after logout

    def get(self, request, *args, **kwargs):
        # Handle logout via GET request
        if request.user.is_authenticated:
            logintrack=True
            messages.success(request, "You have been logged out successfully.")
            
        else:
            messages.error(request, "You are not logged in.")
        return super().dispatch(request, *args, **kwargs)  # Call dispatch to handle logout
    
