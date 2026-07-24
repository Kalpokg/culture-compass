from scripts.load_eventim import load_eventim
from scripts.load_ticketmaster import load_ticketmaster


def main():
    print("\n========== Loading Ticketmaster ==========\n")
    load_ticketmaster()

    print("\n========== Loading Eventim ==========\n")
    load_eventim()

    print("\n========== Finished Loading All Sources ==========\n")


if __name__ == "__main__":
    main()