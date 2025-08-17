"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main.views import PageView, LogsFileView, LogsFolderView, TextView, \
    IndexView, CronListView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view()),
    path('cron/list/', CronListView.as_view()),
    path('text/<str:text>', TextView.as_view()),

    path('page/<str:title>', PageView.as_view(),
         name='page'),

    path('logs/<str:root>/', LogsFolderView.as_view(),
         name='logs_folder'),

    path('logs/<str:root>/<path:path>/', LogsFolderView.as_view(),
         name='logs_folder'),

    path('logs/<str:root>/<path:path>', LogsFileView.as_view(),
         name='logs_file'),

    # todo: path('storage/<str:root>/<path:path>', StorageView.as_view(), name='storage'),
]
