import json
import sys

import requests


def cli_read() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Not enough arguments')
        quit()


def request_for_user_events(username) -> list:
    url = f'https://api.github.com/users/{username}/events'
    response = requests.get(url)
    events = json.loads(response.text)

    return events

def to_json(filename,data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def main() -> None:
    username: str = cli_read()
    events: list = request_for_user_events(username)
    to_json('events.json', events)
    print(events)

if __name__ == '__main__':
    main()
