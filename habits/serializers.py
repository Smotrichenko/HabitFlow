from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner", "created_at")

    def validate(self, attrs):
        reward = attrs.get("reward", getattr(self.instance, "reward", None))
        related_habit = attrs.get(
            "related_habit", getattr(self.instance, "related_habit", None)
        )
        is_pleasant = attrs.get(
            "is_pleasant", getattr(self.instance, "is_pleasant", False)
        )
        execution_time = attrs.get(
            "execution_time", getattr(self.instance, "execution_time", None)
        )
        periodicity = attrs.get("periodicity", getattr(self.instance, "periodicity", 1))

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if execution_time is not None and execution_time > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно быть больше 120 секунд."
            )

        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только приятные привычки."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не могут быть вознаграждения или связанной привычки."
            )

        return attrs
