from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import ActivityDetailView, ActivityListView, ProfileView

urlpatterns = [
    path(
        "activity/<int:pk>", login_required(ActivityDetailView.as_view()), name="detail"
    ),
    path("activity", login_required(ActivityListView.as_view()), name="list"),
    path("profile", login_required(ProfileView.as_view()), name="profile"),
    path("google/login", "django_openid_auth.views.login_begin", name="openid-login"),
    path(
        "google/login-complete",
        "django_openid_auth.views.login_complete",
        name="openid-complete",
    ),
    path(
        "logout", "django.contrib.auth.views.logout", {"next_page": "/"}, name="logout"
    ),
]

# from django.conf.urls import patterns, url
# from django.contrib.auth.decorators import login_required, permission_required

# urlpatterns = patterns('accounts.views',
#                        url(r'^profile/$',
#                            login_required(.as_view()),
#                            name='profile'
#                            ),

#                        url(r'^activity/$',
#                            login_required(ActivityListView.as_view()),
#                            name='activities'),

#                        url(r'^activity/(?P<pk>\d+)$',
#                            login_required(ActivityDetailView.as_view()),
#                            name='activity-detail'),
#                        )

# urlpatterns += patterns('',
#                         url(r'^google/login/$',
#                             'django_openid_auth.views.login_begin',
#                             name='openid-login'),
#                         url(r'^google/login-complete/$',
#                             'django_openid_auth.views.login_complete',
#                             name='openid-complete'),
#                         url(r'^logout/$',
#                             'django.contrib.auth.views.logout',
#                             {'next_page': '/',},
#                             name='logout'
#                             ),
#                     )

# (r'^login/$', 'django.contrib.auth.views.login',
#  {'template_name': 'accounts/login.html'},
#  "login"
#  ),

# (r'^logout/$', 'django.contrib.auth.views.logout',
#  {'template_name': 'accounts/logout.html'},
#  "logout",
#  ),

# (r'^changepasswd/$', 'django.contrib.auth.views.password_change',
#  {'template_name': 'accounts/password_change_form.html'},
#  'change-passwd',
#  ),

# (r'^changedone/$', 'django.contrib.auth.views.password_change_done',
#  {'template_name': 'accounts/password_change_done.html'},
#  'password_change_done',
#  ),
