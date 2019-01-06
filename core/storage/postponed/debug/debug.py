from libs.utils.debug import debug
from libs.utils.dt import dt


class DebugMixin:
    @debug
    def _debug_title(self, i, title):
        print(dt(), i, title, ' --  ', end='')

    @debug
    def _debug_info(self, info):
        print(info, ' --  ', end='')

    @debug
    def _debug_skipped(self):
        print('skipped.')

    @debug
    def _debug_processed(self):
        print('processed.')

    @debug
    def _debug_titles_saved(self):
        print(dt(), '## Titles saved!')
