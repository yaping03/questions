from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm,Form
from app01 import models
from django.forms import fields
from django.forms import widgets as wd
import json
# Create your views here.


def index(request):
    return HttpResponse("Welcome to here")
class Quest(ModelForm):
    class Meta:
        model = models.Question
        fields = ['caption','tp']

class OptionModelForm(ModelForm):
    class Meta:
        model = models.Option
        fields = ['name','score']

score = [i for i in range(1,11)]
def quest(request,qid):
    obj = models.Question.objects.filter(naire_id=qid)
    def my_iter():
        if not obj:
            form = Quest()
            yield {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}
        else:
            for item in obj:
                form = Quest(instance=item)
                temp = {'form': form, 'obj': item, 'option_class': 'hide', 'options': None}
                if item.tp == 2:
                    temp['option_class'] = ''
                    def inner(quee):
                        option_list = models.Option.objects.filter(qs=quee)
                        for i in option_list:
                            yield {'form': OptionModelForm(instance=i), 'obj': i}
                    temp["options"] = inner(item)
                yield temp
    if request.method=="POST":
        que_list=json.loads(request.POST.get('data'))
        for que in que_list:
            if que.get("pid"):
                models.Question.objects.filter(id=que.get("pid")).update(caption=que.get("title"), tp=que.get("type"))
                if que.get("type")=="2":
                    for option in que.get("options"):
                        if option.get("id"):
                            models.Option.objects.filter(id=option.get("id")).update(name=option.get("title"),score=option.get("score"))
                        else:
                            models.Option.objects.create(name=option.get("title"),score=option.get("score"),qs_id=que.get("pid"))
            else:
                que_obj=models.Question.objects.create(caption=que.get("title"),tp=que.get("type"),naire_id=qid)
                if que.get("type") == "2":
                    for option in que.get("options"):
                        models.Option.objects.create(name=option.get("title"), score=option.get("score"),
                                                     qs=que_obj)
        return HttpResponse("ok")


    return render(request, "quest.html", {"form_dict": my_iter(),"id":qid})


def del_quest(request,qid):
    if request.method=="POST":
        id = request.POST.get("qid")
        models.Question.objects.filter(id=id).delete()
        return HttpResponse("ok")
    return redirect("/quest/%s/"%qid)

def del_option(request,qid):
    if request.method=="POST":
        id = request.POST.get("qid")
        models.Option.objects.filter(id=id).delete()
        return HttpResponse("ok")
    return redirect("/quest/%s/"%qid)

