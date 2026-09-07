from django import template

register = template.Library()

@register.simple_tag
def mutual_friends(user1, user2):
    profile1 = set(user1.profile.friends.values_list('id', flat=True))
    profile2 = set(user2.profile.friends.values_list('id', flat=True))
    return len(profile1.intersection(profile2))



    


