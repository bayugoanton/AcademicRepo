from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_ratelimit.decorators import ratelimit 
import datetime

# PDF Generation - Using xhtml2pdf for Windows stability
from xhtml2pdf import pisa

from .models import UserProfile, Portfolio, Publication, Dataset, Credential, Review, Notification
from .forms import (
    UserRegistrationForm, UserProfileForm, PortfolioForm, 
    PublicationForm, CoAuthorFormSet, DatasetForm, CredentialForm, ReviewForm
)

# ==========================================
# STATIC / MARKETING PAGES
# ==========================================
class HomeView(TemplateView): template_name = 'pages/home.html'
class AboutView(TemplateView): template_name = 'pages/about.html'
class ContactView(TemplateView): template_name = 'pages/contact.html'
class SettingsView(TemplateView): template_name = 'settings/settings.html'

# ==========================================
# CORE DASHBOARD PIPELINE
# ==========================================
@login_required
def profile_dashboard(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    portfolio, created = Portfolio.objects.get_or_create(user=user)

    if request.method == 'POST':
        if 'username' in request.POST:
            new_username = request.POST.get('username', '').strip()
            new_email = request.POST.get('email', '').strip()
            new_first_name = request.POST.get('first_name', '').strip()
            new_last_name = request.POST.get('last_name', '').strip()
            new_role = request.POST.get('role', '').strip()
            new_avatar = request.FILES.get('avatar')

            if new_username != user.username:
                if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                    messages.error(request, f"Operational Identity Conflict: '{new_username}' is already allocated.")
                    return redirect(request.path)
                user.username = new_username

            user.email = new_email
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.save()

            profile.role = new_role
            if new_avatar:
                profile.avatar = new_avatar
            profile.save()

            messages.success(request, "Identity profile matrix successfully committed.")
            return redirect(request.path)
        else:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            portfolio_form = PortfolioForm(request.POST, instance=portfolio)
            if profile_form.is_valid() and portfolio_form.is_valid():
                profile_form.save()
                portfolio_form.save()
                messages.success(request, "Your profile and portfolio have been updated.")
                return redirect('dashboard')
    
    profile_form = UserProfileForm(instance=profile)
    portfolio_form = PortfolioForm(instance=portfolio)

    publications = Publication.objects.filter(author=user)
    datasets = Dataset.objects.filter(uploader=user)
    credentials = Credential.objects.filter(user=user)
    reviews = Review.objects.all()
    notifications = Notification.objects.filter(user=user).order_by('-id')[:5]

    pending_tasks_count = reviews.filter(status='pending').count() if hasattr(Review, 'status') else 3

    chart_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    base_activity = publications.count() + datasets.count() + credentials.count()
    chart_data = [max(0, base_activity - 4), max(0, base_activity - 2), max(0, base_activity - 1), max(1, base_activity), max(2, base_activity + 1), base_activity]

    context = {
        'profile_form': profile_form,
        'portfolio_form': portfolio_form,
        'profile': profile,
        'portfolio': portfolio,
        'publications': publications,
        'datasets': datasets,
        'credentials': credentials,
        'pending_tasks': pending_tasks_count,
        'notifications': notifications,
        'chart_labels': chart_labels,
        'chart_data': chart_data
    }
    
    if 'profile' in request.path:
        return render(request, 'profile/profile.html', context)
    elif 'portfolio' in request.path:
        return render(request, 'portfolio/portfolio.html', context)
    return render(request, 'dashboard/dashboard.html', context)

# ==========================================
# AUTHENTICATION & REGISTRATION
# ==========================================
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = user.profile
            profile.role = form.cleaned_data.get('role', 'researcher')
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

# ==========================================
# MANAGEMENT HOOKS
# ==========================================
class PublicationListView(ListView): model = Publication; template_name = 'publications/publication_list.html'; context_object_name = 'publications'

@login_required
def publication_create(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES)
        if form.is_valid():
            pub = form.save(commit=False); pub.author = request.user; pub.save()
            formset = CoAuthorFormSet(request.POST, instance=pub)
            if formset.is_valid():
                formset.save()
                messages.success(request, "Publication successfully added!")
                return redirect('dashboard')
    else: form = PublicationForm(); formset = CoAuthorFormSet()
    return render(request, 'publications/publication_form.html', {'form': form, 'formset': formset})

@login_required
def secure_download_publication(request, pk): get_object_or_404(Publication, pk=pk); return redirect('dashboard')

class DatasetListView(ListView): model = Dataset; template_name = 'datasets/dataset_list.html'; context_object_name = 'datasets'

@login_required
def dataset_upload(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            ds = form.save(commit=False); ds.uploader = request.user; ds.save()
            messages.success(request, "Dataset uploaded successfully.")
            return redirect('dashboard')
    else: form = DatasetForm()
    return render(request, 'datasets/dataset_form.html', {'form': form})

class CredentialListView(ListView): model = Credential; template_name = 'credentials/credential_list.html'; context_object_name = 'credentials'

@login_required
def credential_add(request):
    if request.method == 'POST':
        form = CredentialForm(request.POST, request.FILES)
        if form.is_valid():
            cred = form.save(commit=False); cred.user = request.user; cred.save()
            messages.success(request, "Credential added.")
            return redirect('dashboard')
    else: form = CredentialForm()
    return render(request, 'credentials/credential_form.html', {'form': form})

class ReviewListView(ListView): model = Review; template_name = 'reviews/review_list.html'; context_object_name = 'reviews'

@login_required
def submit_review(request, publication_id):
    pub = get_object_or_404(Publication, id=publication_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False); rev.reviewer = request.user; rev.publication = pub; rev.save()
            return redirect('dashboard')
    else: form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'publication': pub})

class NotificationListView(ListView): model = Notification; template_name = 'notifications/notification_list.html'; context_object_name = 'notifications'

def deactivate_account(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('settings')

def generate_pdf(request):
    """Generates PDF of the researcher's portfolio using xhtml2pdf."""
    portfolio = request.user.portfolio
    html_string = render_to_string('portfolio/pdf_template.html', {'user': request.user, 'portfolio': portfolio})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="academic_portfolio.pdf"'
    
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('PDF generation error', status=500)
    return response

@login_required
def edit_portfolio(request):
    portfolio = get_object_or_404(Portfolio, user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        p_form = PortfolioForm(request.POST, instance=portfolio)
        u_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Portfolio matrix successfully updated.")
            return redirect('portfolio')
    else:
        p_form = PortfolioForm(instance=portfolio)
        u_form = UserProfileForm(instance=profile)
        
    return render(request, 'portfolio/edit_portfolio.html', {'p_form': p_form, 'u_form': u_form})