from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('researcher', 'Principal Investigator / Researcher'),
        ('peer_reviewer', 'Academic Peer Reviewer'),
        ('general_public', 'General Observer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='researcher')
    department = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    academic_position = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    research_interests = models.TextField(help_text="Comma separated terms")
    is_public = models.BooleanField(default=True)

    bio_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Portfolio: {self.user.get_full_name() or self.user.username}"


class Publication(models.Model):
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Revision Required', 'Revision Required'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    journal_name = models.CharField(max_length=255)
    publication_date = models.DateField()
    doi = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to='publications/')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='Submitted')
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CoAuthor(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='co_authors')
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.publication.title})"


class Dataset(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    title = models.CharField(max_length=255)
    description = models.TextField()
    data_file = models.FileField(upload_to='datasets/')
    license = models.CharField(max_length=100, default='CC BY 4.0')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credentials')
    title = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    verification_file = models.FileField(upload_to='credentials/')

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class Review(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comments = models.TextField()
    decision = models.CharField(max_length=25, choices=Publication.STATUS_CHOICES)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.publication.title} by {self.reviewer.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


# ==========================================
# DATABASE SIGNALS / LIFECYCLE HANDLERS
# ==========================================

@receiver(post_save, sender=User)
def manage_user_profile_lifecycle(sender, instance, created, **kwargs):
    """Automatically generates profiles and portfolios when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)
        Portfolio.objects.create(user=instance)
