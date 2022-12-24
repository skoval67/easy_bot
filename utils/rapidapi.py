from typing import Dict
from json import loads
from requests import get, post, Response, exceptions
from config_data import config
from loader import logger
from datetime import date
from backoff import on_exception, expo, fibo
from loader import logger


APIHOST = "hotels4.p.rapidapi.com"
APIURL = f"https://{APIHOST}/"+"{0}"

def fatal_code(e: Exception) -> bool:
  return e.response.status_code >= 500

@on_exception(expo, exceptions.RequestException, max_time=60, max_tries=8, jitter=0.1, giveup=fatal_code, logger=logger)
def get_url(url: str, **kwargs) -> Response:
  return get(url, **kwargs)

@on_exception(fibo, exceptions.RequestException, max_time=60, max_tries=8, jitter=None, giveup=fatal_code, logger=logger)
def get_post(url: str, **kwargs) -> Response:
  return post(url, **kwargs)


def make_query(data: Dict) -> (bool, Dict):
  try:
    url = APIURL.format('locations/v3/search')
  
    headers = {
  	  "X-RapidAPI-Key": config.RAPID_API_KEY,
	    "X-RapidAPI-Host": APIHOST
    }

    querystring = {"q": data['location']}

    response = get_url(url, headers=headers, params=querystring)
    if response.status_code != 200:
      raise ValueError('Bad response')

    regionId = loads(response.text)['sr'][0]['gaiaId']
  
    url = APIURL.format('properties/v2/list')
    headers["content-type"] = "application/json"

    payload = {
	    "destination": {"regionId": regionId},
	    "checkInDate": data['checkin'],
	    "checkOutDate": data['checkout'],
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

    response = get_post(url, json=payload, headers=headers)
    if response.status_code != 200:
      raise ValueError('Bad response')

    hotels = loads(response.text)['data']['propertySearch']['properties']
    for hotel in hotels:
      answer[hotel['id']] = dict()
      answer[hotel['id']]['name'] = hotel['name']
      answer[hotel['id']]['price'] = round(hotel['price']['lead']['amount'], 2)
      answer[hotel['id']]['distance'] = round(hotel['destinationInfo']['distanceFromDestination']['value'] * 1.60934, 2)    # переводим расстояние в километры (возвращается в милях)
      answer[hotel['id']]['checkin'] = data['checkin']
      answer[hotel['id']]['checkout'] = data['checkout']

      url = APIURL.format('properties/v2/detail')
      payload = {"propertyId": hotel['id']}

      response = get_post(url, json=payload, headers=headers)
      if response.status_code != 200:
        raise ValueError('Bad response')

      hotel_detail = loads(response.text)['data']['propertyInfo']

      answer[hotel['id']]['address'] = hotel_detail['summary']['location']['address']['addressLine']
      answer[hotel['id']]['url'] = hotel_detail['summary']['location']['staticImage']['url']            # другой страницы отеля в api не нашел
      answer[hotel['id']]['tag'] = hotel_detail['summary']['tagline'].strip()
      if data['show_photo']:
        images_list = hotel_detail['propertyGallery']['images']
        answer[hotel['id']]['images'] = list()
        for i_photo in range(data['photo_count']):
          answer[hotel['id']]['images'].append(images_list[i_photo])

  except Exception as e:
    logger.exception(e)
    return False, str(e)

  return True, answer
