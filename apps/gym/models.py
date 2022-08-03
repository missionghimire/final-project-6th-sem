from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# src/users/model.py
class CustomUser(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField( unique=True)
    full_name = models.CharField('Full Name',
                                 max_length=255,
                                 blank=True,
                                 null=False)

    address=models.CharField(max_length=100,null=True)    
    number=models.CharField(max_length=100,null=True)                         
    image = models.FileField(upload_to= 'uploads/%Y/%m/%d',null=True)

    is_trainer=models.BooleanField(default=False)
    REQUIRED_FIELDS = 'full_name', 'username','address','number','image',
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Enquery(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_text = models.TextField()

    def __str__(self):
        return self.user.username


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class TrainerDepartment(models.Model):
    DEPARTMENT=[
        ("GYM","GYM"),
        ("Cardio","Cardio"),
        ("zumba","zumba")
        
    ]
    department=models.CharField(max_length=100,choices=DEPARTMENT)
    def __str__(self):
        return self.department

class Trainer(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    department=models.ForeignKey(TrainerDepartment,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username




class Member(models.Model):
    Gender_Choice = [('male', 'male'), ('female', 'female'),
                     ('others', 'others')]
    STATUS=[
        ('pending','pending'),
        ('Accept','Accept'),
        ('Reject','Reject')
    ]                 

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    date_of_birth = models.DateField()
    gender = models.CharField(max_length=100, choices=Gender_Choice)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    joindate = models.DateTimeField(auto_now_add=True)
    expiredate = models.DateField()
    initialamount = models.DecimalField(max_digits=10, decimal_places=2)
    trainer=models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True)
    status=models.CharField(max_length=100,choices=STATUS,default="pending",null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class AccountInfo(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    # def __str__(self):
    #     return self.member.first_name


class Dietmanagement(models.Model):
    height = models.IntegerField()
    weight = models.IntegerField()
    # def __str__(self):
    #     return self.username


class Dietmanagement(models.Model):
    height = models.CharField(max_length=199)
    weight = models.CharField(max_length=100)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    message = models.TextField(max_length=100)

    def __str__(self):
        return self.Name


class Category(models.Model):
    options=(
        ('breakfast','breakfast'),
        ('lunch','lunch'),
        ('dinner','dinner'),
        ('snacks','snacks'),
    )
    name=models.CharField(max_length=50,choices=options)
    def __str__(self):
        return self.name

