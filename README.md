# Server for Getting Developer Social Connections

This server will query both Twitter and GitHub to see if two developers are connected

## Getting Started

Clone this repository


### Running

Create a secrets.py file following this struture:
```
TWITTER_CONSUMER_KEY = '{your key}'
TWITTER_CONSUMER_SECRET = '{your secret}'
TWITTER_ACCESS_TOKEN_KEY = '{your access token key}'
TWITTER_ACCESS_TOKEN_SECRET = '{your access token secret}'
GITHUB_TOKEN = '{your github token}'
```
Run the following two commands:

```
docker build -t connectionserver .
docker run -v /{path to your secrets file}/secrets.py:/app/secrets.py -p 5000:5000 connectionserver
```

### Usage

Available calls: <br>
```
GET http://127.0.0.1:5000/connected/realtime/{dev1}/{dev2}
GET http://127.0.0.1:5000/connected/register/{dev1}/{dev2}
```

### Future developments
The docker image could be using an NGinx web server which could act as a proxy for the Flask web app.
