from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Garage, GarageService, ServiceType
from .forms import GarageProfileForm, GarageServiceForm
# from accounts.models import User


# -------------------------------------------------------
# Garage Dashboard
# -------------------------------------------------------
@login_required
def garage_dashboard(request):
    if request.user.role != 'garage':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')

    garage = Garage.objects.filter(user=request.user).first()
    services = GarageService.objects.filter(garage=garage)
    return render(request, 'garage/garage_dashboard.html', {'garage': garage, 'services': services})


# -------------------------------------------------------
# Create or Edit Garage Profile
# -------------------------------------------------------
@login_required
def garage_profile(request):
    if request.user.role != 'garage':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')

    garage, created = Garage.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = GarageProfileForm(request.POST, instance=garage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Garage profile updated successfully.')
            return redirect('garage_dashboard')
    else:
        form = GarageProfileForm(instance=garage)
    return render(request, 'garage/garage_profile.html', {'form': form})


# -------------------------------------------------------
# Add New Service
# -------------------------------------------------------
@login_required
def add_service(request):
    if request.user.role != 'garage':
        messages.error(request, 'Unauthorized access.')
        return redirect('login')

    garage = get_object_or_404(Garage, user=request.user)
    if request.method == 'POST':
        form = GarageServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.garage = garage
            service.save()
            messages.success(request, 'Service added successfully!')
            return redirect('garage_dashboard')
    else:
        form = GarageServiceForm()
    return render(request, 'garage/add_service.html', {'form': form})


# -------------------------------------------------------
# Delete Service
# -------------------------------------------------------
@login_required
def delete_service(request, pk):
    service = get_object_or_404(GarageService, id=pk, garage__user=request.user)
    service.delete()
    messages.success(request, 'Service deleted successfully!')
    return redirect('garage_dashboard')

