from libs.parse.data.blocks.detailed.base import BaseDetailedData
from libs.parse.utils.decorators import parsing


class TranscriptionsData(BaseDetailedData):
    @parsing
    def _parse(self):
        rules = {
            'ru': ['transcription-ru', 'transcriptions-ru'],
            'hy': ['transcription-hy', 'transcriptions-hy'],
            'uk': ['transcription-uk', 'transcriptions-uk'],
            'eo': ['transcription eo', 'transcriptions eo', 'transcription/eo'],
            'la': ['transcription-la'],
            'grc': ['transcription-grc'],
            # 'nl': ['transcription', 'transcriptions', 'transcription3'],
            # 'de': ['transcription', 'transcriptions', 'transcription3'],
        }

        templates = []
        for key, tpl in self.base.templates(re='transcription.*'):
            t = {
                'name': tpl.name,
                'values': tpl.params,
                'has_data': tpl.has_data,
                'wrong': [],
            }

            for lang, rule in rules.items():
                if lang == self.lang:
                    if tpl.name not in rule:
                        t['wrong'].append(f'need_{lang}')
                        if tpl.name not in ['transcription', 'transcriptions']:
                            t['wrong'].append('wrong_tpl')
                    break
            else:
                if tpl.name not in ['transcription', 'transcriptions']:
                    t['wrong'].append('wrong_tpl')

            is_noun = None
            if self.base_data.morphology:
                is_noun = self.base_data.morphology.is_noun()

            if is_noun and not tpl.name.startswith('transcriptions'):
                t['wrong'].append('need_plural')
            elif not is_noun and tpl.name.startswith('transcriptions'):
                t['wrong'].append('need_singular')

            # if 'need_ru' in t['wrong'] \
            #         or 'wrong_tpl' in t['wrong']:
            #     print(f'{tpl.name} - [{self.lang}] - {self.title}')

            templates.append(t)

        self._sub_data = {
            'has_data': any([t['has_data'] for t in templates]),
            'templates': templates,
        }
