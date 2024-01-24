import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie,  Country, Director

def validateFields(data):
    requiredFields = [field.name for field in Movie._meta.get_fields()]
    for field in requiredFields:
        if field not in data or data[field] is None or data[field] == '':
            return JsonResponse({'result': False, 'data': f'{field} cannot be blank or null'})

@csrf_exempt
def movies(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            validateFields(data)
            directorName = data['director']
            director, newDirector = Director.objects.get_or_create(name=directorName)

            countryName = data['country']
            country, newCountry = Country.objects.get_or_create(name=countryName)
            
            newMovie = Movie(
                title = data['title'],
                year = data['year'],
                studio = data['studio'],
                country = country
            )
            newMovie.save()

            newMovie.directors.add(director)
            newMovie.save()

            return JsonResponse({'result': True, 'data': 'Movie created successfully', 'movie': {
                'id': newMovie.id,
                'title': newMovie.title,
                'year': newMovie.year,
                'country': newMovie.country.name,
                'directors': [director.name for director in newMovie.directors.all()],
                'studio': newMovie.studio
            }})
        elif request.method == 'GET':
            movies = Movie.objects.all()
            data = [{'id': movie.id,
                    'title': movie.title,
                    'year': movie.year,
                    'country': {'id': movie.country.id, 'name': movie.country.name} if movie.country else None,
                    'directors': [{'id': director.id, 'name': director.name} for director in movie.directors.all()],
                    'studio': movie.studio} for movie in movies]
            return JsonResponse({'result': True, 'data': data})
        else:
            return JsonResponse({'result': False, 'data': 'Invalid HTTP method'})
    except json.JSONDecodeError:
        return JsonResponse({'result': False, 'data': 'Invalid data, please provide a string or a number'})
    except Exception as e:
        return JsonResponse({'result': False, 'data': str(e)})

@csrf_exempt
def movieOperations(request, movieId):

    try:
        movie = get_object_or_404(Movie, id=movieId)
        if request.method == 'GET':
            data = {
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'country': {'id': movie.country.id, 'name': movie.country.name} if movie.country else None,
                'directors': [{'id': director.id, 'name': director.name} for director in movie.directors.all()],
                'studio': movie.studio
            }
            return JsonResponse({'result': True, 'data': data})

        elif request.method == 'DELETE':
            movie.delete()

        elif request.method == 'PUT':
            data = json.loads(request.body.decode('utf-8'))
            
            validateFields(data)

            for fieldName, newValue in data.items():
                if fieldName == 'directors':

                    directors = [Director.objects.get_or_create(name=directorName)[0] for directorName in newValue]
                    getattr(movie, fieldName).set(directors)
                else:
                    setattr(movie, fieldName, newValue)

            movie.save()

            movies = Movie.objects.all()
            data = [{'id': m.id,
                    'title': m.title,
                    'year': m.year,
                    'country': m.country.name if m.country else None,
                    'directors': [director.name for director in m.directors.all()],
                    'studio': m.studio} for m in movies]

            return JsonResponse({'result': True, 'data': data})

        return JsonResponse({'result': True, 'data': data})
    except json.JSONDecodeError:
        return JsonResponse({'result': False, 'data': 'Invalid data, please provide a string or a number'})
    except Exception as e:
        return JsonResponse({'result': False, 'data': str(e)})


@csrf_exempt
def moviesDirector(request, directorId):
    try:
        try:
            directorId = int(directorId)
        except ValueError:
            return JsonResponse({'result': False, 'data': 'Invalid character, please enter a valid number'})
        director = Director.objects.get(id=directorId)

        movies = Movie.objects.filter(directors=director)

        movie = [
            {
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'country': movie.country.name,
                'studio': movie.studio
            }
            for movie in movies
        ]
        return JsonResponse({'result': True,'director':director.name, 'movies': movie})
    except Director.DoesNotExist:
        return JsonResponse({'result': False, 'data': f'Director with ID "{directorId}" not found'})
    except Exception as e:
        return JsonResponse({'result': False, 'data': str(e)})

@csrf_exempt
def moviesByCountry(request, countryId):
    try:
        if request.method == 'GET':
            
            country = get_object_or_404(Country, id=countryId)
            
            movies = Movie.objects.filter(country=country)
            movieData = [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'year': movie.year,
                    'country': {'id': movie.country.id, 'name': movie.country.name} if movie.country else None,
                    'directors': [{'id': director.id, 'name': director.name} for director in movie.directors.all()],
                    'studio': movie.studio
                }
                for movie in movies
            ]

            return JsonResponse({'result': True, 'data': movieData})
    except Country.DoesNotExist:
        return JsonResponse({'result': False, 'data': f'Country with ID "{countryId}" not found'})
    except Exception as e:
        return JsonResponse({'result': False, 'data': str(e)})

