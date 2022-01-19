from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.urls import reverse

class Categoty(models.Model):
    name    =   models.CharField(max_length=100,blank=False)
    total_time = models.IntegerField(default=3)
    description     =   models.TextField(max_length=300,blank=False)
    photo   =models.ImageField(upload_to="categoy images/",default='product1.jpg')
    userlist=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name

    def descrip(self):
        return self.description[:100]+"..."
    def get_time(self):
        return self.total_time
    def get_question_number(self):
        question=Question.objects.filter(category=self)
        for i in question:
            print(i)
        return question

QUESTION_LEVEL=(
    ('easy','easy'),
    ('medium','medium'),
    ('hard','hard'),
)

class UserLevel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    categry=models.ForeignKey(Categoty,on_delete=models.CASCADE)
    points=models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(str(self.user),self.points)
class Question(models.Model):
    category=   models.ForeignKey(Categoty,on_delete=models.CASCADE)
    title   =   models.CharField(max_length=300,blank=False)
    level   =   models.CharField(choices=QUESTION_LEVEL,max_length=20,blank=False,default='easy')
    option1 =   models.CharField(max_length=150,blank=False)
    option2 =   models.CharField(max_length=150,blank=False)
    option3 =   models.CharField(max_length=150,blank=False)
    option4 =   models.CharField(max_length=150,blank=False)
    answer  =   models.CharField(max_length=150,blank=False)
    hints   =   models.TextField(blank=False,default="this is hint's of this answer")
    read_at = models.ManyToManyField(User, related_name="read_at", blank=True)


    def __str__(self):
        return self.title
class Tournament(models.Model):
    name=models.CharField(max_length=200,blank=False)
    entry_point=models.IntegerField(default=100)
    description=models.TextField(max_length=500)
    photo=models.ImageField(default="product1.jpg",upload_to="Tournaments")
    attemp=models.ManyToManyField(User,blank=True)
    fisrt_attemp=models.ManyToManyField(User,blank=True,related_name="first_attemp")
    winning_points=models.IntegerField(default=500)
    time=models.IntegerField(default=2)
    start_date=models.DateTimeField(auto_now=True,auto_now_add=False)
    end_date=models.DateTimeField(auto_now_add=False,auto_now=False)

    def __str__(self):
        return self.name

    def get_tournament_question_number(self):
        question=TournamentQuestion.objects.filter(tournament=self)
        for i in question:
            print(i)
        return question
    def get_absolute_url(self):
        return reverse("App_Quiz:tournament_start",kwargs={"id":self.id})

class TournamentQuestion(models.Model):
    tournament=   models.ForeignKey(Tournament,on_delete=models.CASCADE)
    title   =   models.CharField(max_length=300,blank=False)
    option1 =   models.CharField(max_length=150,blank=False)
    option2 =   models.CharField(max_length=150,blank=False)
    option3 =   models.CharField(max_length=150,blank=False)
    option4 =   models.CharField(max_length=150,blank=False)
    answer  =   models.CharField(max_length=150,blank=False)
    attemp  =   models.ManyToManyField(User,blank=True)

    def __str__(self):
        return '{}-{}'.format(str(self.tournament),self.title)

class Quizwin(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Categoty,on_delete=models.CASCADE)
    point=models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}-{}'.format(str(self.user),str(self.category),self.point)




class TempResult(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(Categoty,on_delete=models.CASCADE,blank=True)
    corrent=models.IntegerField(default=0)
    timetaken=models.CharField(max_length=10,blank=True)
    point=models.IntegerField(default=0)
    asnwer_show=models.IntegerField(default=0)
    timestamp=models.DateTimeField(auto_now=True,auto_now_add=False)


    def __str__(self):
        return str(self.user)

class QuizAtemp(models.Model):
    category=models.ForeignKey(Categoty,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    wrong=models.IntegerField(default=0)
    correct=models.IntegerField(default=0)
    score=models.IntegerField(default=0)


    def __str__(self):
        return '{}-{}-{}'.format(self.category,self.user,self.score)

