from django.shortcuts import render, redirect
from . import services
from users.forms import *
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Login(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    succes_url = 'dashboard/'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            request.session['user_email'] = email
            request.session['user_password'] = password
            return redirect('dashboard/')
        return super(Login, self).form_invalid(form)

class Registration(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        full_name = form.cleaned_data['full_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        services.post_user(full_name, email, password)
        return super(Registration, self).form_valid(form)

class ForgotPassword(FormView):
    template_name = 'forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = './email-sent/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        services.send_email(email)
        return super(ForgotPassword, self).form_valid(form)

class ChangePassword(FormView):
    template_name = 'password_change.html'
    form_class = ChangePasswordForm
    success_url = '/'

    def form_valid(self, form):
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        token = self.request.META['PATH_INFO'][-36:]
        print("TOKEN: ", token)
        services.change_password(token, password1)
        return super(ChangePassword, self).form_valid(form)

@method_decorator(login_required(login_url='/'), name='dispatch')
class Users(TemplateView):
    def get(self, request):
        users = services.get_users(self.request)
        return render(request, 'users.html', users)

class EmailSent(TemplateView):
    def get(self, request):
        return render(request, 'email_sent.html', {})
