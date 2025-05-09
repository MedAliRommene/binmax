from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'includes/sidebar.html', {'segment': 'index'})

@login_required
def dynamic_tables(request):
    return render(request, 'dyn_dt/index.html', {'segment': 'dyn_dt'})

@login_required
def dynamic_api(request):
    return render(request, 'dyn_api/index.html', {'segment': 'dyn_api'})

@login_required
def charts(request):
    return render(request, 'charts/index.html', {'segment': 'charts'})

@login_required
def tables(request):
    return render(request, 'templates/tables.html', {'segment': 'tables'})

@login_required
def billing(request):
    return render(request, 'templates/billing.html', {'segment': 'billing'})

@login_required
def vr(request):
    return render(request, 'templates/vr.html', {'segment': 'virtual_reality'})

@login_required
def rtl(request):
    return render(request, 'templates/rtl.html', {'segment': 'rtl'})

@login_required
def profile(request):
    return render(request, 'templates/profile.html', {'segment': 'profile'})

# Authentication views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})