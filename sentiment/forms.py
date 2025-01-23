from django import forms
from .models import InputData

class InputDataForm(forms.ModelForm):
    class Meta:
        model = InputData
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter text for sentiment analysis...',
                'rows': 5,
            }),
        }
        labels = {
            'text': 'Text Input',
        }

        def clean_text(self):
            text = self.cleaned_data['text']
            if len(text) < 2:
                raise forms.ValidationError('The input is too short. Please provide more context.')
            if len(text) > 1000:
                raise forms.ValidationError('The input is too long. Please limit your text to 500 characters.')
            return text
