from django.db import models

from config import settings


class Habit(models.Model):
    """Модель привычка"""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habit")
    place = models.CharField(max_length=250)
    time = models.TimeField()
    action = models.CharField(max_length=250)

    is_pleasant = models.BooleanField(default=False)  # Приятная привычка

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_to",
    )

    periodicity = models.PositiveSmallIntegerField(default=1)  # По умолчанию - ежедневно
    reward = models.CharField(max_length=250, blank=True, null=True)
    execution_time = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} - {self.action}"
