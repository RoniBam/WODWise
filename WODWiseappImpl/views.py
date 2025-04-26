from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Box, Review
from django.contrib.admin.views.decorators import staff_member_required
import requests
from django.core.cache import cache

# Create your views here.
def index(request):
    boxes = Box.objects.all()
    # Get min/max price for slider
    all_prices = Box.objects.values_list('price_per_month', flat=True)
    min_price_val = min(all_prices) if all_prices else 0
    max_price_val = max(all_prices) if all_prices else 1000

    # Get all unique locations for the filter
    all_locations = Box.objects.values_list('location', flat=True).distinct()

    # Filtering
    selected_locations = request.GET.getlist('location')
    min_price = request.GET.get('min_price', min_price_val)
    max_price = request.GET.get('max_price', max_price_val)
    min_rating = request.GET.get('min_rating')

    if selected_locations:
        boxes = boxes.filter(location__in=selected_locations)
    if min_price:
        boxes = boxes.filter(price_per_month__gte=min_price)
    if max_price:
        boxes = boxes.filter(price_per_month__lte=max_price)

    # Filter by average rating (in Python, since it's a property)
    if min_rating:
        boxes = [box for box in boxes if box.average_rating is not None and box.average_rating >= float(min_rating)]

    return render(request, 'WODWiseappImpl/index.html', {
        'boxes': boxes,
        'all_locations': all_locations,
        'selected_locations': selected_locations,
        'filter_min_price': min_price,
        'filter_max_price': max_price,
        'filter_min_rating': min_rating or '',
        'min_price_val': min_price_val,
        'max_price_val': max_price_val,
    })

def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    reviews = Review.objects.filter(box=box).order_by('-created_at')
    return render(request, 'WODWiseappImpl/box_detail.html', {'box': box, 'reviews': reviews})

def box_list(request):
    boxes = Box.objects.all()
    return render(request, 'WODWiseappImpl/box_list.html', {'boxes': boxes})

def box_create_form(request):
    cities = get_israeli_cities()
    return render(request, 'WODWiseappImpl/create_box.html', {'cities': cities})

@csrf_exempt
def box_create(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
    
    name = request.POST.get('name')
    location = request.POST.get('location')
    
    # Validate required fields
    if not name or not location:
        messages.error(request, 'Name and city are required fields')
        return redirect('box_create_form')
    
    try:
        box = Box.objects.create(
            name=name,
            location=location,
            website=request.POST.get('website'),
            price_per_month=request.POST.get('price_per_month'),
            description=request.POST.get('description'),
            open_gym=request.POST.get('open_gym', False)
        )
        messages.success(request, f'Box "{box.name}" created successfully!')
        return redirect('box_detail', box_id=box.id)
    except Exception as e:
        messages.error(request, f'Error creating box: {str(e)}')
        return redirect('box_create_form')

@csrf_exempt
def add_review(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        # Replace with request.user if you have authentication
        Review.objects.create(
            box=box,
            user=User.objects.first(),
            rating=rating,
            comment=comment
        )
        return redirect('WODWiseappImpl:box_detail', box_id=box.id)
    return render(request, 'WODWiseappImpl/review_form.html', {'box': box})

CITIES_CACHE_KEY = 'israeli_cities'
CITIES_API_URL = 'https://countriesnow.space/api/v0.1/countries/cities'

def get_israeli_cities():
    cities = cache.get(CITIES_CACHE_KEY)
    if cities is not None:
        return cities
    # Fetch from API
    response = requests.post(CITIES_API_URL, json={"country": "Israel"})
    if response.status_code == 200:
        data = response.json()
        cities = data.get('data', [])
        cache.set(CITIES_CACHE_KEY, cities, timeout=None)  # Cache forever (until server restart or manual clear)
        return cities
    return []
