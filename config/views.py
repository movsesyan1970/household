from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from config.forms import AddEditAccountTypeForm,AddAccountAttributeForm,AddVehicleTypeForm
from config.forms import AddDocumentTypeForm
from config.models import AccountType,AccountAttribute,VehicleType,DocumentType

# Create your views here.



@login_required
def view_all_objects(request):
    template = loader.get_template("config/all_objects.html")
    context = dict()
    context['username'] = request.session['user_name']
    return HttpResponse(template.render(context))


@login_required
def manage_acct_type(request):
    acct_types = AccountType.objects.all()
    context = dict()
    template = "config/manage_acct_types.html"
    context['types'] = acct_types
    context['username'] = request.session['user_name']
    return render(request,template,context)


@login_required
def add_acct_type(request):
    if request.method == 'POST':
	in_form = AddEditAccountTypeForm(request.POST)
	if in_form.is_valid():
	    new_type = AccountType.objects.create(
		type_name = in_form.cleaned_data['type_name'],
		brief = in_form.cleaned_data['brief']
	    )
	    if 'description' in in_form.cleaned_data:
		new_type.description = in_form.cleaned_data['description']
		new_type.save()
	    return HttpResponseRedirect("/config/acct_type")
	else:
	    template = loader.get_template('base/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    in_form = AddEditAccountTypeForm()
    template = "config/add_edit_acct_type.html"
    context = {'form':in_form}
    context['username'] = request.session['user_name']
    return render(request,template,context)

@login_required
def edit_acct_type(request,in_type_id):
    acct_type = AccountType.objects.get(pk=in_type_id)
    if request.method == 'POST':
	in_form = AddEditAccountTypeForm(request.POST)
	if in_form.is_valid():
	    acct_type.type_name = in_form.cleaned_data['type_name']
	    acct_type.brief = in_form.cleaned_data['brief']
	    
	    if 'description' in in_form.cleaned_data:
		acct_type.description = in_form.cleaned_data['description']
	    acct_type.save()
	    return HttpResponseRedirect("/config/account/types")
	else:
	    template = loader.get_template('base/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    in_form = AddEditAccountTypeForm(instance=acct_type)
    template = "config/add_edit_acct_type.html"
    context = {'form':in_form}
    context['username'] = request.session['user_name']
    return render(request,template,context)


@login_required
def manage_acct_attribute(request):
    attributes = AccountAttribute.objects.all()
    context = dict()
    template = "config/manage_acct_attributes.html"
    context['attributes'] = attributes
    context['username'] = request.session['user_name']
    return render(request,template,context)


@login_required
def add_acct_attribute(request):
    if request.method == 'POST':
	in_form = AddAccountAttributeForm(request.POST)
	if in_form.is_valid():
	    new_attribute = AccountAttribute.objects.create(
		attribute_name = in_form.cleaned_data['attribute_name'],
		description = in_form.cleaned_data['description']
	    )
	    return HttpResponseRedirect("/config/account/attributes")
	else:
	    template = loader.get_template('base/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    in_form = AddAccountAttributeForm()
    template = "config/add_acct_attribute.html"
    context = {'form':in_form}
    context['username'] = request.session['user_name']
    return render(request,template,context)



@login_required
def manage_vehicle_type(request):
    vehicle_types = VehicleType.objects.all()
    context = dict()
    template = "config/manage_vehicle_types.html"
    context['vehicle_types'] = vehicle_types
    context['username'] = request.session['user_name']
    return render(request,template,context)



@login_required
def add_vehicle_type(request):
    if request.method == 'POST':
	in_form = AddVehicleTypeForm(request.POST)
	if in_form.is_valid():
	    new_attribute = VehicleType.objects.create(
		vehicle_type=in_form.cleaned_data['vehicle_type'],
		description=in_form.cleaned_data['description']
	    )
	    return HttpResponseRedirect("/config/vehicle/types/")
	else:
	    template = loader.get_template('base/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    in_form = AddVehicleTypeForm()
    template = "config/add_acct_attribute.html"
    context = {'form':in_form}
    context['username'] = request.session['user_name']
    return render(request,template,context)

@login_required
def manage_document_type(request):
    document_types = DocumentType.objects.all()
    context = dict()
    template = "config/manage_document_types.html"
    context['document_types'] = document_types
    context['username'] = request.session['user_name']
    return render(request,template,context)




@login_required
def add_document_type(request):
    if request.method == 'POST':
	in_form = AddDocumentTypeForm(request.POST)
	if in_form.is_valid():
	    new_doocument_type = DocumentType.objects.create(
		document_type=in_form.cleaned_data['document_type'],
		description=in_form.cleaned_data['description']
	    )
	    return HttpResponseRedirect("/config/document/types/")
	else:
	    template = loader.get_template('base/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    in_form = AddDocumentTypeForm()
    template = "config/add_document_type.html"
    context = {'form':in_form}
    context['username'] = request.session['user_name']
    return render(request,template,context)
