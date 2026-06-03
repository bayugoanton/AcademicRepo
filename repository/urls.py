from django.urls import path, include
from django.contrib.auth import views as auth_views
from researchvault import settings
from rest_framework.routers import DefaultRouter
from . import views, api_views
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'publications', api_views.APIPublicationViewSet, basename='api-pubs')
router.register(r'datasets', api_views.APIDatasetViewSet, basename='api-datasets')
router.register(r'reviews', api_views.APIReviewViewSet, basename='api-reviews')

urlpatterns = [
    # Core Application Routes
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Internal Auth Pipeline
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Secure Dashboard & User Profiles
    path('dashboard/', views.profile_dashboard, name='dashboard'),
    path('profile/', views.profile_dashboard, name='profile'),
    path('portfolio/', views.profile_dashboard, name='portfolio'),
    
    # Publications Registry
    path('publications/', views.PublicationListView.as_view(), name='publication_list'),
    path('publications/new/', views.publication_create, name='publication_create'),
    path('publications/download/<int:pk>/', views.secure_download_publication, name='secure_download_publication'),
    
    # Datasets, Credentials, & Reviews
    path('datasets/', views.DatasetListView.as_view(), name='dataset_list'),
    path('datasets/new/', views.dataset_upload, name='dataset_upload'),
    path('credentials/', views.CredentialListView.as_view(), name='credential_list'),
    path('credentials/new/', views.credential_add, name='credential_add'),
    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/evaluate/<int:publication_id>/', views.submit_review, name='submit_review'),
    
    # System Utilities
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/deactivate/', views.deactivate_account, name='deactivate'),

    path('portfolio/', views.profile_dashboard, name='portfolio_view'),
    path('portfolio/generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('portfolio/edit/', views.edit_portfolio, name='edit_portfolio'),

    # API Engine
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    # Now that 'static' is imported, this will work without errors
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)