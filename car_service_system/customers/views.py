from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle, Review
from .forms import VehicleForm, ReviewForm
from garage.models import Garage
from bookings.models import Booking


# -------------------------------------------------------
# Customer Dashboard
# -------------------------------------------------------
@login_required
def customer_dashboard(request):
    vehicles = Vehicle.objects.filter(customer=request.user)
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')[:5]
    return render(request, 'customers/customer_dashboard.html', {
        'vehicles': vehicles,
        'bookings': bookings
    })


# -------------------------------------------------------
# Vehicle Management (Add, Edit, Delete)
# -------------------------------------------------------
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
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=request.user)
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
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('customers:dashboard')
    return render(request, 'customers/vehicle_confirm_delete.html', {'vehicle': vehicle})


# -------------------------------------------------------
# Search Garages (Customer Side)
# -------------------------------------------------------
@login_required
def search_garage(request):
    query = request.GET.get('q', '')
    service_type = request.GET.get('service_type', '').strip()
    city = request.GET.get('city', '').strip()
    rating = request.GET.get('rating', '')

    garages = Garage.objects.filter(approved=True)  # show only approved garages

    # ✅ Filter by city or address
    if query:
        garages = garages.filter(Q(city__icontains=query) | Q(address__icontains=query))

    # ✅ Filter by city field (explicit filter)
    if city:
        garages = garages.filter(city__icontains=city)

    # ✅ Filter by service type
    if service_type:
        garages = garages.filter(services__service_type__name__icontains=service_type).distinct()

    # ✅ Filter by minimum rating
    if rating:
        try:
            garages = garages.filter(rating__gte=float(rating))
        except ValueError:
            pass

    return render(request, 'customers/search_garage.html', {
        'garages': garages,
        'query': query,
        'service_type': service_type,
        'city': city,
        'rating': rating
    })


# -------------------------------------------------------
# Garage Detail View (Customer Side)
# -------------------------------------------------------
@login_required
def garage_detail(request, garage_id):
    garage = get_object_or_404(Garage, id=garage_id, approved=True)
    reviews = garage.reviews.select_related('customer').order_by('-date')  # from Review model
    services = garage.services.select_related('service_type').all()
    return render(request, 'customers/garage_detail.html', {
        'garage': garage,
        'services': services,
        'reviews': reviews
    })


# -------------------------------------------------------
# Booking History
# -------------------------------------------------------
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')
    return render(request, 'customers/booking_history.html', {'bookings': bookings})


# -------------------------------------------------------
# Add Review / Feedback
# -------------------------------------------------------
@login_required
def add_review(request, garage_id):
    garage = get_object_or_404(Garage, id=garage_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.garage = garage
            review.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('customers:garage_detail', garage_id=garage.id)
    else:
        form = ReviewForm()
    return render(request, 'customers/add_review.html', {'form': form, 'garage': garage})
