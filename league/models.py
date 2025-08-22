from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('player', 'Player'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class League(models.Model):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.season})"


class PlayerProfile(models.Model):
    POSITION_CHOICES = [
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('GK', 'Goalkeeper'),
        ('FWD', 'Forward'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="player_profile")
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
    limit_choices_to={'role': 'manager'},related_name="players")
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name="players")
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} (Manager: {self.manager.email if self.manager else 'None'},League: {self.league.name if self.league else 'None'}, Position: {self.get_position_display()})"