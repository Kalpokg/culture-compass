from pyventim import (
    EventimCategory,
    EventimClient,
    EventimMarket,
)

print("=" * 80)
print("EVENTIM CATEGORIES")
print("=" * 80)

for category in EventimCategory:
    print(
        f"{category.name:<30} -> {category.value}"
    )

print()


def main():

    client = EventimClient(
        EventimMarket.GERMANY,
    )

    product_groups = client.product_groups(
        categories=[
            EventimCategory.CONCERTS,
        ],
        page_limit=1,
    )

    product_groups = list(product_groups)

    print(f"Retrieved {len(product_groups)} product groups.\n")

    if not product_groups:
       print("No product groups found.")
       return

    product_group = product_groups[0]

    print(type(product_group))
    print()

    print(product_group)
    print()

    print(product_group.model_dump())
        

    try:
        print(product_group.model_dump())
    except AttributeError:
        print(product_group)

    print("\n" + "=" * 80)
    print("ATTRIBUTES")
    print("=" * 80)

    for attribute in sorted(dir(product_group)):
        if not attribute.startswith("_"):
            print(attribute)


if __name__ == "__main__":
    main()