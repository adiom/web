from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
import requests
import json
import time

def get_ozon(client_id, client_api, article):
    url = "https://api-seller.ozon.ru/v3/product/info/stocks"
    headers = {
        "Client-Id": client_id,
        "Api-Key": client_api 
        }

    body = {
        "filter" : { "offer_id": [article] }, "limit": "1"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        if response.status_code == 200:
            print(body)
            total_products = data["result"]["items"]
            if total_products:
                return total_products[0]['stocks'][1]['present']
            else:
                return 0
            #print("Total number of products:", total_products)
        else:
            #print("Request failed with status code:", response.status_code)
            return("Error message:", data["message"])
    except requests.exceptions.RequestException as e:
            return("Request failed:", e)

def home(request):
    base_url = 'https://api.moysklad.ru/api/remap/1.2/report/stock/all'
    name_and_password = request.user.last_name
    print(request.user.last_name)
    ozon_id_and_ozon_key = request.user.first_name
    INN_and_email = request.user.email

    split_data = name_and_password.split("___")
    sklad_user = split_data[0]
    sklad_password = split_data[1]
    split_data = INN_and_email.split("___")
    INN = split_data[0]
    email = split_data[1]
    split_data = ozon_id_and_ozon_key.split("___")
    ozon_id = split_data[0]
    ozon_key = split_data[1]
    
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
                'Ozon': get_ozon(ozon_id, ozon_key, product['article'])
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