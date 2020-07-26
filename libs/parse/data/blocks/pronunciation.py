from libs.parse.data.blocks.base import BaseBlockData
from libs.parse.data.blocks.detailed.pronunciation.transcriptions import \
    TranscriptionsData
from libs.parse.utils.decorators import parsing


class PronunciationData(BaseBlockData):
    @parsing
    def _parse(self):
        self._sub_data = {
            # 'has_data': ...,  # todo
            # 'has_transcription': ...,  # todo
            'transcriptions': TranscriptionsData(self.base, self, self.page),
        }
