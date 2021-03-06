from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
import re
import datetime
from transfert.forms import Transfert_Form, Client_Form, Receveur_Form, Prefixe_Code_Form, Note_Form
from transfert.models import Client, Receveur, Monnaie, Transfert, Note


@login_required
def transfert(request):
    transferts = Transfert.objects.all().order_by('-id')
    monnaies = Monnaie.objects.all()
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    date_du_jour = datetime.datetime.today()

    if request.method == 'GET':
        return render(request, 'transfert/transfert.html', {'transferts': transferts, 'monnaies': monnaies, 'clients': clients,
                                                        'receveurs': receveurs, 'date_du_jour': date_du_jour})

    if 'search_code' in request.POST:
        search = request.POST.get('search')
        if Transfert.objects.filter(ref=search):
            monnaies = Monnaie.objects.all()
            clients = Client.objects.all()
            receveurs = Receveur.objects.all()
            transfert_info = get_object_or_404(Transfert, ref=search)
            return render(request, 'transfert/transfert.html',
                          {'transfert_info': transfert_info, 'monnaies': monnaies, 'clients': clients,
                           'receveurs': receveurs})
        else:
            messages.error(request, 'Cet Code n\'existe pas !')
            return render(request, 'transfert/transfert.html')


@login_required
def nouveau_client(request):

    if request.method == 'GET':
        form = Client_Form()
        return render(request, 'client/nouveau_client.html', {'form': form})
    else:
        try:
            if Client.objects.filter(telephone=request.POST.get('telephone')):
                client = get_object_or_404(Client, telephone=request.POST.get('telephone'))
                messages.error(request, 'Ce client existe d??j?? dans votre base de donn??es !')
                return redirect('nouveau_receveur', customer_pk=client.id)
            else:
                form = Client_Form(request.POST)
                form = form.save(commit=False)
                form.save()
                messages.success(request, 'Nouveau client ajout?? avec succ??s !')
                return redirect('nouveau_receveur', customer_pk=form.id)
        except ValueError:
            return render(request, 'client/nouveau_client.html', {'form': form, 'error': 'Mauvaises donn??es saisies !'})


@login_required
def nouveau_receveur(request, customer_pk):
    client = get_object_or_404(Client, pk=customer_pk)
    receveurs = Receveur.objects.all().order_by('-created')
    transferts = Transfert.objects.filter(client_id=customer_pk)

    if 'new_receveur' in request.POST:
        form = Receveur_Form(request.POST)
        form = form.save(commit=False)
        form.save()
        messages.success(request, 'Nouveau receveur ajout?? avec succ??s !')
        return redirect('nouveau_transfert', customer_pk=customer_pk, receveur_pk=form.id)

    if 'select_receveur' in request.POST:
        messages.success(request, 'Receveur s??lectionn?? avec succ??s !')
        return redirect('nouveau_transfert', customer_pk=customer_pk, receveur_pk=request.POST.get('receveur_id'))

    if request.method == 'GET':
        form = Receveur_Form()
        return render(request, 'transfert/nouveau_receveur.html', {'form': form, 'client': client, 'transferts': transferts,
                                                                   'receveurs': receveurs})


@login_required
def nouveau_transfert(request, customer_pk, receveur_pk):
    client = get_object_or_404(Client, pk=customer_pk)
    receveur = get_object_or_404(Receveur, pk=receveur_pk)
    monnaies = Monnaie.objects.all()
    dernier_transfert = Transfert.objects.all().last()
    date_du_jour = datetime.datetime.today()
    if request.method == 'GET':

        if dernier_transfert:
            p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
            s = dernier_transfert.ref
            #on extrait le nombre de la reference
            if re.search(p, s) is not None:
                for catch in re.finditer(p, s):
                    code_last_transfert = catch[0]  # catch is a match object
            #on ajoute 1 au nombre receupere, il sera utilise pour la prochaine reference
            code_last_transfert = int(code_last_transfert) + 1
        else:
            code_last_transfert = 1000
        form = Transfert_Form()
        return render(request, 'transfert/nouveau_transfert.html', {'form': form, 'client': client, 'receveur': receveur,
                                                                    'monnaies': monnaies, 'dernier_transfert': dernier_transfert,
                                                                    'code_last_transfert': code_last_transfert,
                                                                    'date_du_jour': date_du_jour})
    else:
        try:
            form = Transfert_Form(request.POST)
            form = form.save(commit=False)
            if Transfert.objects.filter(ref=form.ref):
                messages.error(request, 'Cette r??f??rence existe d??j?? dans votre base de donn??es, utiliser une autre !')
                return redirect('nouveau_transfert', customer_pk=customer_pk, receveur_pk=receveur.id)
            else:
                form.monnaie = get_object_or_404(Monnaie, id=request.POST.get('monnaie_id'))
                form.receveur = get_object_or_404(Receveur, id=receveur_pk)
                form.client = get_object_or_404(Client, id=customer_pk)
                form.save()
                messages.success(request, 'Nouveau transfert ajout?? avec succ??s !')
                return redirect('transfert')
        except ValueError:
            return render(request, 'transfert/nouveau_transfert.html', {'form': form, 'client': client, 'receveur': receveur,
                                                                        'monnaies': monnaies, 'dernier_transfert':
                                                                            dernier_transfert,
                                                                       'error': 'Mauvaises donn??es saisies !'})


@login_required
def client(request):
    #clients = Client.objects.all()
    if 'research' in request.POST:
        search = request.POST.get('search')
        if Client.objects.filter(telephone=search):
            monnaies = Monnaie.objects.all()
            clients = Client.objects.filter(telephone=search)
            receveurs = Receveur.objects.all()
            transferts = Transfert.objects.all().order_by('-created')
            for client in clients:
                transferts_number = Transfert.objects.filter(client_id=client.id).count()
                return render(request, 'client/client.html',
                              {'transferts': transferts, 'monnaies': monnaies, 'clients': clients,
                               'receveurs': receveurs, 'transferts_number': transferts_number})
        else:
            messages.error(request, 'Cet Client n\'existe pas !')
            return redirect('client')

    return render(request, 'client/client.html')


@login_required
def edit_transfert(request, transfert_pk):
    transfert = get_object_or_404(Transfert, pk=transfert_pk)
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()

    if request.method == 'GET':
        form = Transfert_Form(instance=transfert)
        return render(request, 'transfert/edit_transfert.html',
                      {'transfert': transfert, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                          'form': form})
    else:
        try:
            if 'edit_transfert' in request.POST:
                form = Transfert_Form(request.POST, instance=transfert)
                if form.is_valid():
                    form = form.save(commit=False)
                    #form.client = get_object_or_404(Client, id=request.POST.get('client_id'))
                    form.monnaie = get_object_or_404(Monnaie, id=request.POST.get('monnaie_id'))
                    #form.receveur = get_object_or_404(Receveur, id=request.POST.get('receveur_id'))
                    form.save()
                    messages.success(request, 'Modificatin effectu??e avec succ??s !')
                    return redirect('transfert')

            if 'edit_customer_transfert' in request.POST:
                client = get_object_or_404(Client, pk=request.POST.get('client_id'))
                form = Client_Form(request.POST, instance=client)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.save()
                    messages.success(request, 'Modificatin effectu??e avec succ??s !')
                    return redirect('transfert')

            if 'edit_receveur_transfert' in request.POST:
                receveur = get_object_or_404(Receveur, pk=request.POST.get('receveur_id'))
                form = Receveur_Form(request.POST, instance=receveur)
                if form.is_valid():
                    form = form.save(commit=False)
                    form.save()
                    messages.success(request, 'Modificatin effectu??e avec succ??s !')
                    return redirect('transfert')

        except ValueError:
            return render(request, 'transfert/edit_transfert.html',
                          {'transfert': transfert, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                        'form': form,
                           'error': 'Mauvaises donn??es saisies !'})


@login_required
def delete_transfert(request, transfert_pk):
    transfert = get_object_or_404(Transfert, pk=transfert_pk)
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()

    if request.method == 'GET':
        return render(request, 'transfert/delete_transfert.html',
                      {'transfert': transfert, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies})
    if request.method == 'POST':
        transfert.delete()
        messages.success(request, 'Suppression effectu??e !')
        return redirect('transfert')


@login_required
def print_transfert(request, transfert_pk):
    transfert = get_object_or_404(Transfert, pk=transfert_pk)
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()
    date_du_jour = datetime.datetime.today()

    if request.method == 'GET':
        return render(request, 'transfert/print_transfert.html',
                      {'transfert': transfert, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                        'date_du_jour': date_du_jour})


@login_required
def situation_comptable(request):
    transferts = Transfert.objects.all()
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()

    if request.method == 'GET':
        return render(request, 'situation_comptable/situation_comptable.html',
                      {'transferts': transferts, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies})


@login_required
def situation_comptable_du_jour(request):
    date_du_jour = datetime.datetime.today()
    transferts = Transfert.objects.order_by('created')
    note = Note.objects.all().last()
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()
    number_transferts = Transfert.objects.count()
    total_montant_transfert_dollar = \
    Transfert.objects.filter(monnaie_id=1, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_montant_transfert_euro = \
    Transfert.objects.filter(monnaie_id=2, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_montant_transfert_cfa = \
    Transfert.objects.filter(monnaie_id=3, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_commission_transfert_dollar = \
    Transfert.objects.filter(monnaie_id=1, created__gte=datetime.date.today()).aggregate(Sum('commission'))[
        'commission__sum']
    total_commission_transfert_euro = \
    Transfert.objects.filter(monnaie_id=2, created__gte=datetime.date.today()).aggregate(Sum('commission'))[
        'commission__sum']
    total_commission_transfert_cfa = \
    Transfert.objects.filter(monnaie_id=3, created__gte=datetime.date.today()).aggregate(Sum('commission'))[
        'commission__sum']

    if request.method == 'GET':
        return render(request, 'situation_comptable/situation_comptable_du_jour.html',
                      {'transferts': transferts, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                          'date_du_jour': date_du_jour, 'note': note, 'number_transferts': number_transferts,
                       'total_montant_transfert_dollar': total_montant_transfert_dollar,
                       'total_montant_transfert_cfa': total_montant_transfert_cfa, 'total_montant_transfert_euro':
                       total_montant_transfert_euro, 'total_commission_transfert_dollar': total_commission_transfert_dollar,
                       'total_commission_transfert_euro': total_commission_transfert_euro, 'total_commission_transfert_cfa':
                           total_commission_transfert_cfa})
    if request.method == 'POST':
        form = Note_Form(request.POST)
        form.save()
        messages.success(request, 'Nouvelle note ajout??e avec succ??s !')
        return redirect('situation_comptable_du_jour')


@login_required
def print_situation_comptable_du_jour(request):
    date_du_jour = datetime.datetime.today()
    transferts = Transfert.objects.order_by('id')
    number_transferts = Transfert.objects.filter(created__gte=datetime.date.today()).count()
    total_montant_transfert_dollar = Transfert.objects.filter(monnaie_id=1, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_montant_transfert_euro = Transfert.objects.filter(monnaie_id=2, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_montant_transfert_cfa = Transfert.objects.filter(monnaie_id=3, created__gte=datetime.date.today()).aggregate(Sum('montant'))['montant__sum']
    total_commission_transfert_dollar = Transfert.objects.filter(monnaie_id=1, created__gte=datetime.date.today()).aggregate(Sum('commission'))['commission__sum']
    total_commission_transfert_euro = Transfert.objects.filter(monnaie_id=2, created__gte=datetime.date.today()).aggregate(Sum('commission'))['commission__sum']
    total_commission_transfert_cfa = Transfert.objects.filter(monnaie_id=3, created__gte=datetime.date.today()).aggregate(Sum('commission'))['commission__sum']
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()
    note = Note.objects.all()

    if request.method == 'GET':
        return render(request, 'situation_comptable/print_situation_comptable_du_jour.html',
                      {'transferts': transferts, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                          'note': note, 'date_du_jour': date_du_jour, 'number_transferts': number_transferts,
                       'total_montant_transfert_dollar': total_montant_transfert_dollar,
                       'total_montant_transfert_cfa': total_montant_transfert_cfa, 'total_montant_transfert_euro':
                       total_montant_transfert_euro, 'total_commission_transfert_dollar': total_commission_transfert_dollar,
                       'total_commission_transfert_euro': total_commission_transfert_euro, 'total_commission_transfert_cfa':
                           total_commission_transfert_cfa
                       })


@login_required
def search_situation_comptable1(request):
    clients = Client.objects.all()
    receveurs = Receveur.objects.all()
    monnaies = Monnaie.objects.all()
    date_du_jour = datetime.datetime.today()

    if 'search_one_date' in request.POST:
        search = request.POST.get('date_search')
        note = Note.objects.all()
        transferts = Transfert.objects.filter(created=search).order_by('id')
        number_transferts = Transfert.objects.filter(created=search).count()
        total_montant_transfert_dollar = \
            Transfert.objects.filter(monnaie_id=1, created=search).aggregate(Sum('montant'))[
                'montant__sum']
        total_montant_transfert_euro = \
            Transfert.objects.filter(monnaie_id=2, created=search).aggregate(Sum('montant'))[
                'montant__sum']
        total_montant_transfert_cfa = \
            Transfert.objects.filter(monnaie_id=3, created=search).aggregate(Sum('montant'))[
                'montant__sum']
        total_commission_transfert_dollar = \
            Transfert.objects.filter(monnaie_id=1, created=search).aggregate(Sum('commission'))[
                'commission__sum']
        total_commission_transfert_euro = \
            Transfert.objects.filter(monnaie_id=2, created=search).aggregate(Sum('commission'))[
                'commission__sum']
        total_commission_transfert_cfa = \
            Transfert.objects.filter(monnaie_id=3, created=search).aggregate(Sum('commission'))[
                'commission__sum']

        return render(request, 'situation_comptable/search_situation_comptable1.html',
                      {'transferts': transferts, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                       'search': search, 'note': note,
                       'number_transferts': number_transferts, 'total_montant_transfert_dollar': total_montant_transfert_dollar,
                       'total_montant_transfert_cfa': total_montant_transfert_cfa, 'total_montant_transfert_euro':
                           total_montant_transfert_euro, 'date_du_jour': date_du_jour,
                       'total_commission_transfert_dollar': total_commission_transfert_dollar,
                       'total_commission_transfert_euro': total_commission_transfert_euro,
                       'total_commission_transfert_cfa': total_commission_transfert_cfa})

    if 'search_two_date' in request.POST:
        date_search1 = request.POST.get('date_search1')
        date_search2 = request.POST.get('date_search2')

        note = Note.objects.all()
        transferts = Transfert.objects.filter(created__range=(date_search1, date_search2)).order_by('id')
        number_transferts = Transfert.objects.filter(created__range=(date_search1, date_search2)).count()
        total_montant_transfert_dollar = \
            Transfert.objects.filter(monnaie_id=1, created__range=(date_search1, date_search2)).aggregate(Sum('montant'))[
                'montant__sum']
        total_montant_transfert_euro = \
            Transfert.objects.filter(monnaie_id=2, created__range=(date_search1, date_search2)).aggregate(Sum('montant'))[
                'montant__sum']
        total_montant_transfert_cfa = \
            Transfert.objects.filter(monnaie_id=3, created__range=(date_search1, date_search2)).aggregate(Sum('montant'))[
                'montant__sum']
        total_commission_transfert_dollar = \
            Transfert.objects.filter(monnaie_id=1, created__range=(date_search1, date_search2)).aggregate(Sum('commission'))[
                'commission__sum']
        total_commission_transfert_euro = \
            Transfert.objects.filter(monnaie_id=2, created__range=(date_search1, date_search2)).aggregate(Sum('commission'))[
                'commission__sum']
        total_commission_transfert_cfa = \
            Transfert.objects.filter(monnaie_id=3, created__range=(date_search1, date_search2)).aggregate(Sum('commission'))[
                'commission__sum']

        return render(request, 'situation_comptable/search_situation_comptable1.html',
                      {'transferts': transferts, 'clients': clients, 'receveurs': receveurs, 'monnaies': monnaies,
                    'note': note, 'date_search1': date_search1, 'date_search2': date_search2,
                       'number_transferts': number_transferts, 'total_montant_transfert_dollar': total_montant_transfert_dollar,
                       'total_montant_transfert_cfa': total_montant_transfert_cfa, 'total_montant_transfert_euro':
                           total_montant_transfert_euro, 'date_du_jour': date_du_jour,
                       'total_commission_transfert_dollar': total_commission_transfert_dollar,
                       'total_commission_transfert_euro': total_commission_transfert_euro,
                       'total_commission_transfert_cfa': total_commission_transfert_cfa})