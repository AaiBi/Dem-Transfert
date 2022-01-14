from django import forms
from transfert.models import Transfert, Client, Receveur, Prefix_Code_Letter, Note


class Transfert_Form(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = [
            'ref', 'montant', 'commission', 'destination', 'created'
        ]


class Client_Form(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nom', 'prenom', 'telephone'
        ]


class Receveur_Form(forms.ModelForm):
    class Meta:
        model = Receveur
        fields = [
            'nom', 'prenom', 'telephone'
        ]


class Prefixe_Code_Form(forms.ModelForm):
    class Meta:
        model = Prefix_Code_Letter
        fields = [
            'prefix_code'
        ]


class Note_Form(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'message'
        ]