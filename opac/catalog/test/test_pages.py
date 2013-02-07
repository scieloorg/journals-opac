from django_webtest import WebTest
from django.core.urlresolvers import reverse


class AjxListJournalTweets(WebTest):

    def test_returns_400_code_when_request_isnot_ajax(self):
        from .modelfactories import JournalFactory
        j = JournalFactory.build(twitter_user='redescielo')

        response = self.app.get(
            reverse('catalog.ajx_list_journal_tweets',
                kwargs={'journal_id': j.acronym}),
            status=400
        )

        self.assertEqual(response.status_code, 400)

    def test_returns_400_code_when_the_journal_id_doesnot_exist(self):
        response = self.app.get(
            reverse('catalog.ajx_list_journal_tweets',
                kwargs={'journal_id': 'invalid'}),
            status=400,
            headers={'x-requested-with': 'XMLHttpRequest'},
        )

        self.assertEqual(response.status_code, 400)
