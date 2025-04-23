from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Profile(models.Model):
    """Model representing extended user profile information."""
    
    PANEL_ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Manager', 'Manager'),
        ('Employee', 'Pracownik'),
    ]

    DEPARTMENT_CHOICES = [
        ('Security', 'Ochrona'),
        ('Management', 'Zarząd'),
        ('Food', 'Gastronomia'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Użytkownik'
    )
    discord_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='ID Discord'
    )
    rank = models.CharField(
        max_length=100,
        verbose_name='Ranga'
    )
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        verbose_name='Dział'
    )
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates',
        verbose_name='Przełożony'
    )
    base_weekly_payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Podstawowa wypłata tygodniowa'
    )
    overtime_hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Stawka za nadgodziny'
    )
    panel_role = models.CharField(
        max_length=20,
        choices=PANEL_ROLE_CHOICES,
        default='Employee',
        verbose_name='Rola w panelu'
    )

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rank})"


class TimeEntry(models.Model):
    """Model representing a work time entry."""
    
    STATUS_CHOICES = [
        ('Pending', 'Oczekujący'),
        ('Approved', 'Zaakceptowany'),
        ('Rejected', 'Odrzucony'),
    ]

    employee = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='time_entries',
        verbose_name='Pracownik'
    )
    start_time = models.DateTimeField(
        verbose_name='Czas rozpoczęcia'
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Czas zakończenia'
    )
    duration = models.DurationField(
        verbose_name='Czas trwania',
        null=True,
        blank=True,
        editable=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name='Status'
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_entries',
        verbose_name='Zatwierdzone przez'
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data zatwierdzenia'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notatki'
    )
    week_number = models.IntegerField(
        editable=False,
        verbose_name='Numer tygodnia'
    )
    year = models.IntegerField(
        editable=False,
        verbose_name='Rok'
    )

    class Meta:
        verbose_name = 'Wpis czasu pracy'
        verbose_name_plural = 'Wpisy czasu pracy'
        ordering = ['-start_time']
        indexes = [
            models.Index(fields=['employee', 'week_number', 'year']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        # Calculate duration only if end_time is set
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        else:
            self.duration = None
            
        # Set week number and year
        self.week_number = self.start_time.isocalendar()[1]
        self.year = self.start_time.year

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.start_time.date()} ({self.status})"


class Payout(models.Model):
    """Model representing a weekly payout calculation."""
    
    STATUS_CHOICES = [
        ('Calculated', 'Obliczona'),
        ('Paid', 'Wypłacona'),
        ('Error', 'Błąd'),
    ]

    employee = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='payouts',
        verbose_name='Pracownik'
    )
    period_start_date = models.DateField(
        verbose_name='Początek okresu'
    )
    period_end_date = models.DateField(
        verbose_name='Koniec okresu'
    )
    approved_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Zatwierdzone godziny'
    )
    overtime_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Godziny nadliczbowe'
    )
    base_pay_earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Wynagrodzenie podstawowe'
    )
    overtime_pay_earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Wynagrodzenie za nadgodziny'
    )
    bonuses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Premie'
    )
    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Potrącenia'
    )
    total_pay = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Suma do wypłaty',
        editable=False
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Calculated',
        verbose_name='Status'
    )
    calculated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data obliczenia'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data wypłaty'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Notatki'
    )

    class Meta:
        verbose_name = 'Wypłata'
        verbose_name_plural = 'Wypłaty'
        ordering = ['-period_start_date']
        indexes = [
            models.Index(fields=['employee', 'period_start_date']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        # Calculate total pay
        self.total_pay = (
            self.base_pay_earned +
            self.overtime_pay_earned +
            self.bonuses -
            self.deductions
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - Tydzień {self.period_start_date} ({self.status})"
