from django.db import models
import  jieba
import json
# Create your models here.
class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True,max_length=50)
    city = models.CharField(max_length=50)
    players = models.TextField()
    relatedids = models.TextField()
    def __str__(self):
        return  self.name
class Player(models.Model):
    name = models.CharField(unique=True,max_length=50)
    team = models.CharField(max_length=50)
    def __str__(self):
        return  self.name
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True,max_length=255)
    source = models.CharField(max_length=50)
    time = models.DateTimeField()
    content = models.TextField()
    def __str__(self):
        return self.title
class Spider(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)
    def __str__(self):
        return str(self.id)
class Word(models.Model):
    word = models.CharField(unique=True,max_length=50)
    relatedids = models.TextField()
    def __str__(self):
        return  self.word
def parseArticle(article):
    titlelist = jieba.cut_for_search(article.title)
    for ts in titlelist:
        if Word.objects.all().filter(word=ts):
            word = Word.objects.all().get(word=ts)
            try:
                idlist=json.loads(word.relatedids)
            except:
                idlist=[]
            idlist.append(str(article.id))
            idlist=list(set(idlist))
            word.relatedids=json.dumps(idlist,ensure_ascii=False)
            word.save()
        else:
            word = Word(word=ts,relatedids=[str(article.id)])
            word.save()
    contentlist = jieba.cut_for_search(article.content)
    for ts in contentlist:
        if Word.objects.all().filter(word=ts):
            word = Word.objects.all().get(word=ts)
            try:
                idlist = json.loads(word.relatedids)
            except:
                idlist = []
            idlist.append(str(article.id))
            idlist = list(set(idlist))
            word.relatedids = json.dumps(idlist, ensure_ascii=False)
            word.save()
        else:
            word = Word(word=ts, relatedids=[str(article.id)])
            word.save()