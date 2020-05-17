from django.db import models

# Create your models here.

DAY_CHOICES = (
    ('L', 'Lundi'),
    ('MA', 'Mardi'),
    ('ME', 'Mercredi'),
    ('J', 'Jeudi'),
    ('V', 'Vendredi'),
    ('S', 'Samedi'),
    ('D', 'Dimanche')
)
STATUS_CHOICES = (
    ('DE', 'Defaut'),
    ('EX', 'Exceptionnel')
)


class Adresse(models.Model):
    rue = models.CharField(max_length=100)
    numero = models.IntegerField()
    ville = models.CharField(max_length=100)
    codePostale = models.IntegerField()
    pays = models.CharField(max_length=100)

    def __str__(self):
        return self.rue


class Contact(models.Model):
    telephone = models.PositiveIntegerField()
    email = models.EmailField()
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Horaire(models.Model):
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, default='DE')
    jour = models.CharField(choices=DAY_CHOICES, max_length=2)
    heureOuverture = models.TimeField(help_text="Utilisez le format \"xx:xx\" s'il vous plait.")
    heureFermeture = models.TimeField(help_text="Utilisez le format \"xx:xx\" s'il vous plait.")

    def __str__(self):
        return self.status + ' ' + self.jour