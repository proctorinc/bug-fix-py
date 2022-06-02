from api import (
    get_linked_challenges,
    get_creation_chlc,
)
parent = get_creation_chlc(6142)
print(parent)
challenges = get_linked_challenges(parent)
print(challenges)