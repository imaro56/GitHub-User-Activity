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
    url = f'https://api.github.com/users/{username.replace('/', '%2F')}/events'
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
    if 'message' in events[0] and 'API rate' in events[0]['message']:
        print('Too many requests, please wait for a while')
        return False
    return True


def print_recent_events(event) -> None:
    repo_name = event['repo']['name']
    if event['type'] == 'PushEvent':
        commits_cnt = int(event['payload']['size'])
        print(f'- Pushed {commits_cnt} commit{'s' if commits_cnt > 1 else ''} to {repo_name}')
    elif event['type'] == 'IssuesEvent':
        action = event['payload']['action'][0].upper() + event['payload']['action'][1:]
        issue_title = event['payload']['issue']['title']
        print(f'- {action} an issue {issue_title} in {repo_name}')
    elif event['type'] == 'CreateEvent':
        ref = event['payload']['ref']
        print(f'- Created {ref + ' branch in ' if ref else ''}{repo_name}')
    elif event['type'] == 'IssueCommentEvent':
        print(f'- Commented on issue {event['payload']['issue']['title']}')
    elif event['type'] == 'IssuesEvent':
        print(f'- Created issue {event['payload']['issue']['title']}')
    elif event['type'] == 'WatchEvent':
        print(f'- Starred {repo_name}')
    elif event['type'] == 'PullRequestEvent':
        print(f'- Created pull request {event['payload']['pull_request']['number']}')
    elif event['type'] == 'PullRequestReviewEvent':
        print(f'- Reviewed pull request {event['payload']['pull_request']['number']}')
    elif event['type'] == 'PullRequestReviewCommentEvent':
        print(f'- Commented on pull request {event['payload']['pull_request']['number']}')
    elif event['type'] == 'CreateEvent':
        print(f'- Created {event['payload']['ref_type']} {event['payload']['ref']}')
    else:
        print(f'- {event['type']}')


def to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def main() -> None:
    username: str = cli_read()
    events: list = user_events(username)
    to_json('events.json', events)
    if not check_if_valid(events):
        return
    for event in events:
        print_recent_events(event)


if __name__ == '__main__':
    main()
