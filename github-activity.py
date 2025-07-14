import json
import sys

import requests


def cli_read() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        print('Not enough arguments')
        quit()


def user_events(username) -> list:
    url = f'https://api.github.com/users/{username.replace('/','%2F')}/events'
    response = requests.get(url)
    events = json.loads(response.text)

    return [events] if type(events) != list else events

def check_if_valid(events):
    if not events:
        print('There\'s no recent activity')
        return False
    if 'status' in events[0] and events[0]['status'] == '404':
        print('No user with such username was found')
        return False
    return True


def to_json(filename,data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def main() -> None:
    username: str = cli_read()
    events: list = user_events(username)
    to_json('events.json', events)
    if not check_if_valid(events):
        return
    print(events)

if __name__ == '__main__':
    main()
