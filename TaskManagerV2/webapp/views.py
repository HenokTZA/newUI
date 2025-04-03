import os
import subprocess
import time
import uuid

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import RegistrationForm, MyAuthenticationForm
from .models import Profile, Container

# --- Global Port Allocation ---
used_ports = set()
base_frontend_port = 3100
base_backend_port = 5100
base_couchdb_port = 6000
base_redis_port = 6400

def get_next_available_port(base_port):
    """Find the next port not already allocated.
    (This simplistic method does not check OS-level usage.)"""
    port = base_port
    while port in used_ports:
        port += 1
    used_ports.add(port)
    return port

# 1. Frontpage (Home)
def home(request):
    return render(request, 'home.html')

# 2. Registration (Unified)
def register(request):
    """
    Handles:
      - Creating the user in Django
      - Creating the associated Profile
      - Logging the user in
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            raw_password = form.cleaned_data['password1']
            user = form.save()
            Profile.objects.create(
                user=user,
                address=form.cleaned_data.get('address'),
                telephone=form.cleaned_data.get('telephone')
            )
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# 3. Login
def login_view(request):
    if request.method == 'POST':
        form = MyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = MyAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 4. Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# 5. Dashboard / Subscription Plans page
@login_required
def dashboard(request):
    container = Container.objects.filter(user=request.user).first()
    server_ip = "127.0.0.1"  # Update this static IP as needed
    return render(request, 'dashboard.html', {
        'user': request.user,
        'container': container,
        'server_ip': server_ip
    })

# 6. Subscription page
@login_required
def subscribe(request):
    if request.method == 'POST':
        # (Dummy) Payment details
        card_number = request.POST.get("cardNumber")
        expiry_date = request.POST.get("expiryDate")
        cvv = request.POST.get("cvv")
        
        # In real code, you'd process payment here.
        user = request.user
        profile = user.profile
        
        # Generate unique ID and allocate ports
        unique_id = uuid.uuid4().hex[:8]
        frontend_port = get_next_available_port(base_frontend_port)
        backend_port = get_next_available_port(base_backend_port)
        couchdb_port = get_next_available_port(base_couchdb_port)
        redis_port = get_next_available_port(base_redis_port)
        
        # Save container configuration to the database
        Container.objects.create(
            user=user,
            unique_id=unique_id,
            frontend_port=frontend_port,
            backend_port=backend_port,
            couchdb_port=couchdb_port,
            redis_port=redis_port
        )
        
        # Set environment variables for Docker Compose.
        env_vars = os.environ.copy()
        env_vars.update({
            "FRONTEND_PORT": str(frontend_port),
            "BACKEND_PORT": str(backend_port),
            "COUCHDB_PORT": str(couchdb_port),
            "REDIS_PORT": str(redis_port),
            "STACK_ID": unique_id
        })
        
        # Path to docker-compose.yml
        compose_file_path = r"C:\Users\Henok\Desktop\system_managemnt_tool\docker-compose.yml"
        
        try:
            result = subprocess.run(
                [
                    "docker", "compose", "-f", compose_file_path,
                    "-p", f"stack_{unique_id}",
                    "up", "-d"
                ],
                check=True,
                capture_output=True,
                text=True,
                env=env_vars
            )
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            time.sleep(3)
            return redirect(f"http://34.42.81.87:{frontend_port}")
        except subprocess.CalledProcessError as e:
            print("Docker Compose Error:", e.stderr)
            messages.error(request, f"Error running docker-compose: {e.stderr}")
            return redirect('dashboard')
        except Exception as e:
            print("Unexpected Error:", e)
            messages.error(request, f"Unexpected error: {e}")
            return redirect('dashboard')
    # GET: Display the subscription form
    return render(request, 'subscribe.html', {'user': request.user})

# 7. API Endpoint: Returns user and container information as JSON, sorted by frontend port.
def users_api(request):
    if request.method == "GET":
        # Retrieve all container records and order by frontend_port
        containers = Container.objects.select_related('user').order_by("frontend_port")
        data = []
        for container in containers:
            profile = getattr(container.user, "profile", None)
            data.append({
                "id": container.frontend_port,  # using frontend_port as ID
                "name": f"{container.user.first_name} {container.user.last_name}",
                "email": container.user.email,
                "address": profile.address if profile else "",
                "telephone": profile.telephone if profile else "",
                "access_level":"5",
                "unique_id": container.unique_id,
                "backend_port": container.backend_port,
                "couchdb_port": container.couchdb_port,
                "redis_port": container.redis_port,
            })
        return JsonResponse({"users": data})
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
