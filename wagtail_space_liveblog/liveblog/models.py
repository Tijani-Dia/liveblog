from django.core.paginator import Paginator
from django.db import models
from django.http import JsonResponse
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from wagtail_live.models import LivePageMixin


@register_snippet
class Person(models.Model):
    slack_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class LiveBlogPage(Page, LivePageMixin):
    content_panels = Page.content_panels + LivePageMixin.panels
    paginate_by = 10

    def serve(self, request, *args, **kwargs):
        if page := request.GET.get("page"):
            return self.serve_live_posts(page)
        return super().serve(request, *args, **kwargs)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        paginator = Paginator(self.live_posts, per_page=self.paginate_by)
        context["live_posts"] = paginator.get_page(1)
        context["total_pages"] = paginator.num_pages
        return context

    def serve_live_posts(self, page):
        paginator = Paginator(self.live_posts, per_page=self.paginate_by)
        live_posts = {
            post.id: {
                "show": post.value["show"],
                "content": post.render(context={"block_id": post.id}),
            }
            for post in paginator.get_page(page)
        }
        return JsonResponse(
            {
                "livePosts": live_posts,
                "totalPages": paginator.num_pages,
            }
        )
