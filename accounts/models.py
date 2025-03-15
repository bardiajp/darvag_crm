from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    first_name = models.CharField(_('First Name'), max_length=50, null=False, blank=False)
    last_name = models.CharField(_('Last Name'), max_length=50, null=False, blank=False)
    birth_date = models.DateField(_('Birth Date'), null=False, blank=False, default='2000-01-01')
    mobile_number = models.CharField(_('Mobile Number'), max_length=11, null=False, blank=False)
    phone_number = models.CharField(_('Phone Number'), max_length=11, null=False, blank=False)
    email = models.EmailField(_('Email Address'), unique=True, null=False, blank=False)
    address = models.TextField(_('Address'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=50, null=False, blank=False)
    state = models.CharField(_('State'), max_length=25, null=False, blank=False)
    zip_code = models.CharField(_('Zip Code'), max_length=10, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'users'

    def __str__(self):
        return f'{self.username}'

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def clean(self):
        super().clean()
        today = date.today()
        if self.birth_date > today:
            raise ValidationError({'birth_date': _('Birthday cannot be in the future!')})
        if (today.year - self.birth_date.year) < 0:
            raise ValidationError({'age': _('Age cannot be negative!')})


class Company(BaseModel):
    user = models.ManyToManyField(User, related_name='company_users')
    name = models.CharField(_('Name'), max_length=50, null=False, blank=False)
    company_no = models.CharField(_('Company No'), max_length=50, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies')
    industry = models.CharField(_('Industry'), max_length=50, null=False, blank=False)
    register_code = models.IntegerField(_('Register Code'), null=False, blank=False)
    mobile_number = models.CharField(_('Mobile Number'), max_length=15, null=False, blank=False)
    phone_number = models.CharField(_('Phone Number'), max_length=15, null=False, blank=False)
    address = models.TextField(_('Address'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=50, null=False, blank=False)
    state = models.CharField(_('State'), max_length=25, null=False, blank=False)
    zip_code = models.CharField(_('Zip Code'), max_length=10, null=False, blank=False)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        db_table = 'companies'

    def __str__(self):
        return f'{self.id} - {self.name} - {self.owner}'
