from django.contrib import admin
from django.urls import include, path
from myappdjf import views

urlpatterns = [
    # path("", views.test, name="index"),
    path("inscription_chercheur_emploi/", views.inscription_chercheur_emploi, name="inscription_chercheur_emploi"),
    path("inscription_entreprise/", views.inscription_entreprise, name="inscription_entreprise"),

    path('login/', views.Mytoken.as_view(), name='login to us'), 
    path("jobs/", views.Les_annonces_emploi.as_view(), name="les_annonces_emploi"),
    # recommended
    path("rec/", views.recommended.as_view(), name="recommended"),
    
    path("updateProfile/", views.updateProfile, name="page_home_chercheur_emploi"),
    
    path('document/<int:pk>/', views.DetailDocument.as_view(), name='Detail Document'), 
    path('document/', views.ListDocument.as_view(), name='List Document'), 

    path('lm/<int:pk>/', views.DetailLangueMaitrise.as_view(), name='Detail LM'), 
    path('lm/', views.ListLangueMaitrise.as_view(), name='List LM'), 
  
]
