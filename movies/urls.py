from django.urls import path
from .views import movieOperations,movies,moviesDirector,moviesByCountry


urlpatterns = [
    path ('<int:movieId>/', movieOperations),
    path ('director/<int:directorId>/', moviesDirector),
    path('', movies),
    path('country/<int:countryId>/', moviesByCountry),
]
