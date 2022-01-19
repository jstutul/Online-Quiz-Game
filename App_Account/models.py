from django.contrib.auth.models import User
from django.db import models
from App_Quiz.models import Categoty


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    photo=models.ImageField(upload_to="photo",blank=True,default="tutul.jpg")

    def __str__(self):
        return str(self.user)
    def save(self, *args, **kwargs):
        if self.points is not None:
            self.level=self.points/3000

        super(Profile, self).save(*args, **kwargs)

    def get_level(self):
        if self.level <=5:
            return "Novice learner"
        elif self.level>5 and self.level <=10:
            return "Advanced learner"
        elif self.level>10:
            return "Expert learner"