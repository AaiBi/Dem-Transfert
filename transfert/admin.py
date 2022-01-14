from django.contrib import admin
from transfert.models import Note, Transfert, Monnaie, Client, Receveur

admin.site.register(Note)
admin.site.register(Transfert)
admin.site.register(Monnaie)
admin.site.register(Client)
admin.site.register(Receveur)
