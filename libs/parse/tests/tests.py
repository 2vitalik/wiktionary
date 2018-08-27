import unittest

from libs.parse.tests.mockup_page import MockupPage


class TestMockupPage(unittest.TestCase):
    def setUp(self):
        self.page = MockupPage()

    def test_languages_keys(self):
        mocked = ['ru', 'en']
        self.assertEqual(self.page.keys, mocked)
        self.assertEqual(self.page.languages.keys, mocked)

    def test_languages_grouper(self):
        for obj in [self.page, self.page.languages]:
            mocked = list(self.page.lang_sections.as_list())
            '''
            [
                LanguageSection(ru),
                LanguageSection(en),
            ]
            '''
            self.assertEqual(mocked, obj.as_list())
            self.assertEqual(mocked, obj.as_list(unique=True))

            mocked = {key: [value]
                      for key, value in self.page.lang_sections.as_dict()}
            '''
            {
                'ru': [ LanguageSection(ru) ],
                'en': [ LanguageSection(en) ],
            }
            '''
            self.assertEqual(mocked, obj.as_dict())
            self.assertEqual(mocked, obj.as_dict('lang'))
            self.assertEqual(mocked, obj.as_dict('*'))
            self.assertEqual(mocked, obj.as_list('lang'))
            self.assertEqual(mocked, obj.as_list('*'))

            mocked = self.page.lang_sections
            '''
            {
                'ru': LanguageSection(ru),
                'en': LanguageSection(en),
            }
            '''
            self.assertEqual(mocked, obj.as_dict(unique=True))
            self.assertEqual(mocked, obj.as_dict('lang', unique=True))
            self.assertEqual(mocked, obj.as_dict('*', unique=True))
            self.assertEqual(mocked, obj.as_list('lang', unique=True))
            self.assertEqual(mocked, obj.as_list('*', unique=True))

    def test_language_indexer(self):
        mocked = self.page.lang_sections['ru']
        '''
        LanguageSection(ru)
        '''
        self.assertEqual(mocked, self.page['ru'])
        self.assertEqual(mocked, self.page[0])

        mocked = self.page.lang_sections['en']
        '''
        LanguageSection(en)
        '''
        self.assertEqual(mocked, self.page['en'])
        self.assertEqual(mocked, self.page[1])

    def test_language_attr(self):
        mocked = self.page.lang_sections['ru']
        '''
        LanguageSection(ru)
        '''
        self.assertEqual(mocked, self.page.ru)

        mocked = self.page.lang_sections['en']
        '''
        LanguageSection(en)
        '''
        self.assertEqual(mocked, self.page.en)

    def test_homonyms_keys(self):
        mocked = ['']
        self.assertEqual(self.page['ru'].keys, mocked)
        self.assertEqual(self.page['ru'].homonyms.keys, mocked)

        mocked = ['I', 'II', 'III']
        self.assertEqual(self.page['en'].keys, mocked)
        self.assertEqual(self.page['en'].homonyms.keys, mocked)

    def test_homonyms_grouper(self):
        mocked = self.page.homonym_sections
        '''
        {
            'ru': {
                '': HomonymSection(),
            },
            'en': {
                'I': HomonymSection(I),
                'II': HomonymSection(II),
                'III': HomonymSection(III),
            },
        }
        '''
        self.assertEqual(mocked, self.page.homonyms.as_dict('*', unique=True))

        # todo: ...

    def test_lang_homonyms_grouper(self):
        pass  # todo


if __name__ == '__main__':
    unittest.main()
