from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Box

# Create your views here.
def index(request):
    return render(request, 'WODWiseappImpl/index.html')

def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    return HttpResponse(f"Box: {box.name} - Location: {box.location}")

def box_list(request):
    boxes = Box.objects.all()
    boxes_info = []
    for box in boxes:
        boxes_info.append(f"Box: {box.name} - Location: {box.location} - Price: ${box.price_per_month}")
    return HttpResponse("<br>".join(boxes_info))

def box_create_form(request):
    return render(request, 'WODWiseappImpl/create_box.html')

@csrf_exempt
def box_create(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed", status=405)
    
    try:
        box = Box.objects.create(
            name=request.POST.get('name'),
            location=request.POST.get('location'),
            website=request.POST.get('website'),
            price_per_month=request.POST.get('price_per_month'),
            description=request.POST.get('description'),
            open_gym=request.POST.get('open_gym', False)
        )
        return HttpResponse(f"Box created successfully! ID: {box.id}")
    except Exception as e:
        return HttpResponse(f"Error creating box: {str(e)}", status=400)
