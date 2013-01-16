# coding: utf-8

import unittest

import mocker


class PipeTests(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.pipes import Pipe
        return Pipe(*args, **kwargs)

    def test_pipe_cannot_be_instantiated(self):
        data = {
                    'abstract_keyword_languages': None,
                    'acronym': 'AISS',
                }

        self.assertRaises(TypeError, lambda: self._makeOne(data))

    def test_returns_an_iterator(self):
        from utils.sync.pipes import Pipe

        class Blitz(Pipe):
            def transform(self, data):
                return 'Foo'

        data = {
                    'abstract_keyword_languages': None,
                    'acronym': 'AISS',
                }

        p = Blitz(data)
        self.assertTrue(hasattr(iter(p), 'next'))

    def test_accepts_generator_objects(self):
        from utils.sync.pipes import Pipe

        class Blitz(Pipe):
            def transform(self, data):
                return 'Foo'

        def make_generator():
            data = {
                        'abstract_keyword_languages': None,
                        'acronym': 'AISS',
                    }
            yield data

        p = Blitz(make_generator())
        self.assertTrue(hasattr(iter(p), 'next'))

    def test_fetch_resource(self):
        from utils.sync.pipes import Pipe
        data = {
                    'issues': [
                        '/api/v1/issues/1/'
                    ]
                }

        expected = {
            'cover': None,
            'created': '2010-04-01T01:01:01',
            'ctrl_vocabulary': 'nd',
            'editorial_standard': 'vancouv',
            'id': 1,
            'is_marked_up': False,
            'is_press_release': False,
            'is_trashed': False,
            'journal': '/api/v1/journals/1/',
            'label': '45 (4)',
            'number': '4',
            'order': 4,
            'publication_end_month': 12,
            'publication_start_month': 10,
            'publication_year': 2009,
            'resource_uri': '/api/v1/issues/1/',
            'sections': [
            '/api/v1/sections/514/',
            ],
            'suppl_number': None,
            'suppl_volume': None,
            'total_documents': 17,
            'updated': '2012-11-08T10:35:37.193612',
            'volume': '45'
        }

        class Blitz(Pipe):
            def transform(self, data):
                """This is just a placebo"""

        blitz = Blitz(data)
        res = blitz._fetch_resource('issues', '1')

        self.assertEqual(res, expected)

    def test_passing_precondition(self):
        from utils.sync import pipes
        precond = self.mocker.mock()

        precond(mocker.ANY)
        self.mocker.result(None)

        self.mocker.replay()

        class Blitz(pipes.Pipe):
            @pipes.precondition(precond)
            def transform(self, data):
                return {
                    'abstract_keyword_languages': None,
                    'acronym': 'AISS',
                }

        data = {
                    'abstract_keyword_languages': None,
                    'acronym': 'AISS',
                }

        p = Blitz(data)
        self.assertEqual(iter(p).next(), data)


class PIssueTest(unittest.TestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.pipes import PIssue
        return PIssue(*args, **kwargs)

    @unittest.expectedFailure
    def test_full_transformation(self):
        data = {
                    'issues': [
                        '/api/v1/issues/1/'
                    ]
                }
        pissue = self._makeOne(data)

        expected = {
            'issues': [
                {
                  'cover': None,
                  'created': '2010-04-01T01:01:01',
                  'ctrl_vocabulary': 'nd',
                  'editorial_standard': 'vancouv',
                  'id': 1,
                  'is_marked_up': False,
                  'is_press_release': False,
                  'is_trashed': False,
                  'label': '45 (4)',
                  'number': '4',
                  'order': 4,
                  'publication_end_month': 12,
                  'publication_start_month': 10,
                  'publication_year': 2009,
                  'resource_uri': '/api/v1/issues/1/',
                  'sections': [
                    '/api/v1/sections/514/',
                  ],
                  'suppl_number': None,
                  'suppl_volume': None,
                  'total_documents': 17,
                  'updated': '2012-11-08T10:35:37.193612',
                  'volume': '45'
                }
            ],
        }

        self.assertEqual(iter(pissue).next(), expected)
