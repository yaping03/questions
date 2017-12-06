from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm,Form
from app01 import models
from django.forms import fields
from django.forms import widgets as wd
# Create your views here.
class Quest(ModelForm):
    class Meta:
        model = models.Question
        fields = ['caption','tp']

def quest(request,id):
    obj = models.Questionnaire.objects.filter(id=id).first()
    que = models.Question.objects.all()
    if obj:
        form = Quest()

        if request.method=="POST":
            pass
        return render(request,"request.html",{"que":que})
    else:
        return HttpResponse("问卷不存在")
