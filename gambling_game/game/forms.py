from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BetForm(forms.Form):
    """Form for placing bets"""
    bet_amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Bet Amount"
    )

class SignUpForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
