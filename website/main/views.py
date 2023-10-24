from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
import requests
import json


def home(request):
    # ... your existing code ...
    name_and_password = request.user.last_name
    split_data = name_and_password.split("___")
    sklad_user = split_data[0]
    sklad_password = split_data[1]

    products = [
        {'Имя': request.user.last_name,
         'Артикул': '880982069 2788',
         'Количество': 10.0,
         'SKLAD': 'moy_sklad'},
         {'Имя': 'Стрейч пленка 500 мм (3й сорт)',
         'Артикул': '880982069 2789',
         'Количество': 2.0,
         'SKLAD': 'moy_sklad'},
    ]

    # Укажите базовый URL для API МойСклад
    base_url = 'https://api.moysklad.ru/api/remap/1.2/report/stock/all'

    # Создание сессии для авторизации
    session = requests.Session()
    session.auth = (sklad_user, sklad_password)
    # Выполнение запроса для получения остатков товаров
    response = session.get(base_url)
    response_json = response.json()
    # Извлечение артикула и количества товара
    products = []
    for product in response_json['rows']:
    	product_data = {
    		'Имя': product['name'],
        	'Артикул': product['code'],
        	'Количество': product['stock'],
        	'SKLAD': 'moy_sklad'
    	}
    	products.append(product_data)

    
    return render(request, 'main/home.html', {'products': products})

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