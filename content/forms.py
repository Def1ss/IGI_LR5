from django import forms
from .models import GlossaryTerm

class GlossaryTermForm(forms.ModelForm):
    class Meta:
        model = GlossaryTerm
        fields = "__all__"