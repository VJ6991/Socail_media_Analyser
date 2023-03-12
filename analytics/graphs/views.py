from django.shortcuts import render, redirect
from .models import Graph
from django.db.models import Sum
from django.db.models import Count
import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import connection


def dashboard(request):
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
    # return render(request,"dashboard.html")


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
    
    cursor = connection.cursor()

    cursor.execute('select min(age) from graphs_graph')
    min_age=cursor.fetchone()[0]
    range_start = ((min_age+ 9) // 10 * 10)-10

    cursor.execute('select max(age) from graphs_graph')
    max_age=cursor.fetchone()[0]
    range_stop = ((max_age + 9) // 10 * 10)
    
    # labels_list=[]
    # view_sum_list=[]
    data_to_pass = [['Age Range', 'Views Count']]
    while (range_start < range_stop):
        label = str(range_start + 1) + " - " + str(range_start + 10)
        # labels_list.append(label)
        #above is the label
        print("label : " + label)
        query = "select sum(Views) from graphs_graph where age >= " + str(range_start + 1) + " and age <= " + str(range_start + 10)  
        print("query : " + query)
        cursor.execute(query)
        view_sum = cursor.fetchone()[0]
       
        if view_sum==None:
            view_sum=0
        data_to_pass.append([label,view_sum])
        # view_sum_list.append(view_sum)
        # print (view_sum)
         ## add code for curser execute etc and get the sum...
        range_start = range_start + 10

        # chart_data = {'label_list': labels_list, 'view_sum_list':view_sum_list}
        # chart_data_json = json.dumps(chart_data)
   
    modified_data = json.dumps(data_to_pass)
    return render(request, 'bargraph.html',{'values':modified_data})
    

def piechart(request):  
    data = Graph.objects.values('gender').annotate(likes_count=Sum('likes'))
    gender = [d['gender'] for d in data]
    likes_count = [d['likes_count'] for d in data]
    graph_data={'gender':gender,'likes':likes_count}
    graph_data_json=json.dumps(graph_data)
    return render(request,'piechart.html',{'graph_data':graph_data_json,'likes':likes_count})

def vectormap(request):
    data_to_pass = [['Country', 'Likes Count']]
    data = Graph.objects.values('country').annotate(likes_count=Sum('likes'))
    country = [d['country'] for d in data]
    likes_count = [d['likes_count'] for d in data]
    for cnt,lik in zip(country,likes_count):
        data_to_pass.append([cnt,lik])
    
    modified_data = json.dumps(data_to_pass) 
    # graph_data={'country':country,'likes':likes_count}
    # graph_data_json=json.dumps(graph_data)
    return render(request, 'vectormap.html', {'values':modified_data})

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