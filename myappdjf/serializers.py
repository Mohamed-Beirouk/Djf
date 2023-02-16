from rest_framework import serializers
from myappdjf.models import *





class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = '__all__'

class TravailSerializer(serializers.ModelSerializer):
    # "2023-02-14T18:51:49.671335Z"
    class Meta:
        model = Travail
        fields = '__all__'

class DeposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposer
        fields = '__all__'

class VisiteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visiteur
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'

class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = '__all__'
    

class LangueMaitriseSerializer(serializers.ModelSerializer):
    lang = serializers.ReadOnlyField(source='langue.nom')
    class Meta:
        model = LangueMaitrise
        fields=['lang']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields='__all__'


class C_emploiSerializer(serializers.ModelSerializer):
    nom = serializers.ReadOnlyField(source='user.first_name')
    prenom = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = C_emploi
        fields = ['nom', 'prenom', 'email', 'username', 'id', 'telephone', 'image', 'sexe', 'type', 'description', 'experience', 'adresse', 'skills']