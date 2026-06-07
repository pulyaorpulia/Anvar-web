from django.shortcuts import render, get_object_or_404
from .models import Project, Service


def project_list(request):
    category = request.GET.get('category', '')  # ➕ filter
    projects = Project.objects.all()
    if category:
        projects = projects.filter(category=category)

    context = {
        'projects': projects,
        'services': Service.objects.all(),
        'current_category': category,
        'categories': Project.CATEGORY_CHOICES,
    }
    return render(request, 'projects/project_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.filter(category=project.category).exclude(slug=slug)[:3]  # ➕
    context = {
        'project': project,
        'related': related,
    }
    return render(request, 'projects/project_detail.html', context)


def project_extra(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'projects/project_extra.html', {'project': project})