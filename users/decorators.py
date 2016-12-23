from django.contrib.auth.decorators import user_passes_test


def team_required(function=None):
    def user_has_team(user):
        return user.team is not None

    actual_decorator = user_passes_test(user_has_team, login_url='join_team')

    if function:
        return actual_decorator(function)
    return actual_decorator
