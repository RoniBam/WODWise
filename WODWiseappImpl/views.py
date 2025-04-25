from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from .models import Box

# Create your views here.
def index(request):
    return render(request, 'WODWiseappImpl/index.html')

def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    return render(request, 'WODWiseappImpl/box_detail.html', {'box': box})

def box_list(request):
    boxes = Box.objects.all()
    return render(request, 'WODWiseappImpl/box_list.html', {'boxes': boxes})

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
        messages.success(request, f'Box "{box.name}" created successfully!')
        return redirect('box_list')
    except Exception as e:
        messages.error(request, f'Error creating box: {str(e)}')
        return redirect('box_create_form')
