# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from stepsapp.forms import UserForm, MembersForm, StepsForm
from django.db import IntegrityError
from django.db.models import Sum, Avg, Count
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

from stepsapp.models import Contact, Stepslog, Members, Events

import forms
import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


def RegisterView(request):

    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        msg = ' method post '
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        members_form = MembersForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and members_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            msg = msg + ', form saved '
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            members = members_form.save(commit=False)
            members.username = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
              #  profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            members.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            email_text = 'Thanks for registering with us. Please do not reply to this email. '
            email_text = email_text + 'Please make sure to walk every day and enter you steps count to this site. '
            email_text = email_text + 'If you have to reset the password, please use Reset Password link on the login page.'
            email_text = email_text + 'Thanks!'

            email = EmailMessage('Welcome to iWalk.', email_text, to=[user.email])
            email.send()

            email_text = 'Please check.'
            email = EmailMessage('New Account Created On iWalk.', email_text, to=['munir@noorali.com'])
            email.send()

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            msg = msg + ', no valid '
            print user_form.errors, members_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        msg = 'method not post'
        user_form = UserForm()
        members_form = MembersForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'members_form': members_form, 'registered': registered, 'msg': msg},
            context)


@login_required
def StepsView(request):
    # Get the context from the request.
    context = RequestContext(request)

    member = Members.objects.get(username=request.user)

    event = Events.objects.get(status='Active')

    #steps_sum = Stepslog.objects.filter(username=request.user).aggregate()
    steps_info = Stepslog.objects.filter(username=request.user).aggregate(avg=Avg('steps'), sum=Sum('steps'))

    group_members = Members.objects.filter(groupname=member.groupname).values_list('username')
    group_steps_info = Stepslog.objects.filter(username__in=group_members).aggregate(avg=Avg('steps'), sum=Sum('steps'))

    msg = ' '
    # A HTTP POST?
    if request.method == 'POST':
        # msg = ' method post '
        steps_form = StepsForm(data=request.POST, files=request.FILES)
     
        # Have we been provided with a valid form?
        if steps_form.is_valid():

            # Save the new record to the database.
            stepslog = steps_form.save(commit=False)
            stepslog.username = request.user
            stepslog.eventname = event.eventname

            try:
                stepslog.save()
            except IntegrityError as e:
                msg = 'You have already entered data for this date. Try a different date.'
                return render_to_response('enter_steps.html', {'steps_form': steps_form, 
                    'msg': msg, 'member': member, 'event': event, 'steps_info': steps_info,
                    'group_steps_info': group_steps_info}, context)

            steps_info = Stepslog.objects.filter(username=request.user).aggregate(avg=Avg('steps'), sum=Sum('steps'))
            group_steps_info = Stepslog.objects.filter(username__in=group_members).aggregate(avg=Avg('steps'), sum=Sum('steps'))
            steps_form = StepsForm()
            msg = 'Record Saved.'
            # msg = ' method post, and saved '
            # Now call the index() view.
            # The user will be shown the homepage.
     #       return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            # msg = ' not valid'
            print steps_form.errors

    else:
        # If the request was not a POST, display the form to enter details.
        # msg = ' not post '
        steps_form = StepsForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render_to_response('enter_steps.html', {'steps_form': steps_form, 'msg': msg, 
        'member': member, 'event': event, 'steps_info': steps_info, 'group_steps_info': group_steps_info}, context)

@login_required
def StepsList(request):
    # Get the context from the request.
    context = RequestContext(request)
    msg = ''

    curr_date = datetime.date.today() + datetime.timedelta(days=1)
    event = Events.objects.get(status='Active')
    diff_days = curr_date - event.startdate
    member = Members.objects.get(username=request.user)
    steps_list = Stepslog.objects.filter(username=request.user).order_by('-stepsdate')

    steps_count = Stepslog.objects.filter(username=request.user).count()

    missing_steps = diff_days.days - steps_count - 1

    # Render the form with error messages (if any).
    return render_to_response('steps_list.html', {'steps_list': steps_list, 'msg': msg, 'member': member,
        'event': event, 'missing_steps': missing_steps, 'diff_days': diff_days,
        'steps_count': steps_count}, context)

@login_required
def Profile(request):
    context = RequestContext(request)
    u = User.objects.get(username=request.user)
    member = Members.objects.get(username=request.user)
    try:
        up = Members.objects.get(user=request.user)
    except:
        up = None

    event = Events.objects.get(status='Active')

    return render_to_response('profile.html', {'u': u, 'member': member, 'event': event}, context)
