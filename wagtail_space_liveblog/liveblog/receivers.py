import re

from wagtail_live.receivers.slack import SlackEventsAPIReceiver

from .utils import get_person_or_create


class SlackReceiver(SlackEventsAPIReceiver):
    def parse_text(self, text):
        mention_format = re.compile(r"<(.*?)>")
        mentions = mention_format.finditer(text)
        for mention in mentions:
            mentionned = mention.group()[1:-1]
            if mentionned.startswith("#C"):
                channel_name = mentionned.split("|")[-1]
                text = text.replace(mention.group(), f"#{channel_name}")
            elif mentionned.startswith("@U") or mentionned.startswith("@W"):
                user_id = mention.group()[2:-1]
                person = get_person_or_create(user_id)
                text = text.replace(mention.group(), f"@{person}")

        return super().parse_text(text)
