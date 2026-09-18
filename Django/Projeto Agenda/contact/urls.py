from django.urls import path # type: ignore
from contact.views import contact_views, contact_forms, user_forms 

app_name = 'contact'
urlpatterns = [
    path("", contact_views.index, name='index'),
    path('search/', contact_views.search, name='search'),
    path('contact/<int:id>/', contact_views.contact, name='contact'),
    path('contact/create/', contact_forms.create , name='create'),
    path('contact/<int:contact_id>/update/', contact_forms.update, name='update'),
    path('contact/<int:contact_id>/delete/', contact_forms.delete, name='delete'),
    
    path('user/register/', user_forms.register , name='register'),
    path('user/login/', user_forms.user_login , name='user_login'),
    path('user/logout/', user_forms.user_logout , name='user_logout'),
    path('user/update/', user_forms.user_update , name='user_update'),
]
