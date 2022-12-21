from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='E-mail*',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    theme = forms.CharField(
        required=True,
        label='Topic*',
        help_text='Required field',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        required=True,
        label='Message*',
        help_text='Input you text here, please',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contact
        fields = ['theme', 'email', 'message']