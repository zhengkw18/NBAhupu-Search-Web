# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from newsapp.models import Team,Player,Article,parseArticle
class NewsscrapyPipeline(object):
    def process_item(self, item, spider):
        return item
class PlayerPipeline(object):
    def process_item(self, item, spider):
        if item["id"]=="0":
            if Player.objects.filter(name=item["name"]):
                player = Player.objects.get(name=item["name"])
            else:
                player = Player(name=item["name"], team=item["team"])
            player.save()
            team = Team.objects.get(name=item["team"])
            try:
                players = json.loads(team.players)
            except AttributeError:
                players=[]
            players.append(item["name"])
            players=list(set(players))
            team.players = json.dumps(players,ensure_ascii=False)
            team.save()
        return item
class ArticlePipeline(object):
    def process_item(self, item, spider):
        if item["id"]=="1":
            if not Article.objects.filter(title=item["title"]):
                article = Article(title=item["title"],source=item["source"],time=item["datetime"],content=item["content"]);
                article.save()
                parseArticle(article)
                for team in Team.objects.all():
                    if((team.name in article.title) | (team.name in article.content)):
                        ids = json.loads(team.relatedids)
                        ids.append(str(article.id))
                        team.relatedids = json.dumps(list(set(ids)),ensure_ascii=False)
                        team.save()
                for player in Player.objects.all():
                    namelist = player.name.split('-')
                    lastname = namelist[-1]
                    if((lastname in article.title) | (lastname in article.content)):
                        team = Team.objects.get(name=player.team)
                        ids = json.loads(team.relatedids)
                        ids.append(str(article.id))
                        team.relatedids = json.dumps(list(set(ids)), ensure_ascii=False)
                        team.save()
        return item