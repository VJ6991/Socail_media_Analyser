from django.shortcuts import render
from .models import Graph
from django.db.models import Sum
import json
def dashboard(request):
    
    return render(request,"dashboard.html")


def linegraph(request):
    # data=Graph.objects.values_list('date','likes','Views')
    data = Graph.objects.values('date').annotate(likes_count=Sum('likes'),views_count=Sum('Views'))
    dates = [d['date'].strftime('%d-%m-%Y') for d in data]
    # likes = [d[1] for d in data]
    # views = [d[2] for d in data]
    likes_count=[d['likes_count'] for d in data]
    views_count=[d['views_count'] for d in data]
    chart_data = {'dates': dates, 'likes':likes_count, 'views': views_count}
    chart_data_json = json.dumps(chart_data)
    return render(request,'linegraph.html',{'chart_data': chart_data_json,'data':data})

def bargraph(request):
    return render(request,'bargraph.html')

def piechart(request):
    data = Graph.objects.values('gender').annotate(likes_count=Sum('likes'))
    gender = [d['gender'] for d in data]
    likes_count = [d['likes_count'] for d in data]
    graph_data={'gender':gender,'likes':likes_count}
    graph_data_json=json.dumps(graph_data)
    return render(request,'piechart.html',{'graph_data':graph_data_json})


# def chart_view(request):
#     data = Graph.objects.all()
#     return render(request, 'chart.html', {'data': data})