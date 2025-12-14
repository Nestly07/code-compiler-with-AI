from django import forms
from .models import User
from .models import Submission
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {'password': forms.PasswordInput()}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

from django import forms
from .models import Submission, LANGUAGE_CHOICES

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["language", "source_code", "display_name"]
        widgets = {
            "source_code": forms.Textarea(attrs={
                "rows": 18,
                "placeholder": "Write your solution here...",
                "spellcheck": "false",
                "style": "font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;"
            })
        }

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    display_name = forms.CharField(max_length=100, required=False)
