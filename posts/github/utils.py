import requests
import re

from posts.github.github import GithubEvent


events = {
    "Push":'PushEvent',
    "Create": 'CreateEvent',
    "Delete": 'DeleteEvent',
    "Watch": 'WatchEvent',
    "Fork": "ForkEvent",
    'Pull': 'PullRequestEvent'
}

def github_events_to_posts(github_events, github_url, author):
    objects = []
    for event in github_events:
        if event["type"] not in events.values():
            continue

        github_event = GithubEvent(
            id = event["id"],
            type = event["type"],
            username = event["actor"]["login"],
            url = github_url,
        )
        github_event.create_event_content(event)
  
        github_event_post = github_event.create_github_post(author)
        if github_event_post:
            objects.append(github_event_post)

    return objects

def get_github_activities(github_url, author):
    if github_url is None:
        return []
    match = re.search(r'(https?:\/\/)?(www\.)?github\.com\/(?P<username>[\w-]+)\/?', github_url)
    username = match.group("username") if match else ""
    if len(username) == 0:
        return []

    # https://docs.github.com/en/rest/reference/activity#list-public-events-for-a-user
    response = requests.get(
        url = f"https://api.github.com/users/{username}/events",
        params = {"per_page": 20}
    )

    if response.status_code != 200:
        print(f"Cannot get github activity for user {username}")
        print(f"Request returned a status code: {response.status_code}")
        print(f"Request body: {response.text}")
        return []

    return github_events_to_posts(response.json(), github_url, author)

    