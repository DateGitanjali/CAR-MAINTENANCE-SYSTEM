from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from garage.models import Garage

@login_required
def book_service(request, garage_id=None):
    garage = get_object_or_404(Garage, id=garage_id) if garage_id else None

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.status = 'Booked'
            booking.save()
            messages.success(request, 'Booking confirmed successfully!')
            return redirect('bookings:booking_list')  # ✅ correct

    else:
        form = BookingForm(user=request.user, initial={'garage': garage})

    return render(request, 'bookings/book_service.html', {
        'form': form,
        'garage': garage
    })
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})
