from typing import Dict
import requests, json
from config_data import config
from loader import logger

APIHOST = "hotels4.p.rapidapi.com"
APIURL = f"https://{APIHOST}/"+"{0}"

def make_query(data: Dict) -> (bool, Dict):
  try:
    url = APIURL.format('locations/v3/search')
  
    headers = {
  	  "X-RapidAPI-Key": config.RAPID_API_KEY,
	    "X-RapidAPI-Host": APIHOST
    }

    querystring = {"q": data['location']}

    response = requests.request("GET", url, headers=headers, params=querystring, timeout=15)
    if response.status_code != 200:
      raise ValueError('Bad response')

    regionId = json.loads(response.text)['sr'][0]['gaiaId']
  
    url = APIURL.format('properties/v2/list')
    headers["content-type"] = "application/json"

    payload = {
	    "destination": {"regionId": regionId},
	    "checkInDate": {
		    "day": 25,
		    "month": 12,
		    "year": 2022
	    },
	    "checkOutDate": {
		    "day": 29,
		    "month": 12,
		    "year": 2022
	    },
	    "rooms": [
		    {
			    "adults": 1,
          "children": []
		    }
	    ],
	    "resultsStartingIndex": 0,
	    "resultsSize": data['hotels_count'],
	    "sort": data['sort_order']
    }

    answer = dict()

    response = requests.request("POST", url, json=payload, headers=headers, timeout=15)
    if response.status_code != 200:
      raise ValueError('Bad response')

    hotels = json.loads(response.text)['data']['propertySearch']['properties']
    for hotel in hotels:
      answer[hotel['id']] = dict()
      answer[hotel['id']]['name'] = hotel['name']
      answer[hotel['id']]['price'] = round(hotel['price']['lead']['amount'], 2)
      answer[hotel['id']]['distance'] = round(hotel['destinationInfo']['distanceFromDestination']['value'] * 1.60934, 2)
      
      url = APIURL.format('properties/v2/detail')
      payload = {"propertyId": hotel['id']}

      response = requests.request("POST", url, json=payload, headers=headers, timeout=15)
      if response.status_code != 200:
        raise ValueError('Bad response')

      hotel_detail = json.loads(response.text)['data']['propertyInfo']

      answer[hotel['id']]['address'] = hotel_detail['summary']['location']['address']['addressLine']
      answer[hotel['id']]['url'] = hotel_detail['summary']['location']['staticImage']['url']
      answer[hotel['id']]['tag'] = hotel_detail['summary']['tagline'].strip()
      if data['show_photo']:
        images_list = hotel_detail['propertyGallery']['images']
        answer[hotel['id']]['images'] = list()
        for i_photo in range(min(len(images_list), data['photo_count'])):
          answer[hotel['id']]['images'].append(images_list[i_photo])

  except Exception as e:
    logger.exception(e)
    return False, str(e)

  return True, answer
