from django.db import models


class Receveur(models.Model):
    nom = models.CharField(max_length=300)
    prenom = models.CharField(max_length=300)
    telephone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=300)
    prenom = models.CharField(max_length=300)
    telephone = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Monnaie(models.Model):
    nom = models.CharField(max_length=300)

    def __str__(self):
        return self.nom


class Transfert(models.Model):
    ref = models.CharField(max_length=300)
    montant = models.IntegerField()
    commission = models.IntegerField()
    destination = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    receveur = models.ForeignKey(Receveur, on_delete=models.CASCADE)
    monnaie = models.ForeignKey(Monnaie, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.ref


class Note(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Prefix_Code_Letter(models.Model):
    prefix_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prefix_code