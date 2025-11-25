from django.shortcuts import render, redirect
from .models import Team
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by('-created_date')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)


def filter_options(request):
    model = request.GET.get("model")
    city = request.GET.get("city")
    year = request.GET.get("year")
    body_style = request.GET.get("body_style")

    filters = Q()
    if model:
        filters &= Q(model=model)
    if city:
        filters &= Q(city=city)
    if year:
        filters &= Q(year=year)
    if body_style:
        filters &= Q(body_style=body_style)

    cars = Car.objects.filter(filters)

    return JsonResponse({
        "models": list(cars.values_list("model", flat=True).distinct()),
        "cities": list(cars.values_list("city", flat=True).distinct()),
        "years": list(cars.values_list("year", flat=True).distinct()),
        "body_styles": list(cars.values_list("body_style", flat=True).distinct()),
    })




def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        email_subject = f'You have a new message from CarDealer Website regarding {subject}'
        message_body = f'Name: {name}. Email: {email}. Phone: {phone}. Message: {message}'

        admin_info = User.objects.filter(is_superuser=True).first()
        if admin_info:
            admin_email = admin_info.email
            send_mail(
                email_subject,
                message_body,
                'syedmdyeasin456@gmail.com',
                [admin_email],
                fail_silently=False,
            )

        messages.success(request, 'Thank you for contacting us. We will get back to you shortly')
        return redirect('contact')

    return render(request, 'pages/contact.html')


