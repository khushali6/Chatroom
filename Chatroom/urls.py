# Project name urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app import views
from social_django import urls as social_django_urls  # Import social_django URLs
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models
from app.models import PublicChatMessageManager, PublicRoomChatMessage
from django.contrib.auth.views import LogoutView

class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class PublicRoomChatMessageAdmin(admin.ModelAdmin):
    list_filter=['room','user','timestamp']
    list_display=['room','user','timestamp','content']
    search_fields=['room__title','user__username','content']

    show_full_result_count=False
    paginator=CachingPaginator

# Do not register PublicRoomChatMessage again if it's already registered
if not admin.site.is_registered(PublicRoomChatMessage):
    admin.site.register(PublicRoomChatMessage, PublicRoomChatMessageAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', views.home, name='default_home'),
    path('app/', include('app.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
