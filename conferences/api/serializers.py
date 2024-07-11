from rest_framework import serializers

from conferences import models

class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conference
        fields = '__all__'
        read_only_fields = ('submission_link',)
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be after end date.")
        if data['submission_deadline'] > data['start_date']:
            raise serializers.ValidationError("Submission deadline cannot be after start date.")
        return data