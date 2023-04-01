from posts.models import Post

events = {
    "Push":'PushEvent',
    "Create": 'CreateEvent',
    "Delete": 'DeleteEvent',
    "Watch": 'WatchEvent',
    "Fork": "ForkEvent",
    'Pull': 'PullRequestEvent'

}
class GithubEvent:

    def __init__(self, id, type, username, url):
        self.id = id
        self.username = username
        self.type = type
        self.url = url
        self.content = ""
        self.title = ""
        self.events = events


    def __str__(self):
        return f"{self.username} of {self.type} and id {str(self.id)}"

    def create_event_content(self, github_event):
        
        try:
            repo_name = github_event["repo"]["name"]
            repo_url = "https://github.com/" + repo_name
            repo_md = f"[{repo_name}]({repo_url})"
            user_url = self.url if "https://" in self.url else "https://" + self.url
            user_md = f"[{self.username}]({user_url})"
            if self.type == self.events["Push"]:
                commits = github_event["payload"]["commits"]
                content = f"{user_md} made {len(commits)} commit(s) to repo {repo_md}: \n"
                for commit in commits:
                    sha = commit["sha"]
                    message = commit["message"]
                    sha_url = commit["url"].replace("repos/", "").replace("api", "www")
                    content += f"[{sha}]({sha_url}): {message}  \r\n"
            if self.type == self.events["Pull"]:
                content = f"{user_md} made a pull request to repo {repo_md}"
            elif self.type == self.events["Create"] \
                or self.type == self.events["Delete"]:
                ref = github_event["payload"]["ref"]
                ref_type = github_event["payload"]["ref_type"]
                if ref:
                    action = self.type[0:6].lower() + "d"
                    content = f"{user_md} {action} the {ref} {ref_type} in repo {repo_md}"
                elif ref_type == "repository":
                    content = f"{user_md} {self.type} the repository {repo_md}"
            elif github_event["type"] == self.events["Watch"]:
                content = f"{user_md} starred repo {repo_md}"
            elif github_event["type"] == self.events["Fork"]:
                content = f"{user_md} forked repo {repo_md}"

            if 'content' in locals():
                self.content = content
                self.save()

            self.url = repo_url
        except:
            pass

    
    def create_github_post(self, author):
        data = {
            "title": "GitHub activity of type " + self.type,
            "source": self.url,
            "origin": self.url,
            "author": author,
            "contentType": "text/markdown",
            "content": self.content,
            "visibility": "PUBLIC",
            "is_github": True
        }
        
        post = Post(**data)

        return post


