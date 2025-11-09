from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

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
            booking.status = 'Pending'
            booking.save()

            # Send booking confirmation email
            send_mail(
                subject="Booking Confirmed",
                message=f"Your booking (ID: {booking.booking_id}) at {booking.garage.name} has been confirmed.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

            messages.success(request, 'Booking confirmed successfully!')
            return redirect('bookings:booking_list')
    else:
        form = BookingForm(user=request.user, initial={'garage': garage})

    return render(request, 'bookings/booking_form.html', {'form': form, 'garage': garage})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-booked_on')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def download_invoice(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)

    # Generate invoice PDF
    invoice_path = f"media/invoices/invoice_{booking.booking_id}.pdf"
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)

    c = canvas.Canvas(invoice_path, pagesize=A4)
    c.drawString(100, 800, "Smart Garage - Invoice")
    c.drawString(100, 780, f"Booking ID: {booking.booking_id}")
    c.drawString(100, 760, f"Customer: {booking.customer.get_full_name()}")
    c.drawString(100, 740, f"Garage: {booking.garage.name}")
    c.drawString(100, 720, f"Service: {booking.service.name}")
    c.drawString(100, 700, f"Vehicle: {booking.vehicle.brand} {booking.vehicle.model}")
    c.drawString(100, 680, f"Date: {booking.appointment_date.strftime('%d %b %Y')}")
    c.drawString(100, 660, f"Status: {booking.status}")
    c.drawString(100, 640, f"Remarks: {booking.remarks or 'N/A'}")

    c.showPage()
    c.save()

    booking.invoice_pdf.name = f"invoices/invoice_{booking.booking_id}.pdf"
    booking.save()

    return FileResponse(open(invoice_path, 'rb'), as_attachment=True, filename=f"Invoice_{booking.booking_id}.pdf")
