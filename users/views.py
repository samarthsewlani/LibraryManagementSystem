from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import UpdateView,CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Profile



def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"Your account has been created.You are now able to Log In")
            return redirect('login')
        else:
        	print(form.cleaned_data)
        	print(form.errors)
        	print("Form invalid")
    else:
        print("New form created")
        form=UserRegistrationForm()
    return render(request,'users/register.html',{'form':form})


class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Profile
    fields=['image','email','address','contact']

    success_url='/'

    def test_func(self):
        profile=self.get_object()
        if profile.user==self.request.user:
            return True
        return False

