from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import UserProfile, Portfolio, Publication, CoAuthor, Dataset, Credential, Review

from django import forms
from .models import Publication

from django import forms
from .models import Portfolio, UserProfile

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['research_interests', 'bio_text', 'is_public']
        widgets = {
            'research_interests': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'bio_text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department', 'avatar']

class PublicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'journal_name', 'publication_date', 'doi', 'document']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department', 'bio', 'avatar']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['research_interests', 'is_public']
        widgets = {
            'research_interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'journal_name', 'publication_date', 'doi', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'journal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'doi': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }

CoAuthorFormSet = inlineformset_factory(Publication, CoAuthor, fields=('name', 'email'), extra=2, can_delete=True)

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['title', 'description', 'data_file', 'license']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_file': forms.FileInput(attrs={'class': 'form-control'}),
            'license': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = ['title', 'issuing_organization', 'issue_date', 'expiry_date', 'verification_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'verification_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['decision', 'comments']
        widgets = {
            'decision': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

        