from pprint import pprint

from culture_compass.api.ticketmaster_client import TicketmasterClient
from culture_compass.data_processing.parser import parse_events
from culture_compass.data_processing.cleaning import clean_events
from culture_compass.features.text_features import create_event_text

client = TicketmasterClient()

response = client.search_events(
    keyword="jazz",
    city="Berlin",
)

df = parse_events(response)
df = clean_events(df)
df = create_event_text(df)

print(df.info())
print()

print(df[[
    "event_name",
    "genre",
    "segment",
    "city",
    "event_text"
]].head())

from culture_compass.recommender.content_based import (
    ContentBasedRecommender,
)

recommender = ContentBasedRecommender()

recommender.fit(df)

print("\nRecommendations:\n")

print(
    recommender.recommend(
        event_id=df.iloc[0]["event_id"],
        top_n=5,
    )
)