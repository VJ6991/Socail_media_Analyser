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
    likes_by_age_range = Graph.objects.values('age').annotate(num_likes=Count('likes'))
    age_ranges = [item['age'] for item in likes_by_age_range]
    num_likes = [item['num_likes'] for item in likes_by_age_range]
    return render(request, 'bargraph.html', {'age_ranges': age_ranges,'num_likes': num_likes})
    

def piechart(request):
    data = Graph.objects.values('gender').annotate(likes_count=Sum('likes'))
    gender = [d['gender'] for d in data]
    likes_count = [d['likes_count'] for d in data]
    graph_data={'gender':gender,'likes':likes_count}
    graph_data_json=json.dumps(graph_data)
    return render(request,'piechart.html',{'graph_data':graph_data_json})

def vectormap(request):
    context = {
        'chart_js': True,
        'chart_data': {
            'labels': ['US', 'Canada', 'Mexico', 'Brazil', 'Argentina'],
            'datasets': [{
                'label': 'Likes',
                'data': [50, 20, 30, 40, 10],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                'borderWidth': 1
            }]
        },
        'chart_options': {
            'legend': {
                'display': False
            },
            'scales': {
                'xAxes': [{
                    'type': 'map',
                    'position': 'top',
                    'gridLines': {
                        'display': False
                    },
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            },
            'plugins': {
                'map': {
                    'center': {'lat': 37.8, 'lng': -96},
                    'zoom': 4,
                    'geoJSON': 'https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson',
                    'tooltipTemplate': '<%=label%>: <%=value%> likes'
                }
            }
        }
    }
    return render(request, 'vectormap.html', context)


def registration(request):
    if request.method == 'POST':
        # Get form data from request
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        
        # Check if password and confirm password match
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})
        
        # Create new user
        user = User.objects.create(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        
        return redirect('login')  # Replace 'home' with your desired URL name
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