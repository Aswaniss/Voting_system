from django.urls import path
from . import views

urlpatterns = [
    path('vote/', views.vote, name='vote'),
    path('vote_summary',views.vote_summary,name='vote_summary')
]
