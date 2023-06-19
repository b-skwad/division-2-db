"""Skill Models for the Division 2 DB App"""

from django.db import models

from division.core.models.generics import BaseModel


class Skill(BaseModel):
    """
    Skill object.

    Which type of kill
    - Turret
    - Ballistic Shield
    - % Skill Haste
    - etc
    """

    skill_name = models.CharField(max_length=24, unique=True)
    skill_description = models.CharField(max_length=2048, unique=True)

    def __str__(self):
        return self.skill_name


class SkillSlot(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    skill_slot_name = models.CharField(max_length=24, unique=True)
    skill = models.ForeignKey(
        Skill,
        related_name="skill",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.skill_slot_name


class SkillVariant(BaseModel):
    """
    Skill object variant.

    Which type of variant by skill
    - Defender Drone
    - Artillery Turret
    - Reviver Hive
    """

    skill_variant_name = models.CharField(max_length=24, unique=True)
    skill_variant_description = models.CharField(max_length=2048, unique=True)
    skill = models.ForeignKey(
        Skill,
        related_name="variant_skill",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.skill_variant_name


class SkillSlotModificationType(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    percent_value = models.BooleanField(default=True)
    max_value = models.IntegerField(default=0)
    skill_slot_modification_type_name = models.CharField(max_length=24, unique=True)

    def __str__(self):
        return self.skill_slot_modification_type_name


class SkillSlotModification(BaseModel):
    """
    Skill object slot.

    Which type of slot by skill
    - Agitator Slot
    - Battery Slot
    - Gyro Slot
    - etc
    """

    skill_slot = models.ForeignKey(
        SkillSlot,
        related_name="skill_slot",
        on_delete=models.PROTECT,
    )
    skill_slot_modification_type = models.ForeignKey(
        SkillSlotModificationType,
        related_name="skill_slot_modification_type",
        on_delete=models.PROTECT,
    )
