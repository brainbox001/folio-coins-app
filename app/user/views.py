from .models import User, Referral
from .forms import UserCreationForm, UserLoginForm, UserVerifyEmail

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .tasks import send_verification_email

from random import choices
import json

VERIFICATION_CODE_NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def register(request):

    if 'user_data' in request.session:
      del request.session['user_data']

    if request.user.is_authenticated:
      pass
      #  return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)


        if form.is_valid():

            user = form.save(commit=False)
            user.email = form.cleaned_data['email'].lower()
            user.referral_id = form.cleaned_data['referral_id'].title()
            user.first_name = form.cleaned_data['first_name'].title()
            user.last_name = form.cleaned_data['last_name'].title()
            user.username = form.cleaned_data['username']
            user.password = form.cleaned_data['password']

            code = ''.join(str(number) for number in choices(VERIFICATION_CODE_NUMBERS, k=6))

            referred_by = request.POST.get('referred_by').title()

            request.session['user_data'] = {
                'email': user.email,
                'password': user.password,
                'referral_id': user.referral_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'code': code
            }

            if referred_by != '':
              try:

                referrer = User.objects.get(referral_id=referred_by)
                referrer_id = referrer.referral_id

                request.session['user_data']['referrer_id'] = referrer_id

              except User.DoesNotExist:
                not_found = f'Referrer with ID "{referred_by}" not found!!'
                response_data = {
                    'success': False,
                    'not_found': not_found
                }
                return JsonResponse(response_data)


            if User.objects.filter(referral_id=user.referral_id).exists():
              error_message = f'Referral ID "{user.referral_id}" already in use. Please choose a different one.'
              response_data = {
                    'success': False,
                    'error_message': error_message
                }
              return JsonResponse(response_data)

            send_verification_email.delay(user.email, code)
            response_data = {
                    'success': True,
                }
            return JsonResponse(response_data)

        else:
          errors = {}
          for field in form.errors:
              errors[field] = form.errors[field][0]
          return JsonResponse({'success': False, 'errors': errors})


    else:
      form = UserCreationForm()
    return render(request, 'user/sign-up.html', {'form': form})
