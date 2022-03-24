

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from firebase.views import db, users_ref, persons_ref, tokens_ref
import jwt
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Create your views here.


def index(request):

    return render(request, 'index.html')


def login_view(request):

    return render(request, 'login.html')


def register_view(request):

    if request.method == 'POST':

        streets = {
            0: 'Jorge Miguel',
            1: 'Mangueiras',
            2: 'Gurgel Santos'
        }

        uuid_user = str(uuid.uuid4())

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')

        street = request.POST.get('street')
        house = request.POST.get('house')

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        designation = request.POST.get('designation')

        if password != confirm_password:

            password_error = 'As passwords não coincidem!'

            return render(request, 'register.html', {
                'message': password_error
            })

        else:

            password_hash = generate_password_hash(password, method='sha256')
            check_street = False

            if designation == 'resident':
                for i in streets:
                    if street == streets[i]:
                        check_street = True

                if check_street:

                    resident_data = {
                        'id': uuid_user,
                        'street': street,
                        'house': house,
                        'status': False
                    }

                    db.child('resident').push(resident_data)

                else:
                    street_not_exists = 'Essa rua não existe. Tente novamente ou consulte um funcionário do condomínio.'

                    return render(request, 'register.html', {
                        'message': street_not_exists
                    })

            elif designation == 'visitor':

                visitor_data = {
                    'id': uuid_user,
                    'street': street,
                    'house': house,
                }

                db.child('visitor').push(visitor_data)

            """ location = {

                'province': 'Luanda',
                'municipality': 'Luanda',
                'community': 'Samba',
                'neighborhood': 'Morro-Bento',
                'street': request.POST.get('street'),
                'house': request.POST.get('house'),
            } """

            person_data = {

                'id': uuid_user,
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': birth_date,
                # 'location': location,
            }

            user_data = {
                'id': uuid_user,
                'email': email,
                'password': password_hash
            }

            # JWT authentication
            """ token_user = str(jwt.encode({
                'person_data': person_data,
                'user_data': user_data,
            },

                'condsys_token'
            )) """

            db.child('person').push(person_data)
            db.child('users').push(user_data)
            # db.child('tokens').push(token_user)

    return render(request, 'register.html')


def users_view(request):

    return render(request, 'users.html')
