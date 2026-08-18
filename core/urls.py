from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('contact/', views.contact, name='contact'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.NWZLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('book/', views.book_appointment, name='book_appointment'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
