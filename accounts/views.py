# Create your views here.
import json
import logging

from django.views.generic import DetailView, ListView, TemplateView

from accounts.models import Activity

logger = logging.getLogger(__name__)


class ProfileView(TemplateView):
    template_name = "accounts/profile.html"


class ActivityListView(ListView):
    context_object_name = "activities"

    def get_queryset(self):
        user_profile = self.request.user.profile
        return user_profile.activity_set.all().order_by("-date")


class ActivityDetailView(DetailView):
    model = Activity
    context_object_name = "activity"

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        activity = context["activity"]
        try:
            context["diff_list"] = json.loads(activity.serialized_data)
        except Exception:
            logger.exception()
        return context
