import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Appointment, ContactMessage, Service


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'field')
            field.widget.attrs.setdefault('placeholder', field.label)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'mode', 'full_name', 'phone', 'email', 'notes']
        widgets = {
            'service': forms.Select(attrs={'class': 'field'}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'field',
                'min': datetime.date.today().isoformat(),
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'field',
                'min': '09:00',
                'max': '17:00',
            }),
            'mode': forms.Select(attrs={'class': 'field'}),
            'full_name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'class': 'field', 'placeholder': '080...'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'you@example.com'}),
            'notes': forms.Textarea(attrs={
                'class': 'field',
                'rows': 4,
                'placeholder': 'Anything NWZ should know before your session (optional)',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['notes'].required = False

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        service = cleaned_data.get('service')

        if date and time and service:
            clashing = Appointment.objects.filter(
                date=date, time=time, status__in=['pending', 'confirmed']
            )
            if self.instance.pk:
                clashing = clashing.exclude(pk=self.instance.pk)
            if clashing.exists():
                raise forms.ValidationError(
                    "That time slot is already booked. Please choose another time."
                )
        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'field', 'placeholder': '080... (optional)'}),
            'subject': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Subject (optional)'}),
            'message': forms.Textarea(attrs={'class': 'field', 'rows': 5, 'placeholder': 'How can NWZ help?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['subject'].required = False
