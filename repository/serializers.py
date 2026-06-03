# repository/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Publication, Dataset, UserProfile, Review

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = UserProfile
        fields = ['username', 'role', 'department', 'bio', 'avatar']

class PublicationSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Publication
        fields = ['id', 'author_name', 'title', 'abstract', 'journal_name', 'publication_date', 'doi', 'document', 'status', 'views_count', 'downloads_count']

class DatasetSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source='uploader.username', read_only=True)
    class Meta:
        model = Dataset
        fields = ['id', 'uploader_name', 'title', 'description', 'data_file', 'license', 'uploaded_at']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'publication', 'reviewer_name', 'comments', 'decision', 'reviewed_at']