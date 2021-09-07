from django.urls import path
from . import views

urlpatterns = [
    path('apicall/', views.ApiCallView.as_view(), name='apicall'),
]