import twitter

api = twitter.Api(
    consumer_key='kKPenxy5WFahqtNNtG66XfthI',
    consumer_secret='rEt8ux88iRxfcPR2Q9uFqjCKxFQZMkTV1lrxRqRKpEVWQRTu3o',
    access_token_key='803348197586374656-C1dKgm5XBApL9vgNxSis0cAuxuJRDJs',
    access_token_secret='BQhQIf7mELBWVZMA2ggAw8F2yhWqRm74MRyytTLlgbN5I'
)

print(api.VerifyCredentials())

# GetFollowerIDs UsersLookup GetUser

user = api.GetUser(screen_name='@LazeaNicoleta')

print(str(user))

user_wrong = api.GetUser(screen_name='@hoebkbkoekoxko')

print(str(user))
