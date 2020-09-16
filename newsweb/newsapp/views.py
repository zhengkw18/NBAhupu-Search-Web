from django.shortcuts import render, HttpResponse, redirect, Http404
from django.template import Context, Template
from newsapp.models import Team, Article, Player, Spider, parseArticle, Word
from django.core.paginator import Paginator
import datetime
import json
import jieba.analyse


# Create your views here.
def team(request, nid, pn):
    if len(pn.strip()) == 0:
        return redirect(to="/team/" + nid + "/1")
    teams = Team.objects.all().filter(id=nid)
    if teams:
        team = teams[0]
        idjson = team.relatedids
        ids = json.loads(idjson)
        idsnum = len(ids)
        articles = sorted([ars[0] for ars in [Article.objects.all().filter(id=id) for id in ids]], key=lambda x: x.time,
                          reverse=True)
        paginator = Paginator(articles, 10)
        page_num = int(pn)
        try:
            current_list = paginator.page(page_num)
        except:
            raise Http404("Page not found")
        if paginator.num_pages > 12:  # 如果分页的数目大于11
            if page_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 12)  # 按钮数
            elif page_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(page_num - 10, page_num + 1)  # 显示的按钮数
            else:
                pageRange = range(page_num - 5, page_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

        else:
            pageRange = range(1, paginator.num_pages + 1)  # 正常分配
        players = json.loads(team.players)
        context = {"team": team, "idsnum": idsnum, "current_list": current_list, "pageRange": pageRange,
                   "players": players, "nid": nid}
        return render(request, "team.html", context)
    else:
        raise Http404("Page not found")


def index(request, pn=None):
    if pn is None:
        return redirect(to="/index/1")
    else:
        articlelist = Article.objects.all().order_by('-time')
        paginator = Paginator(articlelist, 10)
        page_num = int(pn)
        try:
            current_list = paginator.page(page_num)
        except:
            raise Http404("Page not found")
        if paginator.num_pages > 12:  # 如果分页的数目大于11
            if page_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 12)  # 按钮数
            elif page_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(page_num - 10, page_num + 1)  # 显示的按钮数
            else:
                pageRange = range(page_num - 5, page_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

        else:
            pageRange = range(1, paginator.num_pages + 1)  # 正常分配
        rank = []
        for team in Team.objects.all():
            idjson = team.relatedids
            ids = json.loads(idjson)
            rank.append((len(ids), team.name, team.id))
        rank = sorted(rank, reverse=True)
        newsnum = len(Article.objects.all())
        current_num = page_num
        context = {"rank": rank, "pageRange": pageRange, "current_list": current_list, "newsnum": newsnum,
                   "current_num": current_num}
    return render(request, "index.html", context)


def news(request, nid):
    articles = Article.objects.all().filter(id=nid)
    if articles:
        article = articles[0]
        content = article.content
        for team in Team.objects.all():
            content = content.replace(team.name, """<a href="/team/""" + str(team.id) + """ ">""" + team.name + "</a>")
        for player in Player.objects.all():
            content = content.replace(player.name, """<a href="/team/""" + str(
                Team.objects.all().get(name=player.team).id) + """ ">""" + player.name + "</a>")
        paralist = content.split('\n')
        time = article.time.strftime("%Y-%m-%d %H:%M:%S")
        source = article.source
        context = {"article": article, "time": time, "paralist": paralist}
        return render(request, "news.html", context)
    else:
        raise Http404("Page not found")


def search(request):
    """
    Generates the actual response to the search.

    Relies on internal, overridable methods to construct the response.
    """
    wd = request.GET.get("q")
    context = {}

    if wd:
        searched = True
        pn = request.GET.get("pn")
        if pn:
            try:
                page_num = int(pn)
            except:
                page_num = 1
        else:
            page_num = 1
        query = wd
        time1 = datetime.datetime.now()
        dic = {}
        keylist = jieba.analyse.extract_tags(query, topK=20, withWeight=True)
        for key in keylist:
            if Word.objects.all().filter(word=key[0]):
                idstr = Word.objects.all().get(word=key[0])
                idlist = json.loads(idstr.relatedids)
                for id in idlist:
                    if not int(id) in dic.keys():
                        dic[int(id)] = 0
                    dic[int(id)] = dic[int(id)] + key[1]
        relist = []
        for id, weight in dic.items():
            relist.append((id, weight))
        relist = sorted(relist, key=lambda x: x[1], reverse=True)
        idresults = [x[0] for x in relist]
        results = []
        for id in idresults:
            results.append(Article.objects.all().get(id=id))
        time2 = datetime.datetime.now()
        time = (time2 - time1).total_seconds();
        num = len(results)
        paginator = Paginator(results, 10)

        try:
            page = paginator.page(page_num)
        except:
            raise Http404("Page not found")
        if paginator.num_pages > 12:  # 如果分页的数目大于11
            if page_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 12)  # 按钮数
            elif page_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(page_num - 10, page_num + 1)  # 显示的按钮数
            else:
                pageRange = range(page_num - 5, page_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示
        else:
            pageRange = range(1, paginator.num_pages + 1)  # 正常分配
        context = {
            'query': query,
            'current_list': page,
            'paginator': paginator,
            'current_num': page_num,
            'num': num,
            'time': time,
            'pageRange': pageRange,
        }
    else:
        searched = False
    context["searched"] = searched

    return render(request, "search.html", context)


def spider(request):
    sp = Spider.objects.all().get(id=1)
    if request.POST.get('spider'):
        if sp.status == 'OFF':
            sp.status = 'ON'
            sp.save()
        else:
            sp.status = 'OFF'
            sp.save()
        return redirect(to='/spider/')
    else:
        if sp.status == 'OFF':
            return render(request, "spider.html", {'s1': '暂停', 's2': '运行'})
        else:
            return render(request, "spider.html", {'s1': '运行', 's2': '暂停'})
