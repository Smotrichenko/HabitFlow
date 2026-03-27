from celery import shared_task

from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task(ignore_result=True)
def send_habits_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.select_related("owner").filter(time__hour=current_time.hour, time__minute=current_time.minute)

    for habit in habits:
        chat_id = habit.owner.telegram_chat_id
        text = f"Напоминание: {habit.action} в {habit.place} (время на выполнение: {habit.execution_time} секунд.)"
        send_telegram_message(chat_id=chat_id, text=text)
