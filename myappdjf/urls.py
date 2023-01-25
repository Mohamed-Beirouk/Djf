from django.contrib import admin
from django.urls import include, path
from myappdjf import views

urlpatterns = [
    # path("", views.index, name="index"),
    
    path('login/', views.Mytoken.as_view(), name='login to us'), 
    path("jobs/", views.Les_annonces_emploi.as_view(), name="les_annonces_emploi"),
    path("inscription_chercheur_emploi/", views.inscription_chercheur_emploi, name="inscription_chercheur_emploi"),
    path("inscription_entreprise/", views.inscription_entreprise, name="inscription_entreprise"),
    path("updateProfile/", views.updateProfile, name="page_home_chercheur_emploi"),
    


    # # les administrateurs
    # path("connexion_administrateur/", views.connexion_administrateur, name="connexion_administrateur"),
    # path("rien/", views.rien, name="rien"),
    # path("liste_chercheurs_emploi/", views.liste_chercheurs_emploi, name="liste_chercheurs_emploi"),
    # path("supprimer_un_chercheur_emploi/<int:myid>/", views.supprimer_un_chercheur_emploi, name="supprimer_un_chercheur_emploi"),
    # path("entreprises_non_confirmer/", views.entreprises_non_confirmer, name="entreprises_non_confirmer"),
    # path("entreprises_confirmer/", views.entreprises_confirmer, name="entreprises_confirmer"),
    # path("entreprises_rejeter/", views.entreprises_rejeter, name="entreprises_rejeter"),
    # path("tous_les_entreprises/", views.tous_les_entreprises, name="tous_les_entreprises"),
    # path("change_status/<int:myid>/", views.change_status, name="change_status"),
    # path("supprimer_entreprise/<int:myid>/", views.supprimer_entreprise, name="supprimer_entreprise"),
    # path("stat/", views.stat, name="stat"),
     
    # # les chercheur d'emploi
    # path("connexion_chercheur_emploi/", views.connexion_chercheur_emploi, name="connexion_chercheur_emploi"),
    # path("page_home_chercheur_emploi/", views.page_home_chercheur_emploi, name="page_home_chercheur_emploi"),
    # path("deconnecter/", views.deconnecter, name="deconnecter"),
    # # path("les_annonces_emploi/", views.les_annonces_emploi, name="les_annonces_emploi"),
    # path("detail_annonce/<int:myid>/", views.detail_annonce, name="detail_annonce"),
    # path("deposer_pour_emploi/<int:myid>/", views.deposer_pour_emploi, name="deposer_pour_emploi"),
    # path("languesmaitrise/", views.languesmaitrise, name="languesmaitrise"),
    # # les entreprises
    # path("connexion_entreprise/", views.connexion_entreprise, name="connexion_entreprise"),
    # path("page_home_entreprise/", views.page_home_entreprise, name="page_home_entreprise"),
    # path("publier_annonce/", views.publier_annonce, name="publier_annonce"),
    # path("liste_des_annonces/", views.liste_des_annonces, name="liste_des_annonces"),
    # path("modifier_annonce/<int:myid>/", views.modifier_annonce, name="modifier_annonce"),
    # path("logo_entreprise/<int:myid>/", views.logo_entreprise, name="logo_entreprise"),
    # path("les_interesses/", views.les_interesses, name="les_interesses"),

    # # les visiteurs
    # path("freelancer/", views.freelancerHomePage, name="freelancer"),
    # path("detailfreelancer/<int:id>/", views.detailfreelancer, name="detailfreelancer"),
    
]
