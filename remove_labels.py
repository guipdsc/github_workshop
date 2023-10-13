# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
import requests

GITHUB_HEADERS = {
    "DELETE": {
        "Accept": "application/vnd.github.v3+json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
}


# main driver function
if __name__ == "__main__":
    print("ref: ", os.getenv("GITHUB_REF"))
    # requests.delete(
    #     f"https://api.github.com/repos/guipdsc/github_workshop/issues/{request.json['number']}/labels/{request.json['label']['name']}",
    #     headers=GITHUB_HEADERS["DELETE"],
    # )
    # print("Deleted label")
