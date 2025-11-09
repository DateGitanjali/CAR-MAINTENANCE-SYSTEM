from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle
from .forms import VehicleForm
from garage.models import Garage
from bookings.models import Booking
from django.db.models import Q 


@login_required
def customer_dashboard(request):
    vehicles = Vehicle.objects.filter(customer=request.user)
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')[:5]
    return render(request, 'customers/customer_dashboard.html', {
        'vehicles': vehicles,
        'bookings': bookings
    })


@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('customers:dashboard')
    else:
        form = VehicleForm()
    return render(request, 'customers/vehicle_form.html', {'form': form})


@login_required
 # make sure this import is at the top
def search_garage(request):
    query = request.GET.get('q', '')
    service_type = request.GET.get('service_type', '').strip()
    garages = Garage.objects.all()

    # ✅ Filter by city or address (your model has these fields)
    if query:
        garages = garages.filter(
            Q(city__icontains=query) | Q(address__icontains=query)
        )

    # ✅ Filter by service type name (via related models)
    if service_type:
        garages = garages.filter(
            services__service_type__name__icontains=service_type
        ).distinct()

    # ✅ Render template (make sure the name matches your file)
    return render(request, 'customers/search_garage.html', {
        'garages': garages,
        'query': query,
        'service_type': service_type
    })


@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')
    return render(request, 'customers/booking_history.html', {'bookings': bookings})

@login_required
def edit_vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk, customer=request.user)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('customers:dashboard')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'customers/vehicle_form.html', {'form': form, 'edit_mode': True})


@login_required
def delete_vehicle(request, pk):
    vehicle = Vehicle.objects.get(pk=pk, customer=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('customers:dashboard')
    return render(request, 'customers/vehicle_confirm_delete.html', {'vehicle': vehicle})
