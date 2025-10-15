from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .serializers import RestaurantSerializer, FoodItemSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Restaurant, FoodItem 

# Home Page
def home_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'tesstapp/home.html', {'restaurants': restaurants})

# Restaurant Detail Page
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    food_items = FoodItem.objects.filter(restaurant=restaurant)
    context = {
        'restaurant': restaurant,
        'food_items': food_items
    }
    return render(request, 'tesstapp/restaurant_menu.html', context)
# Cart Page
def cart_page(request):
    return render(request, 'tesstapp/cart.html')

# Login Page
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')
        else:
            return render(request, 'tesstapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tesstapp/login.html')

# Signup Page
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'tesstapp/signup.html', {'error': 'Username already exists'})
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'tesstapp/signup.html')

# Search Food Items
def search_food(request):
    query = request.GET.get('food', '').strip()
    food_results = FoodItem.objects.filter(name__icontains=query) if query else []
    return render(request, 'tesstapp/search_results.html', {
        'food_results': food_results,
        'restaurant_results': [],
        'query': query,
        'location': '',
    })

# Search Restaurants by Location
def search_location(request):
    location = request.GET.get('location', '').strip()
    restaurant_results = Restaurant.objects.filter(location__icontains=location) if location else []
    return render(request, 'tesstapp/search_results.html', {
        'restaurant_results': restaurant_results,
        'food_results': [],
        'query': '',
        'location': location,
    })

# Combined Search
def search(request):
    query = request.GET.get('food', '').strip()
    location = request.GET.get('location', '').strip()
    food_results = FoodItem.objects.filter(name__icontains=query) if query else []
    restaurant_results = Restaurant.objects.filter(location__icontains=location) if location else []
    return render(request, 'tesstapp/search_results.html', {
        'food_results': food_results,
        'restaurant_results': restaurant_results,
        'query': query,
        'location': location
    })

# Django REST Framework ViewSets
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer 

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
