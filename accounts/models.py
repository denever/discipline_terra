# encoding: utf-8
# importing User for UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# importing for signals and logging
from django.dispatch import receiver
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _

# from django.utils import simplejson -> json

LOGIN, LOGOUT, CREATE, EDIT, DELETE = range(5)

actions = [_("Logged In"), _("Logged Out"), _("Created"), _("Edited"), _("Deleted")]


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Account")


class Activity(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Activity date"), auto_now_add=True)
    action = models.PositiveSmallIntegerField(_("Action"))
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(_("Object name"), max_length=50)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")

    serialized_data = models.TextField(
        help_text="The serialized form of this version of the model."
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __unicode__(self):
        return "%s %s %s %s" % (
            self.date,
            self.userprofile,
            self.action,
            self.object_repr,
        )

    def get_action_description(self):
        return actions[self.action]

    def get_content_type_name(self):
        return self.content_type.model_class()._meta.verbose_name


@receiver(user_logged_in)
def logged_in_cb(sender, **kwargs):
    user_profile = (kwargs["user"].profile,)
    a = Activity(
        userprofile=user_profile,
        action=LOGIN,
        object_repr=smart_str(user_profile),
        content_object=user_profile,
    )
    a.save()


@receiver(user_logged_out)
def logged_out_cb(sender, **kwargs):
    user_profile = (kwargs["user"].profile,)
    a = Activity(
        userprofile=user_profile,
        action=LOGOUT,
        object_repr=smart_str(user_profile),
        content_object=user_profile,
    )
    a.save()
