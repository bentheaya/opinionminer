from rest_framework import serializers
from .models import InputData, AnalysisResult

class InputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputData
        fields = ['id', 'text', 'created_at']

class AnalysisResultSerializer(serializers.ModelSerializer):
    input_data = InputDataSerializer()  # Nested Serializer

    class Meta:
        model = AnalysisResult
        fields = ['id', 'input_data', 'sentiment_category', 'sentiment_score', 'analyzed_at']
