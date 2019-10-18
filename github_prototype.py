# access token 6bc50263fea3c977f105e03617a6c5bb21d5434f
from github3 import login

gh = login(token='6bc50263fea3c977f105e03617a6c5bb21d5434f')
print(str(gh.me()))

user1 = gh.user('andreiio')
print(str(user1))
# 18010308
for org in gh.organizations_with('surdu'):
    print(str(org))

for org in gh.organizations_with('adi-ads'):
    print(str(org))
