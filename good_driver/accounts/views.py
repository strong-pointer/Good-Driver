
# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import PermissionDenied
from django.http import Http404
from . import backends
from . import models
from . import forms

def register(request):
    import hashlib

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        ##username is the email
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        street_addr = request.POST['street_address']
        city = request.POST['city']
        zip_code = request.POST['zip_code']
        phone_num = request.POST['phone_num']
        
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
    
        if password==confirm_password:
            if models.Users.objects.filter(email=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect(register)
            
                
            else:
                user = models.Users(email=username, password=password_hash, 
                                         first_name=first_name, last_name=last_name, street_address=street_addr, street_address_2=street_addr, city=city, zip_code=zip_code, phone_number=phone_num, user_type='Driver')
                user.save()
                
                return redirect('done')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        return render(request, 'registration.html')
    
    
def driverHome(request):
    return render(request, 'navigation/driverHome.html')
    

def login(request):
    from datetime import datetime
    
    if request.method == "POST":
        
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        user = backends.CustomAuthBackend.authenticate( username=email, password=password)
        if user is not None:
            auth_login(request, user)
            message = 'You are logged in!'
            messages.info(request, message)
            
            return redirect(user_profile)
        else:
            if models.Users.objects.filter(email=email).exists():
                user_id_queryset = models.Users.objects.filter(email=email).values('user_id')
                ##gets id from query
                user_id = user_id_queryset[0]['user_id']
                CURRENT_TIME = datetime.now()
                new_login_attempt = models.LoginAttempt(user_id = user_id, date_time=CURRENT_TIME, was_accepted=0)
                new_login_attempt.save()
                #models.LoginAttempt.save(user_id=user_obj, date_time=CURRENT_TIME,was_accepted=0)
            
            message = 'Username or Password Incorrect'
            ##saves message to html template
            messages.info(request, message)
            return redirect(login)
    elif request.method == "GET":
        
        return render(request, 'registration/login.html')
    
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        
        return redirect(login)
        
    elif request.method == "GET":
        return render(request, 'registration/logout.html' )
    
def resetPassword(request):
    return render(request, 'resetPassword.html')

def sponsorView(request):
    return render(request, 'sponsorView.html')

def pointChange(request):
    return render(request, 'pointChange.html')

def catalog(request):
    return render(request, 'catalog.html')

def pointHistory(request):
    return render(request, 'pointHistory.html')


def user_profile(request):
    return render(request, 'user_profile.html')

    
def admin_panel(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Admin' type
    elif request.user.user_type == "Admin":
        if request.method == "GET":
            # Give page with button options of letting the admin choose what action they want to take:
                #   - Create Account (Driver, Sponsor, Admin)
                #   - Delete Account (Sponsor)
            return render(request, 'adminPanel.html')
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

def admin_create_account(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Admin' type
    elif request.user.user_type == "Admin":
        if request.method == "GET":
            # Give page with basically a registration page, but with more details available
            return render(request, 'adminCreateAccount.html')
        elif request.method == "POST":
            import hashlib

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            ##username is the email
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            street_addr = request.POST['street_address']
            city = request.POST['city']
            zip_code = request.POST['zip_code']
            phone_num = request.POST['phone_num']
            user_type = request.POST['user_type']
            
            password_hash = hashlib.md5(password.encode()).hexdigest()
            
            if password==confirm_password:
                if models.Users.objects.filter(email=username).exists():
                    messages.info(request, 'Username is already taken')
                    return redirect(admin_create_account)
                else:
                    user = models.Users(email=username, password=password_hash, 
                                            first_name=first_name, last_name=last_name, street_address=street_addr, 
                                            street_address_2=street_addr, city=city, zip_code=zip_code, 
                                            phone_number=phone_num, user_type=user_type)
                    user.save()
                    
                    if user.user_type == 'Admin':
                        adminUser = models.AdminUser(user=user)
                        adminUser.save()
                    elif user.user_type == 'Sponsor':
                        print('here')
                        sponsor = request.POST['sponsor']
                        # Check if the organization exists
                        if models.Sponsor.objects.filter(name=sponsor).exists():
                            organization = models.Sponsor.objects.get(name=sponsor)
                        # if not, make it, if so make it equal to organization
                        else:
                            organization = models.Sponsor(point_value=0.0, name=sponsor)
                            organization.save()

                        sponsorUser = models.SponsorUser(user=user, sponsor=organization)
                        sponsorUser.save()
                    elif user.user_type == 'Driver':
                        # HAD TO MAKE sponsor=-1 SINCE WE SHOULDNT EVEN HAVE THAT FIELD (USELESS)
                        driverUser = models.DriverUser(user=user, sponsor_id=-1)
                        driverUser.save()
                        '''driverSponsorCombo = models.DriverSponsor(user=driverUser, sponsor=Sponsor)
                        driverSponsorCombo.save()'''

                    return redirect('done')
            else:
                messages.info(request, 'Both passwords are not matching')
                return redirect(admin_create_account)
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied
    
# Creates a SPONSOR COMPANY in the sponsor table, NOT a sponsor USER ACCOUNT
def admin_create_sponsor(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Admin' type
    elif request.user.user_type == "Admin":
        if request.method == "GET":
            # Give page with basically a registration page, but with more details available
            return render(request, 'adminCreateSponsor.html')
        elif request.method == "POST":

            sponsor_name = request.POST['name']
            point_value = request.POST['point_value']
            
            # Ensures a new sponsor is being created
            if not models.Sponsor.objects.filter(name=sponsor_name).exists():
                new_sponsor = models.Sponsor(point_value=point_value, name=sponsor_name)
                new_sponsor.save()

                return redirect('done')
            else:
                messages.info(request, 'Sponsor Company Name Already Taken! Please Try a Different Name.')
                return redirect(admin_create_sponsor)
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

def admin_delete_account(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Admin' type
    elif request.user.user_type == "Admin":
        if request.method == "GET":
            # Give page with option to enter a user's info to delete from the db
            return render(request, 'adminDeleteAccount.html')
        elif request.method == "POST":
            username = request.POST['username']

            if request.user.email == username:
                messages.info(request, 'You cannot delete your own account while signed-in to it!')
                return redirect(admin_delete_account)

            if models.Users.objects.filter(email=username).exists():
                # Gets the User object for the specified person
                User = models.Users.objects.get(email=username)

                # Logic block to delete from all exterior (non base-user) tables
                if User.user_type == 'Admin' and models.AdminUser.objects.get(user=User).exists():
                    models.AdminUser.objects.get(user=User).delete()
                elif User.user_type == 'Sponsor' and models.SponsorUser.objects.get(user=User).exists():
                    models.SponsorUser.objects.get(user=User).delete()
                elif User.user_type == 'Driver':
                    if models.DriverSponsor.objects.filter(user=User).exists():
                        models.DriverSponsor.objects.filter(user=User).delete()
                    if models.Points.objects.filter(user=User).exists():
                        models.Points.objects.filter(user=User).delete()
                    if models.DriverUser.objects.get(user=User).exists():
                        models.DriverUser.objects.get(user=User).delete()

                # Delete from base Users table
                User.delete()
                return redirect('done')
            else:
                messages.info(request, 'Username does not exist')
                return redirect(admin_delete_account)
        else: 
            raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

def sponsor_panel(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Sponsor' type
    elif request.user.user_type == "Sponsor":
        if request.method == "GET":
            # Give page with button options of letting the sponsor choose what action they want to take:
                #   - Create Account (Sponsor)
            return render(request, 'sponsorPanel.html')
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

def sponsor_create_account(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Sponsor' type
    elif request.user.user_type == "Sponsor":
        if request.method == "GET":
            # Give page with basically a registration page, but with more details available
            return render(request, 'sponsorCreateAccount.html')
        elif request.method == "POST":
            import hashlib
            Sponsor = models.Sponsor.objects.get(sponsor_id=models.SponsorUser.objects.get(user_id=request.user.user_id).sponsor_id)

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            ##username is the email
            username = request.POST['username']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            street_addr = request.POST['street_address']
            city = request.POST['city']
            zip_code = request.POST['zip_code']
            phone_num = request.POST['phone_num']
            
            password_hash = hashlib.md5(password.encode()).hexdigest()
            if password==confirm_password:
                if models.Users.objects.filter(email=username).exists():
                    messages.info(request, 'Username is already taken')
                    return redirect(sponsor_create_account)
                else:
                    # Add to Users table
                    user = models.Users(email=username, password=password_hash, 
                                            first_name=first_name, last_name=last_name, street_address=street_addr, 
                                            street_address_2=street_addr, city=city, zip_code=zip_code, 
                                            phone_number=phone_num, user_type="Sponsor")
                    user.save()

                    # Get user id just created from auto-increment, and create a new entry matching it inside sponsor users table
                    sponsorUser = models.SponsorUser(user=user, sponsor=Sponsor)
                    sponsorUser.save()
                    
                    return redirect('done')
            else:
                messages.info(request, 'Both passwords are not matching')
                return redirect(sponsor_create_account)
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

# Removes driver from the sponsor
def sponsor_remove_driver(request):
    # Denies permission to ANYONE who is NOT signed in
    if request.user.is_anonymous == True:
        raise PermissionDenied
    # Logic for if a user is signed in AND is of the 'Sponsor' type
    elif request.user.user_type == "Sponsor":
        if request.method == "GET":
            # Give page with basically a registration page, but with more details available
            return render(request, 'sponsorRemoveDriver.html')
        elif request.method == "POST":
            username = request.POST['username']

            # Checks that this user even exists within the shared table | Also counts as a check that the user is of "Driver" considering only drivers should be in this table
            if models.Users.objects.filter(email=username).exists() and models.DriverUser.objects.filter(user=models.Users.objects.get(email=username)).exists():
                # Gets the DriverUser object for the specified person
                User = models.DriverUser.objects.get(user=models.Users.objects.get(email=username))
                # Gets the User object for the requester (Sponsor user, not typed tho; just plain User)
                RequestingUser = models.Users.objects.get(email=request.user.email)

                # Make sure that exisiting user that sponsor wants to remove is within THEIR organization already
                #    by checking the bridge table entity Driver_Sponsor
                if not models.DriverSponsor.objects.filter(user=User, sponsor=models.SponsorUser.objects.get(user=RequestingUser).sponsor).exists():
                    messages.info(request, 'Username given is not associated with your Organization!')
                    return redirect(sponsor_remove_driver)

                # Delete all records from DriverSponsor table that has the specified user associated with the sponsor's sponsor id
                models.DriverSponsor.objects.filter(user=User, sponsor_id=models.SponsorUser.objects.get(user=RequestingUser).sponsor).delete()
                return redirect('done')
            else:
                messages.info(request, 'Username does not exist')
                return redirect(sponsor_remove_driver)
        else: raise Http404
    # Returns 403 Error (Permission Denied)    
    else: raise PermissionDenied

def application(request):
    from datetime import datetime
    if request.user.is_anonymous == True:
        messages.info(request, 'You must be logged in to apply to a sponsor')
        return redirect(login)
    elif request.user.user_type == 'Driver':
        if request.method == "GET":
            ## gets sponsor form from forms.py and puts it in application.html
            form = forms.SponsorForm()
            return render(request,'application.html', {'form': form})
        elif request.method == "POST":
            user_id = request.user.user_id
            user_obj = models.Users.objects.get(user_id=user_id)
            sponsor_obj = models.Sponsor.objects.get(name=request.POST['sponsor_name'])
            print(sponsor_obj)
            sponsor_id = getattr(sponsor_obj, 'sponsor_id')
            print(sponsor_id)
            ##prevents duplicate application while original app is still pending
            if(models.DriverApplication.objects.filter(driver=user_id,sponsor=sponsor_id,status='Pending').exists()):
                messages.info(request,"You already applied to " + request.POST['sponsor_name'])
                return redirect(application)
            if(models.DriverSponsor.objects.filter(user=user_id,sponsor=sponsor_obj).exists()):
                messages.info(request,"You are already sponsored by " + request.POST['sponsor_name'])
                return redirect(application)

            CURRENT_TIME = datetime.now()
            

            ##gets id from query
            
            new_Application = models.DriverApplication(driver=user_obj,sponsor=sponsor_obj,date_time=CURRENT_TIME,status="Pending",reason=None)
            new_Application.save()
            messages.info(request, 'You applied successfully')
            return redirect(application)
    elif(request.user.user_type == "Sponsor"):
        if request.method == "GET":
            user_sponsor_obj = models.SponsorUser.objects.get(user_id=request.user.user_id)
            sponsor_id = getattr(user_sponsor_obj, 'sponsor_id')
            sponsor_obj = models.Sponsor.objects.get(sponsor_id=sponsor_id)
            sponsor_name = getattr(sponsor_obj, 'name')
            
            ##select related gets the necessary Users objects so the database only needs to be queried once
            app_list = models.DriverApplication.objects.select_related('driver').filter(sponsor=sponsor_obj,status='Pending')
            
            list_of_apps = []
            for app in app_list:
                first_name = app.driver.first_name
                last_name = app.driver.last_name
                street_address = app.driver.street_address
                city = app.driver.city
                zip_code = app.driver.zip_code
                phone_number = app.driver.phone_number
                new_dict = {'first_name':first_name,'last_name':last_name,'street_address':street_address,'city':city,'zip_code':zip_code, 'phone_number':phone_number, 'status':app.status, 'reason':app.reason, 'date_time':app.date_time, 'application_id': app.application_id}
                list_of_apps.append(new_dict)
            
            
            return render(request, 'application.html', {'app_list': list_of_apps, 'sponsor_name':sponsor_name})
        elif request.method == "POST":
            print(request.POST)
            application_obj = models.DriverApplication.objects.select_related('sponsor').get(application_id=request.POST['application_id'])
            print(application_obj.driver)
            print(application_obj.sponsor)
            if(request.POST['decision'] == "Accept"):
                new_DriverSponsor = models.DriverSponsor(user=application_obj.driver, sponsor=application_obj.sponsor)
                new_DriverSponsor.save()
                application_obj.status = "Accepted"
                application_obj.reason = request.POST['reason_input']
                application_obj.save()
                messages.info(request, "Successfully Accepted Application Number " + request.POST['application_id'])
            elif(request.POST['decision'] == "Reject"):
                application_obj.status = "Rejected"
                application_obj.reason = request.POST['reason_input']
                application_obj.save()
                messages.info(request, "Successfully Rejected Application Number " + request.POST['application_id'])

            return redirect(application)

def admin_edit_account(request):
    # Denies permission to anyone who is not signed in as an Admin
    if  request.user.is_anonymous == True or request.user.user_type != "Admin":
        raise PermissionDenied

    both_forms = {"form1": forms.getDriverEmail, "form2": forms.getDriverInfo}

    if request.method == "GET":
        return render(request, 'adminEditAccount.html', both_forms)
    elif request.method == "POST":
        form1 = forms.getDriverEmail(request.POST)
        # make sure the form is valid
        if form1.is_valid():
            target_user_email = form1.cleaned_data['email']
        else:
            target_user_email = request.POST['email']

        #make sure the user exists
        if models.Users.objects.filter(email=target_user_email).exists():
            print(models.Users.objects.filter(email=target_user_email))

            #get the user from the database
            target_user_queryset = models.Users.objects.filter(email=target_user_email).values('email', 'first_name', 'last_name', 'phone_number', 'street_address', 'street_address_2', 'user_type', 'zip_code', 'city')
            target = target_user_queryset[0]

            #this maps the fields from the database to the variables in adminEditAccounts.html
            context_data =  {"form1": forms.getDriverEmail, "form2": forms.getDriverInfo, 'other_email': target['email'], 'other_first_name': target['first_name'], 'other_last_name':target['last_name'], 'other_street_address':target['street_address'], 'other_city':target['city'], 'other_zip_code':target['zip_code'], 'other_phone_number':target['phone_number'], 'other_user_type':target['user_type']}

            #
            #  If the "Update Provided Fields" button is pressed
            #
            if 'updateInfo' in request.POST:
                #get form submission data

                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                street_addr = request.POST['street_address']
                city = request.POST['city']
                zip_code = request.POST['zip_code']
                phone_num = request.POST['phone_number']

                #update queryset for updated info
                if first_name != "":
                    target_user_queryset.update(first_name=first_name)
                    context_data['other_first_name'] = first_name 
                if last_name != "":
                    target_user_queryset.update(last_name=last_name)
                    context_data['other_last_name'] = last_name
                if street_addr != "":
                    target_user_queryset.update(street_address=street_addr)
                    context_data['other_street_address'] = street_addr
                if city != "":
                    target_user_queryset.update(city=city)
                    context_data['other_city'] = city
                if zip_code != "" and zip_code.isnumeric():
                    target_user_queryset.update(zip_code=zip_code)
                    context_data['other_zip_code'] = zip_code
                if phone_num != "":
                    target_user_queryset.update(phone_number=phone_num)
                    context_data['other_phone_number'] = phone_num

        else:
            context_data = both_forms
    
    return render(request, 'adminEditAccount.html', context_data)
