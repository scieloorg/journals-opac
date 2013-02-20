# coding: utf-8
from __future__ import unicode_literals
import factory

from catalog import mongomodels


class IssueFactory(factory.Factory):
    FACTORY_FOR = mongomodels.Issue

    volume = u'45',
    is_marked_up = False,
    updated = u'2012-11-08T10:35:37.193612',
    resource_uri = u'/api/v1/issues/1/',
    total_documents = 17,
    created = u'2010-04-01T01:01:01',
    ctrl_vocabulary = u'nd',
    suppl_volume = None,
    cover = None,
    number = u'4',
    publication_end_month = 12,
    editorial_standard = u'vancouv',
    order = 4,
    publication_year = 2009,
    is_press_release = False,
    suppl_number = None,
    label = u'45 (4)',
    sections = [
        {
            u'articles': [u'AISS-JHjashA'],
            u'id': 514
        }
    ],
    is_trashed = False,
    publication_start_month = 10
    id = 1


class JournalFactory(factory.Factory):
    FACTORY_FOR = mongomodels.Journal

    editor_address = u'Viale Regina Elena 299'
    copyrighter = u'Istituto Superiore di Sanità'
    editor_address_city = u'Rome'
    editor_address_state = u'Rome'
    creator = u'/api/v1/users/1/'
    ctrl_vocabulary = u'nd'
    national_code = None
    updated = u'2012-11-08T10:35:00.448421'
    frequency = u'Q'
    url_journal = None
    short_title = u'Ann. Ist. Super. Sanità'
    previous_ahead_documents = 0
    final_num = ''
    logo = None
    publisher_country = u'IT'
    publisher_name = u'Istituto Superiore di Sanità'
    eletronic_issn = ''
    issues = [
        {
            u'data':
            {
                u'volume': u'45',
                u'is_marked_up': False,
                u'updated': u'2012-11-08T10:35:37.193612',
                u'resource_uri': u'/api/v1/issues/1/',
                u'total_documents': 17,
                u'created': u'2010-04-01T01:01:01',
                u'ctrl_vocabulary': u'nd',
                u'suppl_volume': None,
                u'cover': None,
                u'number': u'4',
                u'publication_end_month': 12,
                u'editorial_standard': u'vancouv',
                u'order': 4,
                u'publication_year': 2009,
                u'is_press_release': False,
                u'suppl_number': None,
                u'label': u'45 (4)',
                u'sections': [
                    {
                        u'articles': [u'AISS-JHjashA'],
                        u'id': 514
                    }
                ],
                u'id': 1,
                u'is_trashed': False,
                u'publication_start_month': 10
            },
            u'id': 1
        }
    ]
    url_online_submission = None
    init_vol = u'1'
    subject_descriptors = u'public health'
    twitter_user = u'redescielo'
    title = u"Annali dell'Istituto Superiore di Sanit\xe0"
    pub_status_history = [
        {u'date': u'2010-04-01T00:00:00', u'status': u'current'}
    ]
    id = 1
    final_year = None
    editorial_standard = u'vancouv'
    languages = [u'en', u'it']
    scielo_issn = u'print'
    collections = u'/api/v1/collections/1/'
    index_coverage = u'chemabs\nembase\nmedline\npascal\nzoological records'
    current_ahead_documents = 0
    init_year = u'1965'
    sections = [
        {
            u'data': {
                u'titles': {u'en': u'WHO Publications'},
                u'id': 514,
                u'resource_uri': u'/api/v1/sections/514/'
            },
            u'id': 514
        }
    ]
    is_indexed_aehci = False
    use_license = {
        u'reference_url': None,
        u'license_code': '',
        u'id': 1,
        u'resource_uri': u'/api/v1/uselicenses/1/',
        u'disclaimer': ''
    }
    other_titles = []
    secs_code = ''
    editor_address_country = u'Italy'
    acronym = u'AISS'
    publisher_state = ''
    is_indexed_scie = False
    sponsors = [1]
    abstract_keyword_languages = None
    editor_name = u'Istituto Superiore di Sanità'
    other_previous_title = ''
    study_areas = [u'Agricultural Sciences']
    medline_code = None
    init_num = u'1'
    publication_city = u'Roma'
    pub_level = u'CT'
    is_indexed_ssci = False
    missions = {
        u'en': u'To disseminate information on researches in public health'
    }
    editor_email = u'annali@iss.it'
    created = u'2010-04-09T00:00:00'
    medline_title = None
    final_vol = ''
    cover = None
    editor_phone2 = u'0039 06 4990 2253'
    editor_phone1 = u'0039 06 4990 2945'
    print_issn = u'0021-2571'
    editor_address_zip = u'00161'
    contact = None
    pub_status = u'current'
    pub_status_reason = ''
    title_iso = u'Ann. Ist. Super. Sanità'
    notes = ''
    resource_uri = u'/api/v1/journals/1/'
