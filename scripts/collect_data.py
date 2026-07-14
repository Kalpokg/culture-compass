from culture_compass.ingestion.collector import EventCollector

collector = EventCollector()

filepath = collector.collect(
    keyword="jazz",
    city="Berlin",
)

print(f"\nSaved file:\n{filepath}")