from django import forms
from .models import *
from django.contrib.auth import authenticate

class UsersForm(forms.ModelForm):
  class Meta:
    model = Users
    fields = '__all__'

class LoginForm(forms.ModelForm):
  class Meta:
    model = Users
    fields = ['email','pword']
    
  def clean(self):
    email = self.cleaned_data['email']
    pword = self.cleaned_data['pword']
    user = authenticate(email=email, pword=pword)
    if not user or not user.is_active:
      raise forms.ValidationError("Email or password is incorrect.")
    
class ReserveForm(forms.ModelForm):
  class Meta:
    model = Reserve
    fields = '__all__'

class RoomForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
    
class RoomPicsForm(forms.ModelForm):
  class Meta:
    model = Room
    fields = '__all__'
