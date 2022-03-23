from django.urls import path

from . import views

#app_name = 'firebase'

urlpatterns = [

    path('login/', views.login_auth, name='login_auth'),
    path('home/', views.index_auth, name='index_auth'),
    path('register_auth/', views.register_auth, name='register_auth'),
    path('upload_file/', views.upload_file, name='upload_file'),

    path('update_user/<str:id_user>', views.update_user, name='update_user'),
    path('delete_user/<str:id_user>', views.delete_user, name='delete_user'),

    path('logout/', views.logout_auth, name='logout_auth'),
]
