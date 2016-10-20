# Jisoo Kim ID: 72238150 Project 3


###### USER INTERFACE ######
import json
import sys
import http.client
import urllib.request
import urllib.parse


addresses = ['Walnut, CA', 'Seoul, Korea']


def user_interface():
    '''User interface that takes the input needed to return desired information'''
    addresses = []
    outputs = []
    classes = []

    
    num_of_locations = int(input())
    
    for x in range(num_of_locations):
        addy = input().upper()
        addresses.append(addy)

        
    num_of_outputs = int(input())

    for x in range(num_of_outputs):
        output = input().upper()
        outputs.append(output)

    try:
        json1 = open_url(build_url(addresses))
        for x in json1['route']:
            if x == 'routeError':
#                print('\nNO ROUTE FOUND')
                pass
    except:
        print('\nMAPQUEST ERROR')
        return
    


    for x in outputs:
        if x == 'TOTALDISTANCE':
            classes.append(TotalDistance(json1))
        elif x == 'TOTALTIME':
            classes.append(TotalTime(json1))
        elif x == 'LATLONG':
            classes.append(LatLong(json1))
        elif x == 'ELEVATION':
            classes.append(Elevation(json1))
        elif x == 'STEPS':
            classes.append(Steps(json1))

           
    
    _print_output_info(classes)


    
def _print_output_info (classes: []) -> None:
    '''Prints out the information of the indicated outputs'''
    
    for x in classes:
        x.information()


    
###### OPEN DATA APIs ######

def build_url (locations = []) -> str:
    '''Builds the URL that has all the JSON information'''
    API_KEY = 'Fmjtd%7Cluu8216y2l%2C7g%3Do5-942slr'
    BASE_URL = "http://open.mapquestapi.com/directions/v2/route?"
    query_parameters = []
    query_parameters.append(('from', locations[0]))
    for x in locations[1:]:
        query_parameters.append(('to', x))

    new_url = BASE_URL + 'key=' + API_KEY + '&' + urllib.parse.urlencode(query_parameters)

    return new_url
    


def build_elevation_url (latlong: 'latlong') -> str:
    '''Builds the URL needed to obtain the elevations of the locations'''
    API_KEY = 'Fmjtd%7Cluu8216y2l%2C7g%3Do5-942slr'
    BASE = 'http://open.mapquestapi.com/elevation/v1/profile?'
    
    query_parameters = []
    query_parameters.append(('latLngCollection', latlong))
    query_parameters.append(('unit', 'f'))

    
    elevation_url = BASE + 'key=' + API_KEY + '&' + urllib.parse.urlencode(query_parameters)
    return elevation_url


def open_url(URL: str) -> 'json object':
    '''Opens the URL and turns the bytes object into a parsed JSON object'''
    response = None
    
    try:
        response = urllib.request.urlopen(URL)
        json_text = response.read().decode(encoding = 'utf-8')

        return json.loads(json_text)

    finally:
        if response != None:
            response.close()



###### CLASSES ######

class TotalDistance:
    def __init__ (self, json1):
        self._distance = str(round(json1['route']['distance']))

    def information (self):
        print('\nTOTAL DISTANCE: ' + self._distance  + ' miles')


class TotalTime:
    def __init__ (self, json1):
        self._time = str(round(json1['route']['time']/60))

    def information (self):
        print('\nTOTAL TIME: ' + self._time + ' minutes')


class LatLong:
    def __init__ (self, json1):
        self._latlongs = []
        self._unrounded = []
        
        for x in json1['route']['locations']:
            
            self._unrounded.append(str(x['displayLatLng']['lat']))
            latitude = round(x['displayLatLng']['lat'], 2)
            if latitude > 0:
                latitude1 = str(abs(latitude)) + 'N'
            if latitude < 0:
                latitude1 = str(abs(latitude)) + 'S'

            self._unrounded.append(str(x['displayLatLng']['lng']))
            longitude = round(x['displayLatLng']['lng'],2)
            if longitude > 0:
                longitude1 = str(abs(longitude)) + 'E'
            if longitude < 0:
                longitude1 = str(abs(longitude)) + 'W'

            self._latlongs.append(latitude1 + ' ' + longitude1)

    def return_unrounded (self):
        return self._unrounded

    def information(self):
        print('\nLATLONGS')
        
        for x in self._latlongs:
            print(x)


class Elevation:
    def __init__(self, json1):
        x = LatLong(json1)
        self._elevations = []
        self._latlongstring = ','.join(x.return_unrounded())
    
        
        _e_url = (build_elevation_url(self._latlongstring))
        _e_json = open_url(_e_url)
        
        for x in _e_json['elevationProfile']:

            self._elevations.append(round(x['height']))

    def information(self):
        print('\nELEVATIONS')
        for x in self._elevations:
            print(x)

class Steps:
    def __init__ (self, json1):
        self._directions = []
        
        
        for x in json1['route']['legs']:
            for i in x['maneuvers']:
                self._directions.append(i['narrative'])

    def information(self):
        print('\nDIRECTIONS')

        for x in self._directions:
            print(x)                                        
        
            
#json1 = open_url(build_url(addresses))


    
if __name__ == '__main__':
        user_interface()

    

    
