# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import requests
import jwt
import time
import pathlib

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

PEM_FILE = "guipdscappworkshop.2023-10-13.private-key.pem"

# Open PEM
with open(pathlib.Path(__file__).parent.absolute() / PEM_FILE, "rb") as pem_file:
    signing_key = jwt.jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    "iat": int(time.time()),
    # JWT expiration time (10 minutes maximum)
    "exp": int(time.time()) + 600,
    # GitHub App's identifier
    "iss": 407747,
}

# Get JWT
jwt_instance = jwt.JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")
print("JWT:", encoded_jwt)

# Get installation id
installation_id = requests.get(
    "https://api.github.com/app/installations",
    headers={
        "Accept": "application/vnd.github.+json",
        "Authorization": f"Bearer {encoded_jwt}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
print("Installation ID:", installation_id.json()[0]['id'])

# Get installation token
installation_token = requests.post(
    f"https://api.github.com/app/installations/{installation_id.json()[0]['id']}/access_tokens",
    headers={
        "Accept": "application/vnd.github.+json",
        "Authorization": f"Bearer {encoded_jwt}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
print("Installation Token:", installation_token.json()['token'])

GITHUB_HEADERS = {
    "DELETE": {
        "Accept": "application/vnd.github.v3+json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {installation_token.json()['token']}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
}


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/", methods=["POST"])
def webhook():
    if request.method == "POST":
        if request.json["action"] == "labeled":
            requests.delete(
                f"https://api.github.com/repos/guipdsc/github_workshop/issues/{request.json['number']}/labels/{request.json['label']['name']}",
                headers=GITHUB_HEADERS["DELETE"],
            )
            print("Deleted label")
        print("Received Request, Nothing else to do!")
        return "Webhook received!"


# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host="localhost", port=3000, debug=True)
