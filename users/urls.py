from django.urls import path

from users.views import registration_view, index, logout_view, login_view, account_view, must_authenticate_view

app_name = 'users'
urlpatterns = [
    path('', index, name='index'),
    path('detail/', account_view, name='account'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('must_authenticate/', must_authenticate_view, name='must_authenticate'),
    path('register/', registration_view, name='registration_view'),

]