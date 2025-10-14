from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
def home_page(request):
    return render(request,'tesstapp/home.html')

from rest_framework import viewsets
from .models  import restaurant,fooditem
from .serializers import restaurantSerializer, fooditemSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import models 

class restaurantViewSet(viewsets.ModelViewSet):
    queryset=restaurant.objects.all()
    serializer_class=restaurantSerializer

class fooditemViewSet(viewsets.ModelViewSet):
    queryset=fooditem.objects.all()
    serializer_class=fooditemSerializer    

def restaurant_detail(request, restaurant_id):
    # Fetch the restaurant along with its menu items
    res = get_object_or_404(restaurant.objects.prefetch_related('menu'), id=restaurant_id)
    return render(request, 'tesstapp/restaurant_menu.html', {'restaurant': res})
   
def cart_page(request):
    return render(request, 'tesstapp/cart.html')

# Login page
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')  # redirect to home
        else:
            return render(request, 'tesstapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tesstapp/login.html')

# Signup page
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'tesstapp/signup.html', {'error': 'Username already exists'})
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'tesstapp/signup.html')

# Food search
def search_food(request):
    query = request.GET.get('food', '').strip()  # remove extra spaces
    food_results = []
    
    if query:  # only search if query is not empty
        food_results = fooditem.objects.filter(name__icontains=query)
    
    return render(request, 'tesstapp/search_results.html', {
        'food_results': food_results,
        'query': query
    })

# Location search
def search_location(request):
    location = request.GET.get('location', '').strip()
    restaurant_results = []
    
    if location:
        restaurant_results = restaurant.objects.filter(location__icontains=location)
    
    return render(request, 'tesstapp/search_results.html', {
        'restaurant_results': restaurant_results,
        'location': location
    })


def search(request):
    query = request.GET.get('food', '').strip()
    location = request.GET.get('location', '').strip()

    food_results = fooditem.objects.filter(name__icontains=query) if query else []
    restaurant_results = restaurant.objects.filter(location__icontains=location) if location else []

    return render(request, 'tesstapp/search_results.html', {
        'food_results': food_results,
        'restaurant_results': restaurant_results,
        'query': query,
        'location': location
    })