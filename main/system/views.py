

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

    uuid_user = str(uuid.uuid4())

    location = {
        'province': 'Luanda',
        'municipality': 'Luanda',
        'community': 'Samba',
        'neighborhood': 'Morro-Bento',
        'street': 'Jackson Lar',
        'house': 129
    }

    person_data = {
        'id': uuid_user,
        'first_name': 'Sami',
        'last_name': 'Sabino',
        'age': 25,
        'location': location,
    }

    user_data = {
        'id': uuid_user,
        'email': 'samisabino@gmail.com',
        'password': generate_password_hash('123456', method='sha256')
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
    #db.child('tokens').push(token_user)

    return render(request, 'register.html')


def users_view(request):

    return render(request, 'users.html')
