from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
import requests
import json


def home(request):
    base_url = 'https://api.moysklad.ru/api/remap/1.2/report/stock/all'
    name_and_password = request.user.last_name
    INN_and_email = request.user.email

    split_data = name_and_password.split("___")
    sklad_user = split_data[0]
    sklad_password = split_data[1]
    split_data = INN_and_email.split("___")
    INN = split_data[0]
    email = split_data[1]
    
    session = requests.Session()
    session.auth = (sklad_user, sklad_password)
    response = session.get(base_url)
    response_json = response.json()
    products = []
    
    if len(INN) == 12:
        for product in response_json['rows']:
            # Проверяем, начинается ли артикул с INN
            if product['article'].startswith(INN):
                product_data = {
                    'Имя': product['name'],
                    'Артикул': product['article'],
                    'Количество': product['stock'],
                    'SKLAD': 'moy_sklad'
                }
                products.append(product_data)
    else:
        for product in response_json['rows']:
            product_data = {
                'Имя': product['name'],
                'Артикул': product['article'],
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