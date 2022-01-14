from django.urls import path
from transfert import views

urlpatterns = [
    path('transfert/', views.transfert, name='transfert'),
    path('informations_client/', views.nouveau_client, name='nouveau_client'),
    path('informations_receveur/<int:customer_pk>', views.nouveau_receveur, name='nouveau_receveur'),
    path('nouveau_transfert/<int:customer_pk>/<int:receveur_pk>', views.nouveau_transfert, name='nouveau_transfert'),
    path('edit_transfert/<int:transfert_pk>', views.edit_transfert, name='edit_transfert'),
    path('delete_transfert/<int:transfert_pk>', views.delete_transfert, name='delete_transfert'),
    path('print_transfert/<int:transfert_pk>', views.print_transfert, name='print_transfert'),

    path('client/', views.client, name='client'),
    path('codes/', views.prefixe_code, name='prefixe_code'),

    path('situation_comptable/', views.situation_comptable, name='situation_comptable'),
    path('situation_comptable_du_jour/', views.situation_comptable_du_jour, name='situation_comptable_du_jour'),
    path('print_situation_comptable_du_jour/', views.print_situation_comptable_du_jour, name='print_situation_comptable_du_jour'),
    path('search_situation_comptable1/', views.search_situation_comptable1, name='search_situation_comptable1'),
]