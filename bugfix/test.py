from api import (
    apiGetLinkedChallenges,
    apiGetCreationCHLC,
)
parent = apiGetCreationCHLC(6142)
print(parent)
challenges = apiGetLinkedChallenges(parent)
print(challenges)