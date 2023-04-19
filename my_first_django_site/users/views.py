from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView

# Create your views here.

class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):

        context = {'form': UserCreationForm()}
        
        return render(request, self.template_name, context)

    def post(self, request):

        form = UserCreationForm()

        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        
        context = {'form': form}
        
        return render(request, self.template_name, context)
    
# class PasswordResetView(PasswordResetView):
    
#     template_name = 'registration/password_reset_form.html'
#     context_object_name = 'password_reset'