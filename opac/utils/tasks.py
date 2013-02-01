import json

from django.conf import settings

from .sync import datacollector
from .sync import pipes


def full_sync():
    scielo_api = datacollector.SciELOManagerAPI(settings=settings)
    ppl = pipes.Pipeline(pipes.PIssue,
                         pipes.PMission,
                         pipes.PSection,
                         pipes.PCleanup)

    data = scielo_api.get_all_journals('saude-publica')
    transformed_data = ppl.run(data)

    with open('/tmp/journals.json', 'wb') as f:
        for d in transformed_data:
            f.write(json.dumps(d))
