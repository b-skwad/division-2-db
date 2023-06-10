"""Database models for the project."""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
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


class BaseModel(models.Model):
    """Base Model used for Application Models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class GearTalentType(BaseModel):
    """
    Gear Talent Type object.

    To which type of gear doe the talent belong
    - Backpack
    - Body Armour
    - Weapon
    - TBD
    """

    talent_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.talent_type_name


class GearTalent(BaseModel):
    """
    The talents are special bonuses associated with specific weapons/armour.

    With some talents needing to meet a certain criteria in order to properly
    utilize them, while a few others do not need any requirements in order to
    use them. There are also Named Weapons and Armour pieces which have one
    Perfect/Perfected talent that is more powerful than the normal talent.
    """

    talent_type = models.ForeignKey(
        GearTalentType,
        related_name="gear_talent_type",
        on_delete=models.PROTECT,
    )
    talent_name = models.CharField(max_length=64, unique=True)
    talent_description = models.CharField(max_length=256)

    def __str__(self):
        return self.talent_name


class LoadOutSlot(BaseModel):
    """
    Gear Talent Type object.

    To which type of gear doe the talent belong
    - Backpack
    - Body Armour
    - Mask
    - Gloves
    - Knee-pads
    - Holster
    - Primary Weapon
    - Secondary Weapon
    - Sidearm
    - Primary Skill
    - Secondary Skill
    - Specialised
    """

    load_out_slot_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.load_out_slot_name


class GearAttributeType(BaseModel):
    """
    Gear Attribute Type object.

    Which type of attribute does the gear have
    - Offensive
    - Defensive
    - Utility
    - Core
    """

    gear_attribute_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.gear_attribute_type_name


class GearModificationType(BaseModel):
    """
    Gear Modification Type object.

    Which type of modification does the gear have
    - Offensive
    - Defensive
    - Utility
    """

    gear_modification_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.gear_modification_type_name


class GearModification(BaseModel):
    """
    Gear Modification object.

    Which type of modification does the gear have
    - % Weapon Damage
    - Armour
    - Skill Tier
    - etc
    """

    gear_modification_type = models.ForeignKey(
        GearModificationType,
        related_name="gear_modification_type",
        on_delete=models.PROTECT,
    )
    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    gear_modification_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.gear_modification_name


class GearAttribute(BaseModel):
    """
    Gear Attribute object.

    Which type of attribute does the gear have
    - % Critical Hit Damage
    - Armour on Kill
    - % Skill Haste
    - etc
    """

    gear_attribute_type = models.ForeignKey(
        GearAttributeType,
        related_name="gear_attribute_type",
        on_delete=models.PROTECT,
    )
    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    gear_attribute_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.gear_attribute_name
