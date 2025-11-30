import os
from os.path import join

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View

from core.conf import conf
from projects.authors.authors_storage import authors_storage
from core.storage.main import storage
from libs.parse.storage_page import StoragePage
from libs.utils.io import read
from main.cron_control.cron_list import get_cron_list
from main.cron_control.jobs_control import job_reset
from main.cron_control.new.jobs_control import new_job_reset


class IndexView(TemplateView):
    template_name = 'index.html'


class CronListView(TemplateView):
    template_name = 'cron-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'crons': get_cron_list(),
            'admin': 'admin' in self.request.GET,
        })
        return context


class CronResetView(TemplateView):
    def get(self, request, *args, **kwargs):
        if kwargs['prj'] == 'ws0':
            if not new_job_reset(kwargs['slug']):
                ...  # todo: return render(request, 'jobs_error.html', {'error': u"Файл не найден"})
        elif kwargs['prj'] == 'ws1' and 'admin' in self.request.GET:
            if not job_reset(kwargs['slug']):
                ...  # todo: return render(request, 'jobs_error.html', {'error': u"Файл не найден"})
        return redirect('cron-list')


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
            'errors': join(conf.logs_path, 'exceptions'),
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
