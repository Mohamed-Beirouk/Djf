from django.db import models
from django.contrib.auth.models import User

class C_emploi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    sexe = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    description = models.TextField(max_length=400, default="", editable=False)
    experience = models.CharField(max_length=100, default="", editable=False)
    adresse = models.CharField(max_length=100, default="", editable=False)
    skills = models.CharField(max_length=200, default="", editable=False)

    def __str__(self):
        return self.telephone
 
class Entreprise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    sexe = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    nom_entreprise = models.CharField(max_length=100)

    def __str__ (self):
        return self.user.username

class Travail(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    titre = models.CharField(max_length=200)
    salaire = models.FloatField()
    image = models.ImageField(upload_to="")
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    date_creation = models.DateField()

    def __str__ (self):
        return self.titre

class Deposer(models.Model):
    entreprise = models.CharField(max_length=200, default="")
    travail = models.ForeignKey(Travail, on_delete=models.CASCADE)
    c_emploi = models.ForeignKey(C_emploi, on_delete=models.CASCADE)
    cv = models.ImageField(upload_to="")
    date_depot = models.DateField()

    def __str__ (self):
        return str(self.c_emploi)


class Visiteur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.user
    
class Notes(models.Model):
    c_emploi = models.ForeignKey(C_emploi, on_delete=models.CASCADE)
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    note = models.IntegerField()
    
    def __str__ (self):
        return self.c_emploi

class Langue(models.Model):
    nom = models.CharField(max_length=100, default="", editable=False)
    description = models.TextField(max_length=400, default="", editable=False)
    
    def __str__ (self):
        return self.nom
class LangueMaitrise(models.Model):
    c_emploi = models.ForeignKey(C_emploi, on_delete=models.CASCADE, related_name="chercheur")
    langue = models.ForeignKey(Langue, default="",on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.langue.nom +" "+self.c_emploi.user.first_name
