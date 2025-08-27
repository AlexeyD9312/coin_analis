from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin #class from user model, create admin,manager and give permissions
from django.utils import timezone


class AdminUserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError('Email is required!')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuse should have staff status')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuse should have superuser status')
        
        return self.create_user(email, password, **extra_fields)

         


class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email adress', unique=True)
    phone_number = models.CharField('phone number', max_length=10, blank=True)
    date_of_birth = models.DateField('date of birth', null= True, blank=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_active = models.BooleanField('active',default=True)
    is_staff = models.BooleanField('staff status',default=False)
    date_joined = models.DateTimeField('date joined',default=timezone.now)

    objects = AdminUserManager() 
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
    def get_short_name(self):
        return self.first_name
    




