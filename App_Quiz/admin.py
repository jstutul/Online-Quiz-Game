from django.contrib import admin
from App_Quiz.models import *
# Register your models here.
admin.site.register(Categoty)

class AdminQuestion(admin.ModelAdmin):
    list_display = ['id','category','title','level']
admin.site.register(Question,AdminQuestion)

class AdminResult(admin.ModelAdmin):
    list_display = ['user','category','point']
admin.site.register(Quizwin,AdminResult)

admin.site.register(TempResult)
admin.site.register(Tournament)
admin.site.register(TournamentQuestion)
admin.site.register(QuizAtemp)
admin.site.register(UserLevel)