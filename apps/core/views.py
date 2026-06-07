from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import TeamMember, Achievement, Partner
from apps.projects.models import Project, Service



def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz yuborildi! Tez orada bog'lanamiz.")
            return redirect('home')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'team': TeamMember.objects.all(),
        'achievements': Achievement.objects.all(),
        'partners': Partner.objects.all(),
        'featured_projects': Project.objects.filter(is_featured=True)[:6],
        'services': Service.objects.all(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'team': TeamMember.objects.all(),
        'achievements': Achievement.objects.all(),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xabaringiz yuborildi!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})
