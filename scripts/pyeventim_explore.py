from pyventim import EventimClient


from pyventim import EventimClient
from pyventim.enums.markets import EventimMarket

client = EventimClient(
    market=EventimMarket.GERMANY
)

print(client)
print(dir(client))
methods = [
    m for m in dir(client)
    if not m.startswith("_")
]

print(methods)