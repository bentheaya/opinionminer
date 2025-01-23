from django.shortcuts import render, redirect, get_object_or_404
from .forms import InputDataForm
from .models import InputData, AnalysisResult
from django.utils.timezone import now
from textblob import TextBlob

def analyze_sentiment(text):
    # Using TextBlob to calculate sentiment polarity
    blob = TextBlob(text)
    score = blob.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)

    # Determine sentiment category based on polarity
    if score > 0.2:
        category = 'Positive'
    elif score < -0.2:
        category = 'Negative'
    else:
        category = 'Neutral'

    return score, category

def sentiment_analysis(request):
    if request.method == 'POST':
        form = InputDataForm(request.POST)
        if form.is_valid():
            input_data = form.save()
            text = input_data.text.strip()

            if not text:
                form.add_error('text', 'Input cannot be empty.')
                return render(request, 'sentiment/input.html', {'form': form})

            # Perform sentiment analysis
            score, category = analyze_sentiment(text)

            # Save the analysis result
            AnalysisResult.objects.create(
                input_data=input_data,
                sentiment_score=score,
                sentiment_category=category,
                analyzed_at=now()
            )
            return redirect('sentiment:result', pk=input_data.pk)
    else:
        form = InputDataForm()

    return render(request, 'input.html', {'form': form})

def sentiment_result(request, pk):
    input_data = get_object_or_404(InputData, pk=pk)
    analysis = input_data.analysis  # Get the related AnalysisResult
    return render(request, 'result.html', {
        'input_data': input_data,
        'analysis': analysis,
    })

def analysis_history(request):
    results = AnalysisResult.objects.all().order_by('-analyzed_at')  # Show latest first
    return render(request, 'history.html', {'results': results})

# For API's
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InputData, AnalysisResult
from .serializers import InputDataSerializer, AnalysisResultSerializer
from textblob import TextBlob

class SentimentAnalysisAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Validate input data
        serializer = InputDataSerializer(data=request.data)
        if serializer.is_valid():
            # Save input data
            input_data = serializer.save()
            
            # Perform sentiment analysis
            blob = TextBlob(input_data.text)
            polarity = blob.sentiment.polarity
            if polarity > 0:
                category = "Positive"
            elif polarity < 0:
                category = "Negative"
            else:
                category = "Neutral"

            # Save analysis result
            result = AnalysisResult.objects.create(
                input_data=input_data,
                sentiment_score=polarity,
                sentiment_category=category
            )
            result_serializer = AnalysisResultSerializer(result)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import ListAPIView

class AnalysisHistoryAPI(ListAPIView):
    queryset = AnalysisResult.objects.all().order_by('-analyzed_at')
    serializer_class = AnalysisResultSerializer
