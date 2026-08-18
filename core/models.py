import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    """A nutrition/wellness service NWZ offers (booked by clients)."""

    ICON_CHOICES = [
        ('leaf', 'Leaf'),
        ('heart', 'Heart'),
        ('scale', 'Scale'),
        ('baby', 'Maternal'),
        ('briefcase', 'Corporate'),
        ('plate', 'Plate'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(
        max_length=200,
        help_text="One-line summary shown on service cards."
    )
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(default=45)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='leaf')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    @property
    def price_display(self):
        return f"₦{self.price:,.0f}"

    @property
    def duration_display(self):
        if self.duration_minutes >= 60:
            hrs = self.duration_minutes // 60
            mins = self.duration_minutes % 60
            return f"{hrs}hr" + (f" {mins}min" if mins else "")
        return f"{self.duration_minutes} min"


class Appointment(models.Model):
    """A client's booking for a service session."""

    MODE_CHOICES = [
        ('in_person', 'In-person'),
        ('online', 'Online (video call)'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
    )
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name='appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='in_person')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    OPENING_TIME = datetime.time(9, 0)
    CLOSING_TIME = datetime.time(17, 0)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.full_name} — {self.service.name} on {self.date} {self.time}"

    # Statuses that are considered final — once an appointment reaches one
    # of these, it should never silently flip back to pending/confirmed.
    LOCKED_STATUSES = ('cancelled', 'completed')

    def clean(self):
        errors = {}

        if self.date and self.date < datetime.date.today():
            errors['date'] = "You can't book an appointment in the past."

        if self.time:
            if self.time < self.OPENING_TIME or self.time > self.CLOSING_TIME:
                errors['time'] = (
                    f"NWZ takes appointments between "
                    f"{self.OPENING_TIME.strftime('%I:%M %p')} and "
                    f"{self.CLOSING_TIME.strftime('%I:%M %p')}, every day."
                )

        # Guard against accidentally un-cancelling / un-completing an
        # appointment. This runs on every save (admin list-edit, admin
        # detail form, or code), so it can't be bypassed from the UI.
        if self.pk:
            try:
                original_status = Appointment.objects.only('status').get(pk=self.pk).status
            except Appointment.DoesNotExist:
                original_status = None

            if original_status in self.LOCKED_STATUSES and self.status != original_status:
                errors['status'] = (
                    f"This appointment is already marked "
                    f"'{dict(self.STATUS_CHOICES)[original_status]}' and can't be changed further."
                )

        if errors:
            raise ValidationError(errors)

    @property
    def is_upcoming(self):
        today = datetime.date.today()
        now = datetime.datetime.now().time()
        if self.date > today:
            return True
        if self.date == today and self.time >= now:
            return True
        return False

    @property
    def status_color(self):
        return {
            'pending': 'amber',
            'confirmed': 'blue',
            'completed': 'green',
            'cancelled': 'red',
        }.get(self.status, 'grey')


class ContactMessage(models.Model):
    """A message sent via the public contact form."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
