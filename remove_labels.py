# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
import requests

GITHUB_HEADERS = {
    "DELETE": {
        "Accept": "application/vnd.github.+json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
}


# main driver function
if __name__ == "__main__":
    pr_number = os.getenv("GITHUB_REF").split("/")[-2]
    print("pr number: ", pr_number)
    print(os.getenv('GITHUB_TOKEN'))
    print(GITHUB_HEADERS)
    requests.delete(
        f"https://api.github.com/repos/guipdsc/github_workshop/issues/{pr_number}/labels",
        headers=GITHUB_HEADERS["DELETE"],
    )
    print("Deleted label")
