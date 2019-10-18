import twitter

api = twitter.Api(
    consumer_key='hide',
    consumer_secret='hide',
    access_token_key='hide',
    access_token_secret='hide'
)

print(api.VerifyCredentials())

# GetFollowerIDs UsersLookup GetUser

user = api.GetUser(screen_name='@LazeaNicoleta')

print(str(user))

user_wrong = api.GetUser(screen_name='@hoebkbkoekoxko')

print(str(user))
