from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from .forms import UserRegistrationForm, LoginForm, UserEditForm, ProfileEditForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile

class Login(View):
  def get(self, request):
    login_form = LoginForm()
    return render(request, "users/login.html", {'login_form':login_form})

  def post(self, request):
    form = LoginForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None :
            login(request, user)
            messages.success(request, f"{data['username']}, You have successfully logged in!")
            #return redirect('index')
            next_url = request.GET.get("next")
            return redirect(next_url) if next_url else redirect('index')
        else :
            messages.warning(request, "Invalid username or password.")
            return redirect('login')

class Logout(View):
   def get(self, request):            
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index")

class Register_user(View):
  def get(self, request):
    user_form = UserRegistrationForm()
    return render(request, "users/register_user.html", {'user_form':user_form})

  def post(self, request):
    user_form = UserRegistrationForm(request.POST)
    if user_form.is_valid():
      new_user = user_form.save()
      Profile.objects.create(user=new_user)
      messages.success(request, f"{user_form['username'].value()}, You have successfully registered!")
      return redirect("index")
    else:
      return render(request, 'users/register_user.html', {'user_form':user_form})            


class Edit_User(View):
  def post(self, request):
      user_form = UserEditForm(instance=request.user, data=request.POST)
      profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
      if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('edit_user')

      else:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'users/edit_user.html', {'user_form':user_form, 'profile_form':profile_form, 'profile_image': profile.image})  

  def get(self, request):
      user_form = UserEditForm(instance=request.user)
      profile = Profile.objects.get(user=request.user)
      return render(request, 'users/edit_user.html', {'user_form':user_form, 'profile_image':profile.image})  

class DeleteUserView(View):
  def get(self, request):
    user = request.user  
    logout(request)  
    user.delete()  
    messages.success(request, f"User {user} has been deleted")
    return redirect("index")  
  
class CustomPasswordChangeView(PasswordChangeView):
  form_class = CustomPasswordChangeForm  
  template_name = 'users/password_change.html'
  success_url = reverse_lazy('edit_user')  

  def form_valid(self, form):
      """Override form_valid to add a success message before redirecting"""
      messages.success(self.request, "Your password has been changed successfully!")
      return super().form_valid(form)
  
class CustomPasswordResetView(PasswordResetView):
  form_class = CustomPasswordResetForm  
  template_name = 'users/password_reset.html'
 

class CustomPasswordConfirmView(PasswordResetConfirmView):
  form_class = CustomSetPasswordForm
  template_name = 'users/password_reset_confirm.html'
