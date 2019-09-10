import os
from os.path import join

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View

from core.conf import conf
from projects.authors.authors_storage import authors_storage
from core.storage.main import storage
from libs.parse.storage_page import StoragePage
from libs.utils.io import read


class PageView(View):
    def get(self, request, *args, **kwargs):
        page = StoragePage(kwargs['title'], silent=True)
        return HttpResponse(f'<pre>{page.content}</pre>')


class LogsPathMixin:
    def get_path(self, kwargs):
        roots = {
            'storage': storage.logs_path,
            'authors': authors_storage.logs_path,
            # 'htmls': htmls_storage.logs_path,
            # 'reports': conf.MAIN_STORAGE_PATH,
            'errors': join(conf.LOGS_PATH, 'exceptions'),
        }
        root = kwargs['root']
        path = kwargs.get('path')
        full_path = roots[root]
        if path:
            full_path = join(full_path, path)
        return root, path, full_path


class LogsFileView(LogsPathMixin, View):
    def get(self, request, *args, **kwargs):
        root, path, full_path = self.get_path(kwargs)
        content = read(full_path)
        return HttpResponse(f'<pre>{content}</pre>')


class LogsFolderView(LogsPathMixin, TemplateView):
    template_name = 'logs_folder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        root, path, full_path = self.get_path(kwargs)
        files = {}
        folders = {}
        for name in sorted(os.listdir(full_path)):
            full_name = join(full_path, name)
            short_name = join(path, name) if path else name
            if os.path.isdir(full_name):
                folders[name] = short_name
            if os.path.isfile(full_name):
                files[name] = short_name
        context.update({
            'root': root,
            'folders': folders,
            'files': files,
        })
        return context


class TextView(TemplateView):
    template_name = 'text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'text': self.kwargs.get('text')
        })
        return context
