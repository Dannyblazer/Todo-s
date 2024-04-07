from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with given email, username, and password.

        Raises:
            ValueError: If email or username is not provided.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not username:
            raise ValueError(_("Users must have a username"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with given email, username, and password.

        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)

class Account(AbstractBaseUser):
    email = models.EmailField(_("email address"), max_length=60, unique=True)
    username = models.CharField(_("username"), max_length=30, unique=True)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_admin = models.BooleanField(_("admin status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        return self.is_staff

    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the app 'app_label'."""
        return self.is_staff
