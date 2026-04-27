from django.urls import include, path

from . import views

urlpatterns = [
    path("create", include("users.create.urls")),
    path("search", include("users.search.urls")),
    path("count", include("users.count.urls")),
    path("update_page", include("users.update_page.urls")),
    path("messages", include("users.messages.urls")),
    path("add_friend", include("users.add_friend.urls")),
    path("remove_friend", include("users.remove_friend.urls")),
    path("set_active_status", include("users.set_active_status.urls")),
    path("applications", include("users.applications.urls")),
    path("message_notifications", include("users.message_notifications.urls")),
    path("notifications", include("users.notifications.urls")),
    path("settings", include("users.settings.urls")),
    path("delete_user", include("users.delete_user.urls")),
    path("increment_view", include("users.increment_view.urls")),
    path("subscribe_session", include("users.subscribe.urls")),
    path("subscriptions", include("users.subscriptions.urls")),
    path("unsubscribe", include("users.unsubscribe.urls")),
    path("resubscribe", include("users.resubscribe.urls")),
    path("claim_membership", include("users.claim_membership.urls")),
    path("new_chat_limit", include("users.new_chat_limit.urls"))
]