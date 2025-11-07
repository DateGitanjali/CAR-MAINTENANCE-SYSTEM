from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from garages.models import Garage

@login_required
def book_service(request, garage_id=None):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, 'Service booked successfully!')
            return redirect('customers:dashboard')
    else:
        initial_data = {}
        if garage_id:
            initial_data['garage'] = Garage.objects.get(id=garage_id)
        form = BookingForm(user=request.user, initial=initial_data)

    return render(request, 'bookings/booking_form.html', {'form': form})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})
