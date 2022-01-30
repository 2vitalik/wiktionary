import up  # don't remove this
from core.reports.reports.ru.verbs.without_transcription import \
    VerbsWithoutTranscription
from core.reports.scripts.run import reports_some


if __name__ == '__main__':
    reports_some([VerbsWithoutTranscription])
