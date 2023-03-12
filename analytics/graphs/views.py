from django.shortcuts import render, redirect
from .models import Graph
from django.db.models import Sum
from django.db.models import Count
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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
    queryset = Graph.objects.all()
    labels = [obj.age for obj in queryset]
    data = [obj.likes for obj in queryset]
    return render(request, 'bargraph.html', {'labels': labels, 'data': data})
    

def piechart(request):
    data = Graph.objects.values('gender').annotate(likes_count=Sum('likes'))
    gender = [d['gender'] for d in data]
    likes_count = [d['likes_count'] for d in data]
    graph_data={'gender':gender,'likes':likes_count}
    graph_data_json=json.dumps(graph_data)
    return render(request,'piechart.html',{'graph_data':graph_data_json})

def vectormap(request):
    data = Graph.objects.all().values('country', 'likes')
    return render(request, 'vectormap.html', {'data': data})

def registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})
        
        
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})
        
        user = User.objects.create(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        
        return redirect('login') 
    else:
        return render(request, 'registration.html')

    

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        except User.DoesNotExist:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')