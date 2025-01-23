from django.db import models

class InputData(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

class AnalysisResult(models.Model):
    input_data = models.OneToOneField(InputData, on_delete=models.CASCADE, related_name="analysis")
    sentiment_score = models.FloatField()
    sentiment_category = models.CharField(max_length=50)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sentiment_category} ({self.sentiment_score})"
