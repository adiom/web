from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate

def home(request):
	#ozon_id = None
	#ozon_key = None

	#if request.user.is_authenticated:
		# Если пользователь аутентифицирован, получаем его ozon_id и ozon_key
	#	ozon_id = request.user.ozon_id  # Предположим, что ozon_id хранится в поле модели пользователя user.ozon_id
	#	ozon_key = request.user.ozon_key  # Предположим, что ozon_key хранится в поле модели пользователя user.ozon_key

	#context = {
	#	'ozon_id': ozon_id,
	#	'ozon_key': ozon_key
	#}

	return render(request, 'main/home.html')#, context)

def sign_up(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('/home')
	else:
		form = RegisterForm()

	return render(request, 'registration/sign_up.html', {"form": form})