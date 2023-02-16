from django.contrib import admin

# Register your models here

from .models import *


admin.site.register(C_emploi)
admin.site.register(Entreprise)
admin.site.register(Document)
admin.site.register(Travail)
admin.site.register(Langue)
admin.site.register(Notes)
admin.site.register(Visiteur)
admin.site.register(Deposer) 
admin.site.register(LangueMaitrise)






