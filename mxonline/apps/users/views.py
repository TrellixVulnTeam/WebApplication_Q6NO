from django.shortcuts import render
from django.contrib.auth import authenticate, login    # 认证库，登陆函数
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q

from django.views.generic.base import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password   # 对明文进行密码加密
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class LoginView(View):
	# 继承后，get,post等函数可以直接使用，通过as_view()方法被urls引用
	def get(self, request):
		return render(request, "login.html", {})
	
	def post(self, request):
		login_form = LoginForm(request.POST)        # 表单校验，html名称与form的名称一致
		if login_form.is_valid():                   # 检查是否为error
			user_name = request.POST.get("username", "")
			pass_word = request.POST.get("password", "")
			user = authenticate(username=user_name, password=pass_word)
			# 如果验证成功user是个对象，如果失败则为None
			if user is not None:
				login(request, user)    # 登陆
				return render(request, "index.html")        # 判断
			else:
				return render(request, "login.html", {"msg": "用户名或密码错误"})   # 数据库验证不通过
		else:
			return render(request, "login.html", {"login_form": login_form})    # 登陆不成功
			# 通过这样的方式，将login_form输出到前端，通过前端对login_form.errors的遍历循环，取出key和error

class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, "register.html", {'register_form': register_form})
	
	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get("email", "")
			pass_word = request.POST.get("password", "")
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.password = make_password(pass_word)
			user_profile.save()
			# 发送邮件
			send_register_email(user_name, "register")
			return render(request, "index.html")
		else:
			return render(request, "register.html", {'register_form': register_form})

# Create your views here.

# def user_login(request):
# 	if request.method == "POST":
# 		user_name = request.POST.get("username", "")
# 		pass_word = request.POST.get("password", "")
# 		user = authenticate(username=user_name, password=pass_word)
# 		# 如果验证成功user是个对象，如果失败则为None
# 		if user is not None:
# 			login(request, user)    # 登陆
# 			return render(request, "index.html")        # 判断
# 		else:
# 			return render(request, "login.html", {"msg": "账号或密码错误！"})    # 登陆不成功
# 	elif request.method == "GET":
# 		return render(request, "login.html", {})