from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        error_messages={'required': 'Ismingizni kiriting'},
        widget=forms.TextInput(attrs={
            'placeholder': 'Ismingiz',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        required=True,
        error_messages={'required': 'Email kiriting', 'invalid': 'Email noto\'g\'ri'},
        widget=forms.EmailInput(attrs={
            'placeholder': 'mail@email.com',
            'class': 'form-input'
        })
    )
    phone = forms.RegexField(
        regex=r'^\+?[\d\s\-]+$',
        required=True,
        error_messages={
            'required': 'Telefon raqamingizni kiriting',
            'invalid': 'Faqat raqam kiriting'
        },
        widget=forms.TextInput(attrs={
            'placeholder': '+998901234567',
            'class': 'form-input',
            'type': 'tel'
        })
    )
    message = forms.CharField(
        required=True,
        error_messages={'required': 'Xabar kiriting'},
        widget=forms.Textarea(attrs={
            'placeholder': 'Bu yerga xabaringizni kiriting',
            'class': 'form-input',
            'rows': 5
        })
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']