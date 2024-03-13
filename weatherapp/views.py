import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City
from .forms import CityForm
from geopy.geocoders import Nominatim

# Index View
def index(request):
    # Retrieve all cities from the database
    cities = City.objects.all()
    
    # Initialize the city form
    form = CityForm()
    
    # Initialize a dictionary to store weather data for each city
    weather_data = {}
    
    # Iterate through each city to fetch weather data
    for city in cities:
        # Construct the API URL for the Visual Crossing API
        api_key = 'N8LQGH9JV8CL48S9KN54QASFD'
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&contentType=json&unitGroup=metric&locationMode=single&key={api_key}&locations={city.name}'
        
        # Send a GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Extract weather data for the current day
            current_day_data = {
                'date': data['location']['values'][0]['datetimeStr'],
                'temperature': data['location']['values'][0]['temp'],
                'conditions': data['location']['values'][0]['conditions'],
                'icon': data['location']['currentConditions']['icon']
            }
            
            # Store the weather data in the dictionary
            weather_data[city.name] = current_day_data
        else:
            # Handle API errors by storing an error message
            weather_data[city.name] = {'error': 'Failed to fetch weather data'}
    
    # Check if the form was submitted via POST
    if request.method == 'POST':
        # Bind the submitted data to the form
        form = CityForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Retrieve the city name from the form data
            city_name = form.cleaned_data['name']
            
            # Validate the city name
            valid_city = validate_city(city_name)
            if valid_city:
                # Check if the city already exists in the database
                if City.objects.filter(name=city_name).exists():
                    # Display an error message if the city already exists
                    messages.error(request, f'{city_name} already exists in the list!')
                else:
                    # Save the new city to the database
                    form.save()
                    
                    # Display a success message
                    messages.success(request, f'{city_name} added successfully!')
            else:
                # Display an error message if the city name is not valid
                messages.error(request, f'{city_name} is not a valid city name!')
        else:
            # Display an error message if the form is invalid
            messages.error(request, 'Failed to add city. Please check the input.')
            
        # Redirect the user back to the index page
        return redirect('index')
    
    # Prepare the context dictionary with weather data and the form
    context = {'weather_data': weather_data, 'form': form}
    
    # Render the index.html template with the context data
    return render(request, 'weatherapp/index.html', context)



def validate_city(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return True
        else:
            return False
    except Exception as e:
        return False



# Delete city view
def delete_city(request, city_name):
    city_to_delete = City.objects.get(name=city_name)
    city_to_delete.delete()
    messages.success(request, f'{city_name} removed successfully!')
    return redirect('index')  # Redirect to index view after deleting city
