from rest_framework import serializers

from reviews import models

class ReviewSerializer(serializers.ModelSerializer):
    paper = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.Review
        fields = '__all__'

    def get_paper(self, obj):
        paper_data = {
            'id': obj.paper.id,
            'title': obj.paper.title,
            'author': obj.paper.user.email,
        }
        return paper_data

    def get_user(self, obj):
        user_data = {
            'id': obj.user.id,
            'reviewer_name': f'{obj.user.first_name} {obj.user.last_name}',
            'reviewer_email': obj.user.email,
        }
        return user_data