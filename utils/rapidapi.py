from typing import Dict, List
from json import loads
from requests import get, post, Response, exceptions
from config_data import config
from loader import logger
from datetime import date
from backoff import on_exception, expo, fibo
from loader import logger


APIHOST = "hotels4.p.rapidapi.com"
APIURL = f"https://{APIHOST}/"+"{0}"

@on_exception(expo, exceptions.RequestException, max_time=60, max_tries=8, logger=logger)
def get_url(url: str, **kwargs) -> Response:
  return get(url, **kwargs)

@on_exception(fibo, exceptions.RequestException, max_time=60, max_tries=15, logger=logger)
def get_post(url: str, **kwargs) -> Response:
  return post(url, **kwargs)


def get_regions_id(location: str) -> List:
  try:
    url = APIURL.format('locations/v3/search')
    headers = {
  	  "X-RapidAPI-Key": config.RAPID_API_KEY,
	    "X-RapidAPI-Host": APIHOST
    }
    querystring = {"q": location}

    response = get_url(url, headers=headers, params=querystring)
    if response.status_code != 200:
      raise ValueError('Bad response')

  except Exception as e:
    logger.exception(e)
    return False, str(e)

  return True, [(loc['gaiaId'], loc['regionNames']['displayName']) for loc in loads(response.text)['sr'] if loc['type'] == 'CITY']


def make_query(data: Dict) -> (bool, Dict):
  try:
    url = APIURL.format('properties/v2/list')
    headers = {
  	  "X-RapidAPI-Key": config.RAPID_API_KEY,
	    "X-RapidAPI-Host": APIHOST,
      "content-type": "application/json"
    }

    payload = {
      "currency": "USD",
	    "destination": {"regionId": data['region_id']},
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

    if data['command'] == '/highprice':
      payload['filters'] = {'price': {'max': data['max_price'], 'min': data['min_price']}}
      payload['resultsSize'] = 200
      while True:
        response = get_post(url, json=payload, headers=headers)
        if response.status_code != 200:
          raise ValueError('Bad response')
        count = len(loads(response.text)['data']['propertySearch']['properties'])
        payload['resultsStartingIndex'] += count
        if count < 200:
          break
      payload['resultsStartingIndex'] -= data['hotels_count']        # starting_index указывает на последний элемент в списке отелей, надо отнять количество отелей для поиска
      payload['resultsSize'] = data['hotels_count']
    elif data['command'] == '/bestdeal':
      payload['filters'] = {'price': {'max': data['max_price'], 'min': data['min_price']}}
 
    answer = dict()

    response = get_post(url, json=payload, headers=headers)
    if response.status_code != 200:
      raise ValueError('Bad response')

    if 'errors' in loads(response.text):
      raise KeyError(f"{loads(response.text)['errors'][0]['extensions']['code']}")

    if data['command'] == '/bestdeal':
      hotels = [hotel for hotel in loads(response.text)['data']['propertySearch']['properties'] if data['min_distance'] <= float(hotel['destinationInfo']['distanceFromDestination']['value']) <= data['max_distance']]
    else:
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
      answer[hotel['id']]['tag'] = hotel_detail['summary']['tagline'].strip()
      if data['show_photo']:
        images_list = hotel_detail['propertyGallery']['images']
        answer[hotel['id']]['images'] = list()
        for i_photo in range(min(data['photo_count'], len(images_list))):
          answer[hotel['id']]['images'].append(images_list[i_photo])

  except Exception as e:
    logger.exception(e)
    return False, str(e)

  return True, answer
