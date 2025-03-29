from django.db import models
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class SpentTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="spent_times"
    )
    date = models.DateField()
    hours = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.hours} hours on {self.date} for {self.project.name}"
