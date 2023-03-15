import requests
import polyline

api_key = "AsY_3uLWFITVnxJzQMAExgrZQ4zTdMEOha9jDKCKYNEsQdHyxMO-SeTHdvzTgCax"

##################################################################################

def itineraire(traj):
    '''
        traj: Coordinates Array (Longitude THEN Latitude)
        
        Builds a request (String) for the Bing Maps API, sends it, then returns the encoded polyline of the route
    '''
    #API request building
    url = f"https://dev.virtualearth.net/REST/v1/Routes/Driving?wp.0={traj[0]}"
    for i, point in enumerate(traj[1:-1]):
        url += f"&wp.{i+1}={point}"
    url += f"&wp.{len(traj)-1}={traj[-1]}"
    url += f"&routePathOutput=Points&key={api_key}"

    print(url)
    
    #Sending the request to the API 
    response = requests.get(url).json()
    #Gathering itinerary infos
    polyline_str = response["resourceSets"][0]["resources"][0]["routePath"]["line"]["coordinates"]
    polyline_coord = [(lat, lon) for lon, lat in polyline_str]
    polyline_encoded = polyline.encode(polyline_coord)
    
    distance = response["resourceSets"][0]["resources"][0]["travelDistance"]
    duration = response["resourceSets"][0]["resources"][0]["travelDuration"]
    
    #Displaying itinerary infos
    print(f"Distance : {distance} km")
    print(f"Durée : {duration} secondes")
    print(polyline_coord)
    
    return(polyline_encoded)

test = ["48.8566,2.3522" , "51.5074,-0.1278" , "46.5468,1.6639"]
itineraire(test)         
