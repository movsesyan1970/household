from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



from account.forms import CreateUserForm,LoginUserForm,HouseUserForm
from account.models import HouseUser,BasicAddress,MainHouse



def _index(request):
    template=loader.get_template('account/index.html')
    context={}
    return HttpResponse(template.render(context))


def self_register(request):
    if request.method == 'POST':
	in_form=CreateUserForm(request.POST)
	if in_form.is_valid():
	    email = in_form.cleaned_data['email']
	    username = email
	    password = in_form.cleaned_data['password']
	    new_user = User.objects.create_user(
		username,
		email,
		password
	    )
	    user = authenticate(username=username, password=password)    
	    login(request,user)
	    return HttpResponseRedirect('account/')
	else:
	    template = loader.get_template('account/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))
    else:
	in_form = CreateUserForm()
	template = 'account/create_user.html'
	context = {'form':in_form}
	return render(request,template,context)



def log_in(request):
    if request.method == 'POST':
	user = authenticate(
		username = request.POST['email'], 
		password = request.POST['password'])
	if user is not None:
	    login(request,user)
	    return HttpResponseRedirect('/account/')
	else:
	    return HttpResponse('Wrong Credentials')
    else:
	login_form = LoginUserForm()
	template = 'account/login.html'
	context = {'form':login_form}
	return render(request,template,context)

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def user_home(request):
    main_user = request.user
    template = loader.get_template("account/home.html")
    context = dict()

#    context['h_user_form'] = h_user_form
    if hasattr(main_user,'house_user'):
	context['h_user'] = main_user.house_user
    else:
	context['h_user'] = None
    return HttpResponse(template.render(context))



@login_required
def edit_user(request,in_user_id):
    main_user = User.objects.get(id = in_user_id)
    context = dict()
    context['user'] = main_user
    template = 'account/home.html'
    if request.method == 'POST':
	context['edit_form'] = False
	in_form = HouseUserForm(request.POST)
	if in_form.is_valid():

	    main_user.first_name = in_form.cleaned_data['first_name']
	    main_user.last_name = in_form.cleaned_data['last_name']
	    main_user.save()
	    if hasattr(main_user,'house_user'):
		house_user = main.user.house_user
		house_user.dob = in_form.cleaned_data['dob'],
		house_user.sex = in_form.cleaned_data['sex'],
#		house_user.mh_superuser = in_form.cleaned_data['mh_superuser'],
		house_user.ssn_13 = in_form.cleaned_data['ssn_13'],
		house_user.ssn_45 = in_form.cleaned_data['ssn_45'],
		house_user.ssn_69 = in_form.cleaned_data['ssn_69'],
		house_user.save()
		context['h_user'] = main_user.house_user
	    else:
		house_user = HouseUser.objects.create(
		user = main_user,
		dob = in_form.cleaned_data['dob'],
		sex = in_form.cleaned_data['sex'],
#		mh_superuser = in_form.cleaned_data['mh_superuser'],
		ssn_13 = in_form.cleaned_data['ssn_13'],
		ssn_45 = in_form.cleaned_data['ssn_45'],
		ssn_69 = in_form.cleaned_data['ssn_69'],
		)
		context['h_user'] = None
	    return HttpResponseRedirect("/account")
	else:
	    template = loader.get_template('account/err_template.html')
	    return HttpResponse(template.render({'form':in_form}))

    else:
	context['edit_form'] = True
	if hasattr(main_user,'house_user'):
	    context['h_user'] = main_user.house_user
	    h_user_form = HouseUserForm(instance = main_user.house_user)
	else:
	    context['h_user'] = None
	    h_user_form = HouseUserForm()

	context['h_user_form'] = h_user_form
	return render(request,template,context)

