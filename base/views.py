from django.shortcuts import render,redirect
from django.db.models import Q
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from.tasks import *
from django.http import HttpResponseRedirect
# Create your views here.


def homepage(request):
    related_services = Service.objects.all()[:3]
    hearted = request.session.get('hearted')
    if hearted:
        all_ids = request.session['hearted'].split(" ")
        hearted = [int(i) for i in all_ids]
    context = {
        "related_services":related_services,
        "hearted":hearted
        }

    return render(request, "homepage.html", context)

def services_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    services = Service.objects.filter(title__icontains=q)
    hearted = request.session.get('hearted')
    if hearted:
        all_ids = request.session['hearted'].split(" ")
        hearted = [int(i) for i in all_ids]
    context = {
        "services":services,
        "q": q,
        "hearted":hearted
        }

    return render(request, "services_page.html", context)

def service_detail_page(request, id):
    service = Service.objects.get(id=id)
    related_services = Service.objects.all()[:3]
    hearted = request.session.get('hearted')
    if hearted:
        all_ids = request.session['hearted'].split(" ")
        hearted = [int(i) for i in all_ids]
    context = {
        "service":service,
        "hearted":hearted,
        "related_services":related_services
        }
    return render(request, "service_detail_page.html", context)

def heart_btn_clicked(request):
    id = request.GET.get('id') if request.GET.get('id') != None else ''
    id = int(id)
    if id:
        if request.session.get('hearted'):
            all_ids = request.session['hearted'].split(" ")
            all_ids_array = sorted(set([int(i) for i in all_ids]))
            request.session['hearted'] = ' '.join([str(i) for i in all_ids_array])
            request.session.modified = True


            if id in all_ids_array:
                request.session['hearted'] = ' '.join([str(i) for i in all_ids_array if i != id])
                request.session.modified = True
                return JsonResponse({'message': request.session['hearted']})
            else:
                request.session['hearted'] = f"{request.session['hearted']} {id}"
                request.session.modified = True
                return JsonResponse({'message': request.session['hearted']})
        else:
            request.session['hearted'] = f"{id}"
            request.session.modified = True
            return JsonResponse({'message': request.session['hearted']})
    else:
        return JsonResponse({'message': 'SEND ID!'})
    


def leads_collector(request, service_id):
    if request.method == "POST":
        service = Service.objects.get(id=service_id)
        name = request.POST.get('name__input')
        email = request.POST.get('email__input')
        phone = request.POST.get('phone__input')
        desc = request.POST.get('desc__input')
        # try:
        Leads.objects.create(
            phone_number = phone,
            name = name,
            email_address = email,
            desc = desc,
            service_related = service
        )
        for_service = Service.objects.get(id=service_id)
        mail_sender(for_service.email_address_associate, for_service.email_address_password, for_service.receiver_email, for_service.email_text_to_send_user, email, name, for_service.title, phone,desc)
        messages.success(request, 'Successfully Recieved!')
        # except Exception as e:
        #     messages.success(request, e)

    return redirect("service_detail_page", service_id)

def newsletter_emails_collector(request):
    if request.method == "POST":
        email = request.POST.get('email_newsletter__input')
        # try:
        NewsLetterEmail.objects.create(
            email_address = email,
        )

        messages.success(request, 'Successfully Recieved!')
        # except Exception as e:
        #     messages.success(request, e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))