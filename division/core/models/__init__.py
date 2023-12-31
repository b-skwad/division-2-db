"""Database models for the project."""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


from .gear import (
    GearAttribute,
    GearAttributeType,
    GearModification,
    GearModificationType,
    GearTalent,
    GearTalentType,
    LoadOutSlot,
)

from .skills import (
    Skill,
    Slot,
    SlotModificationType,
    # SlotModification
)


class UserManager(BaseUserManager):
    """Manager for Users in the System."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the System."""

    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

__all__ = (
    "GearAttribute",
    "GearAttributeType",
    "GearModification",
    "GearModificationType",
    "GearTalent",
    "GearTalentType",
    "LoadOutSlot",
    "Skill",
    "Slot",
    "SlotModificationType",
    # "SlotModification",
)


