import pyrebase
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from werkzeug.security import generate_password_hash, check_password_hash

# FIREBASE

firebaseConfig = {
    'apiKey': "AIzaSyDr3VgBa4EQwGCsMfB0O8KR7fh7hor2tgA",
    'authDomain': "condsys-2bd2f.firebaseapp.com",
    'projectId': "condsys-2bd2f",
    'databaseURL': 'https://condsys-2bd2f-default-rtdb.firebaseio.com/',
    'storageBucket': "condsys-2bd2f.appspot.com",
    'messagingSenderId': "90795412914",
    'appId': "1:90795412914:web:6fc5b6b8e4fa3a8167e8ab",
    'measurementId': "G-9XQXM8PS9X"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

persons_ref = db.child('person').get()
tokens_ref = db.child('tokens').get()
users_ref = db.child('users').get()

# Create your views here.

email_manager = 'samisabino14@hotmail.com'


def index_auth(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)

        except:
            message = "Credenciais inválidas. Verifique os seus dados."
            return render(request, "login_auth.html", {"message": message})

        id_session = user['idToken']
        request.session['uid'] = str(id_session)

        idToken = request.session['uid']
        user_info = auth.get_account_info(idToken)
        user_info = user_info['users']
        user_info = user_info[0]

        return render(request, "auth.html", {
            "user_info": user_info,
            'email_manager': email_manager
        })

    elif request.method == 'GET':
        return HttpResponseRedirect(reverse('login_auth'))


def login_auth(request):

    return render(request, 'login_auth.html')


def register_auth(request):

    idToken = request.session['uid']
    user_info = auth.get_account_info(idToken)
    user_info = user_info['users']
    user_info = user_info[0]

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register_auth.html', {
                'message': 'Passwords não coincidem. Tente novamente!'
            })

        try:
            success = auth.create_user_with_email_and_password(
                email, password)

        except:
            return render(request, 'register_auth.html', {
                'message': 'Email existente. Tente outro!'
            })

        print(f"Informação: {str(user_info)}")

        if success:

            return HttpResponseRedirect(reverse('index_auth'))

            """ return render(request, 'auth.html', {
                'message': 'Admin criado com sucesso',
                "user_info": user_info,
                'email_manager': email_manager

            }) """

    return render(request, "register_auth.html", {
        "user_info": user_info,
        'email_manager': email_manager

    })


def upload_file(request):

    # filename = input('Enter filename to upload: ')
    filename_cloud = input('Enter filename on cloud: ')

    # UPLOAD file

    """ storage.child(filename_cloud).put(filename)

    print(storage.child(filename_cloud).get_url(None)) """

    # DOWNLOAD file

    storage.child(filename_cloud).download("", "download_1.txt")

    return render(request, 'upload_file.html')


def view_users(request):

    user_data = []

    for user in users_ref.each():
        user_data.append(user.val())

    return render(request, 'view_users.html', {

        'users': user_data
    })


def view_user_by_id(request, id_user):

    person_data = []
    user_data = []

    for person in persons_ref.each():
        for user in users_ref.each():

            if person.val()['id'] == id_user:
                person_data = person.val()

            if user.val()['id'] == id_user:
                user_data = user.val()

    return render(request, 'view_user_by_id.html', {

        'user_data': user_data,
        'person_data': person_data,
    })


def update_user(request, id_user):

    for person in persons_ref.each():
        for user in users_ref.each():
            if person.val()['id'] == id_user:

                db.child('person').child(person.key()).update({
                    'first_name': 'Sami',
                    'last_name': 'Muongueno',
                })

                if user.val()['id'] == id_user:

                    db.child('users').child(user.key()).update({
                        'email': 'samisabino@gmail.com'
                    })

    return render(request, 'update_user.html')


def delete_user(request, id_user):

    idToken = request.session['uid']
    user_info = auth.get_account_info(idToken)
    user_info = user_info['users']
    user_info = user_info[0]

    for user in users_ref.each():

        if user.val()['id'] == id_user:

            db.child('users').child(user.key()).remove()

            print('Successfully deleted user')

            return render(request, 'auth.html', {
                "user_info": user_info,
                'email_manager': email_manager,
                'message': 'Utilizador removido com sucesso',
            })


def logout_auth(request):

    try:
        del request.session['uid']

    except:
        pass

    return HttpResponseRedirect(reverse('login_auth'))
