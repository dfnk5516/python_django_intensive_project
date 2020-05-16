from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import Fcuser

# Create your views here.

def index(request):
  return render(request, 'index.html', {'email' : request.session.get('user')})

class RegisterView(FormView):
  template_name = 'register.html'
  form_class = RegisterForm
  success_url = '/'

  def form_valid(self, form): # 유효성 검사 후 호출되는 함수에 유저 등록 작업 실행
    fcuser = Fcuser(
      email = form.data.get('email'),
      password = make_password(form.data.get('password')),
      level='user'
    )
    fcuser.save()
    return super().form_valid(form)

class LoginView(FormView):
  template_name = 'login.html'
  form_class = LoginForm
  success_url = '/'

  def form_valid(self, form): # 모든 데이터가 정상이면 session 에 저장
    self.request.session['user'] = form.data.get('email')
    return super().form_valid(form)

def logout(request):
  if 'user' in request.session:
      del(request.session['user'])
  return redirect('/')