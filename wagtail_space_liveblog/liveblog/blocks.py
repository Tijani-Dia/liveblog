from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail_live.blocks import LivePostBlock


class WagtailSpaceLivePostBlock(LivePostBlock):
    posted_by = SnippetChooserBlock("liveblog.Person", required=False)
