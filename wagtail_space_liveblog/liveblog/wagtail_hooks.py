from wagtail.core import hooks

from .utils import get_person_or_create


@hooks.register("process_livepost_before_add")
def set_posted_by(live_post, message):
    slack_id = message["user"]
    live_post["posted_by"] = get_person_or_create(slack_id)
