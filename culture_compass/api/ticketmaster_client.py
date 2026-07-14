from typing import Optional

import requests

from culture_compass.config.settings import TICKETMASTER_API_KEY


class TicketmasterClient:
    """
    Client for interacting with the Ticketmaster Discovery API.
    """

    BASE_URL = "https://app.ticketmaster.com/discovery/v2"

    def __init__(self):
        self.api_key = TICKETMASTER_API_KEY

    def search_events(
    self,
    keyword=None,
    city=None,
    page=0,
    size=200,
    ):
        """
        Search Ticketmaster events.
        """

        url = f"{self.BASE_URL}/events.json"

        params = {
         "apikey": self.api_key,
         "keyword": keyword,
         "city": city,
         "page": page,
         "size": size,
         }

        response = requests.get(url, params=params)

        return response.json()