import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .models import Person


def create_person(slack_id):
    slack_bot_token = getattr(settings, "SLACK_BOT_TOKEN", "")
    if not slack_bot_token:
        raise ImproperlyConfigured(
            "You haven't specified SLACK_BOT_TOKEN in your settings. "
            "You won't be able to fetch a user's details from Slack without this setting defined."
        )

    response = requests.get(
        "https://slack.com/api/users.info",
        headers={"Authorization": f"Bearer {slack_bot_token}"},
        params={"user": slack_id},
    )
    response.raise_for_status()

    result = response.json()
    return Person.objects.create(slack_id=slack_id, name=result["user"]["real_name"])


def get_person_or_create(slack_id):
    try:
        return Person.objects.get(slack_id=slack_id)
    except Person.DoesNotExist:
        return create_person(slack_id)
