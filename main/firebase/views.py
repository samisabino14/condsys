
import pyrebase
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout


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


def index_auth(request):

    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = auth.sign_in_with_email_and_password(email, password)
    
    except:
        message = "Invalid Credentials! Please Check your Data"
        return render(request, "login_auth.html", {"message": message})

    request.session = user
    print(request.session)

    login(request, user)

    return render(request, "auth.html", {"email": email})


def login_auth(request):
    return render(request, 'login_auth.html')


def register_auth(request):

    if request.method == 'POST':

        email = input('Email: ')
        password = input('Password: ')
        confirm_password = input('Confirm Password: ')

        if password == confirm_password:

            try:
                auth.create_user_with_email_and_password(email, password)
                print('User created successfully')
                return HttpResponseRedirect(reverse('index_auth'))

            except:
                print('Email exists')
                return HttpResponseRedirect(reverse('register_auth'))

        else:
            print('Password differs')
            return HttpResponseRedirect(reverse('register_auth'))

    return render(request, 'register_auth.html')


def upload_file(request):

    # filename = input('Enter filename to upload: ')
    filename_cloud = input('Enter filename on cloud: ')

    # UPLOAD file

    """ storage.child(filename_cloud).put(filename)

    print(storage.child(filename_cloud).get_url(None)) """

    # DOWNLOAD file

    storage.child(filename_cloud).download("", "download_1.txt")

    return render(request, 'upload_file.html')


def update_user(request, id_user):

    for person in persons_ref.each():
        for user in users_ref.each():

            if person.val()['id'] == id_user:
                #print(person.val()['first_name'])
                #print(person.key())

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

    for user in users_ref.each():

        if user.val()['id'] == id_user:

            print(db.child('person').child(user.val()['id']))

            return HttpResponseRedirect(reverse('index'))

    return render(request, 'delete_user.html')


def logout_auth(request):

    try:
        del request.session['uid']
    except:
        pass

    return render(request, 'index.html')
