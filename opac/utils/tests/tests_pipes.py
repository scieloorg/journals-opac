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

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        mock_manager_api.fetch_data('issues', '1')
        self.mocker.result(expected)

        self.mocker.replay()

        class Blitz(Pipe):
            def transform(self, data):
                """This is just a placebo"""

        blitz = Blitz(data, manager_api_lib=mock_manager_api)
        res = blitz._fetch_resource('/api/v1/issues/1/')

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


class PIssueTest(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.pipes import PIssue
        return PIssue(*args, **kwargs)

    def test_full_transformation(self):
        data = [
            {
                'issues': [
                    '/api/v1/issues/1/'
                ]
            }
        ]

        expected_api_res = {
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

        expected = {
            'issues': [
                {
                    'id': 1,
                    'data': {
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
                }
            ],
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        mock_manager_api.fetch_data('issues', '1')
        self.mocker.result(expected_api_res)

        self.mocker.replay()

        pissue = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(iter(pissue).next(), expected)

    def test_issues_key_exists_and_its_value_is_a_valid_precondition(self):
        data = {
                    'issues': [
                        '/api/v1/issues/1/',
                        '/api/v1/issues/2/',
                        '/api/v1/issues/3/',
                    ]
                }

        from utils.sync.pipes import pissue_precondition

        self.assertIsNone(pissue_precondition(data))

    def test_wrong_endpoint_must_invalidade_the_precondition(self):
        data = {
                    'issues': [
                        '/api/v1/issues/1/',
                        '/api/v1/foo/2/',
                        '/api/v1/issues/3/',
                    ]
                }

        from utils.sync.pipes import pissue_precondition
        from utils.sync.pipes import UnmetPrecondition

        self.assertRaises(UnmetPrecondition, lambda: pissue_precondition(data))

    def test_invalid_resource_id_must_invalidade_the_precondition(self):
        data = {
                    'issues': [
                        '/api/v1/issues/1/',
                        '/api/v1/issues/bar/',
                        '/api/v1/issues/3/',
                    ]
                }

        from utils.sync.pipes import pissue_precondition
        from utils.sync.pipes import UnmetPrecondition

        self.assertRaises(UnmetPrecondition, lambda: pissue_precondition(data))

    def test_transformation_is_bypassed_if_precondition_fails(self):
        data = {
                    'issues': [
                        '/api/v1/foo/1/',
                        '/api/v1/issues/2/'
                    ]
                }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        self.mocker.replay()

        pissue = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(pissue.transform(data), data)


class PMissionTest(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.pipes import PMission
        return PMission(*args, **kwargs)

    def test_full_transformation(self):
        data = {
            "missions": [
                [
                    "en",
                    "To disseminate information on researches in public health."
                ]
            ]
        }

        expected = {
            'missions': {
                "en": "To disseminate information on researches in public health."
            }
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        self.mocker.replay()

        pmission = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(pmission.transform(data), expected)

    def test_missions_key_exists_and_its_value_is_a_valid_precondition(self):
        data = {
            'missions': '',
        }

        from utils.sync.pipes import pmission_precondition

        self.assertIsNone(pmission_precondition(data))

    def test_transformation_is_bypassed_if_precondition_fails(self):
        data = {
            'issues': [
                '/api/v1/foo/1/',
                '/api/v1/issues/2/'
            ]
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        self.mocker.replay()

        pmission = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(pmission.transform(data), data)


class PSectionTest(mocker.MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        from utils.sync.pipes import PSection
        return PSection(*args, **kwargs)

    def test_toplevel_transformation(self):
        data = {
            'sections': [
                '/api/v1/sections/514/',
            ],
        }

        expected_api_res = {
            'code': 'AISS-5pvs',
            'created': '2012-11-08T10:35:32.886155',
            'id': 514,
            'is_trashed': False,
            'issues': [
                '/api/v1/issues/1/'
            ],
            'journal': '/api/v1/journals/1/',
            'resource_uri': '/api/v1/sections/514/',
            'titles': [
                [
                    'en',
                    'WHO Publications'
                ]
            ],
            'updated': '2012-12-03T11:09:15.907132'
        }

        expected = {
            'sections': [
                {
                    'id': 514,
                    'resource_uri': '/api/v1/sections/514/',
                    'titles': [
                        {'en': 'WHO Publications'}
                    ]
                }
            ]
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        mock_manager_api.fetch_data('sections', '514')
        self.mocker.result(expected_api_res)

        self.mocker.replay()

        psection = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(psection.transform(data), expected)

    def test_innerlevel_transformation(self):
        data = {
            'issues': [
                {
                    'id': 1,
                    'data': {
                        'sections': [
                            '/api/v1/sections/514/',
                        ]
                    }
                }
            ],
            'sections': [
                '/api/v1/sections/514/',
            ],
        }

        expected_api_res = {
            'code': 'AISS-5pvs',
            'created': '2012-11-08T10:35:32.886155',
            'id': 514,
            'is_trashed': False,
            'issues': [
                '/api/v1/issues/1/'
            ],
            'journal': '/api/v1/journals/1/',
            'resource_uri': '/api/v1/sections/514/',
            'titles': [
                [
                    'en',
                    'WHO Publications'
                ]
            ],
            'updated': '2012-12-03T11:09:15.907132'
        }

        expected = {
            'issues': [
                {
                    'id': 1,
                    'data': {
                        'sections': [
                            {'id': 514},
                        ]
                    }
                },
            ],
            'sections': [
                {
                    'id': 514,
                    'resource_uri': '/api/v1/sections/514/',
                    'titles': [
                        {'en': 'WHO Publications'}
                    ]
                }
            ]
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        mock_manager_api.fetch_data('sections', '514')
        self.mocker.result(expected_api_res)

        self.mocker.replay()

        psection = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(psection.transform(data), expected)

    def test_sections_key_exists_and_its_value_is_a_valid_precondition(self):
        data = {
            'sections': '',
        }

        from utils.sync.pipes import psection_precondition

        self.assertIsNone(psection_precondition(data))

    def test_wrong_endpoint_must_invalidade_the_precondition(self):
        data = {
            'sections': [
                '/api/v1/sections/514/',
                '/api/v1/baz/515/',
                '/api/v1/sections/516/',
            ]
        }

        from utils.sync.pipes import psection_precondition
        from utils.sync.pipes import UnmetPrecondition

        self.assertRaises(UnmetPrecondition, lambda: psection_precondition(data))

    def test_invalid_resource_id_must_invalidade_the_precondition(self):
        data = {
            'sections': [
                '/api/v1/sections/514/',
                '/api/v1/sections/baz/',
                '/api/v1/sections/516/',
            ]
        }

        from utils.sync.pipes import psection_precondition
        from utils.sync.pipes import UnmetPrecondition

        self.assertRaises(UnmetPrecondition, lambda: psection_precondition(data))

    def test_transformation_is_bypassed_if_precondition_fails(self):
        data = {
            'sections': [
                '/api/v1/sections/514/',
                '/api/v1/baz/515/',
                '/api/v1/sections/516/',
            ]
        }

        mock_manager_api = self.mocker.mock()

        mock_manager_api('http://manager.scielo.org/api/v1/')
        self.mocker.result(mock_manager_api)

        self.mocker.replay()

        psection = self._makeOne(data, manager_api_lib=mock_manager_api)

        self.assertEqual(psection.transform(data), data)
