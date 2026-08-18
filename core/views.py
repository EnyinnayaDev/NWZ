from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AppointmentForm, ContactForm, SignUpForm
from .models import Appointment, Service


def home(request):
    services = Service.objects.filter(is_active=True)[:4]
    stats = [
        {'value': 2, 'suffix': '+', 'label': 'Years of practice'},
        {'value': 100, 'suffix': '%', 'label': 'Personalised plans'},
        {'value': 2, 'suffix': '', 'label': 'Ways to meet — in-person & online'},
        {'value': 9, 'suffix': '–5', 'label': 'Open every day (9am–5pm)'},
    ]
    return render(request, 'core/home.html', {
        'services': services,
        'stats': stats,
    })


def about(request):
    return render(request, 'core/about.html')


def services(request):
    all_services = Service.objects.filter(is_active=True)
    return render(request, 'core/services.html', {'services': all_services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'core/service_detail.html', {'service': service})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for reaching out — NWZ will get back to you shortly."
            )
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Your account has been created. Please sign in to book a session."
        )
        return response


class NWZLoginView(LoginView):
    template_name = 'core/login.html'


@login_required
def book_appointment(request):
    initial = {
        'full_name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    }
    service_slug = request.GET.get('service')
    if service_slug:
        service = Service.objects.filter(slug=service_slug, is_active=True).first()
        if service:
            initial['service'] = service.pk

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(
                request,
                "Your appointment request has been received. "
                "NWZ will confirm it shortly — track it on your dashboard."
            )
            return redirect('dashboard')
    else:
        form = AppointmentForm(initial=initial)

    return render(request, 'core/book_appointment.html', {'form': form})


@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)
    upcoming = [a for a in appointments if a.is_upcoming and a.status != 'cancelled']
    past = [a for a in appointments if not (a.is_upcoming and a.status != 'cancelled')]
    return render(request, 'core/dashboard.html', {
        'upcoming': upcoming,
        'past': past,
    })


@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.info(request, "Your appointment has been cancelled.")
    return redirect('dashboard')
