from rest_framework import serializers

from papers import models

class PaperSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    conference = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        user_data = {
            'id': obj.user.id,
            'author_name': f'{obj.user.first_name} {obj.user.last_name}',
            'author_email': obj.user.email,
        }
        return user_data

    def get_conference(self, obj):
        conf_data = {
            'id': obj.conference.id,
            'title': obj.conference.title,
            'acronym': obj.conference.acronym,
        }
        return conf_data

    class Meta:
        model = models.Paper
        fields = '__all__'