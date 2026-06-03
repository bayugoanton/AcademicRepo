from django.contrib import admin
from .models import UserProfile, Portfolio, Publication, CoAuthor, Dataset, Credential, Review, Notification

class CoAuthorInline(admin.TabularInline):
    model = CoAuthor
    extra = 1

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'created_at')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__email', 'department')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'publication_date', 'downloads_count')
    list_filter = ('status', 'publication_date')
    search_fields = ('title', 'author__username', 'doi')
    inlines = [CoAuthorInline]

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_public')
    search_fields = ('user__username', 'research_interests')

admin.site.register(Dataset)
admin.site.register(Credential)
admin.site.register(Review)
admin.site.register(Notification)