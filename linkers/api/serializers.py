from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from linkers import models
from user_app.models import CustomUser
from papers.models import Paper

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email')

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conference
        fields = ('id', 'title', 'acronym')

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paper
        fields = ('id', 'title', 'file')

class BaseConferenceCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        fields = ['email']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email field is required.")
        return value

class EditorConferenceListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    conference = ConferenceSerializer(many=True)
    class Meta:
        model = models.EditorConference
        fields = '__all__'

class EditorConferenceCreateSerializer(BaseConferenceCreateSerializer):
    class Meta(BaseConferenceCreateSerializer.Meta):
        model = models.EditorConference

class ReviewerConferenceListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    conference = ConferenceSerializer(many=True)
    class Meta:
        model = models.ReviewerConference
        fields = '__all__'

class ReviewerConferenceCreateSerializer(BaseConferenceCreateSerializer):
    class Meta(BaseConferenceCreateSerializer.Meta):
        model = models.ReviewerConference

class ReviewerPaperListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    paper = PaperSerializer(many=True)

    class Meta:
        model = models.ReviewerPaper
        fields = '__all__'

class ReviewerPaperCreateSerializer(serializers.ModelSerializer):
    reviewers = serializers.ChoiceField(choices=[], write_only=True)

    class Meta:
        model = models.ReviewerPaper
        fields = ['reviewers']

    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        choices = context.get('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['reviewers'].choices = choices
    
    def create(self, validated_data):
        reviewer_email = validated_data.pop('reviewers')
        reviewer = get_object_or_404(CustomUser, email=reviewer_email)

        paper_pk = validated_data.pop('paper_pk')
        paper = get_object_or_404(Paper, pk=paper_pk)

        reviewer_paper = models.ReviewerPaper.objects.create()
        reviewer_paper.paper.set([paper])
        reviewer_paper.user.set([reviewer])

        return reviewer_paper