Modelo de dados
===============

    Coleções:

    * Preferences
    * Journal::

        {
          "abstract_keyword_languages": [<string>,],
          "acronym": <string>,
          "collections": [<list:string>,],
          "contact": {"email": <string>, "name": <string>},
          "copyrighter": <string>,
          "cover": <string:uri>,
          "created": <string>,
          "creator": <string:uri>,
          "ctrl_vocabulary": <string>,
          "editorial_standard": <string>,
          "eletronic_issn": <string>,
          "final_num": <string>,
          "final_vol": <string>,
          "final_year": <string>,
          "frequency": <string>,
          "id": <string>,
          "index_coverage": <string>,
          "init_num": <string>,
          "init_vol": <string>,
          "init_year": <string>,
          "is_trashed": <bool>,
          "languages": [<string>,],
          "logo": <string:uri>,
          "missions": {<string:iso639-1>: <string>},
          "national_code": <string>,
          "notes": <string>,
          "other_previous_title": <string>,
          "other_titles": {"paralleltitle": [<string>,], "other": [<string>,]},
          "print_issn": <string>,
          "pub_level": <string>,
          "pub_status": <string>,
          "pub_status_history": [{"date": <datetime>, "status": <string>}]
          "pub_status_reason": <string>,
          "publisher": <string:uri>,
          "resource_uri": <string:uri>,
          "scielo_issn": <string>,
          "secs_code": <string>,
          "short_title": <string>,
          "sponsors": [<string>,],
          "study_areas": [<string>,],
          "subject_descriptors": [<string>,],
          "title": <string>,
          "title_iso": <string>,
          "updated": <string>,
          "url_journal": <string>,
          "url_online_submission": <string>,
          "use_license": {"disclaimer": <string>, "license_code": <string>, "reference_url": <string>, "resource_uri": <string:uri>}
        }

    * Issue::

        {
          "journal_ref": {"id": <id>, "title": <string>, "issn": <string>},
          "abreviated_title": <string>,
          "volume": <int>,
          "number": <int>,
          "documents": [
            {
              "author": {
                "analytical": [{"firstname": <string>, "lastname": <string>, "role": <string>, "affiliations": [{"name": <string>, "divisions": [<string>,]}],
                "corporate": [{"name": <string>, "divisions": [<string>,]}]
              },
              "titles": {<string:iso639-1>: <string>},
              "pages": {"first": <int>, "last": <int>},
              "illustrative_material_type": [<string>,],
              "language": <string>,
              "is_trashed": <bool>,
              "dates": {"thesis": <date:iso8601>, "conference": <date:iso8601>, "publication": <date:iso8601>, "revision": <date:iso8601>},
              "publication_city": <string>,
              "publication_state": <string>,
              "publication_country": <string>,
              "doctopic": <string>,
              "abstract": {<string:iso639-1>: <string>},
              "keywords": {<string>: [{<string:iso639-1>: <string>}]},
              "created_at": <date:iso8601>,
              "bibliographic_standard": <string>,
              "schema_version": <float>,
              "sponsor": <string>,
              "literature_type": <string>,
              "pid": <string>
            }
          ]
        }



Referências
===========

* iso 639-1: http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
* iso 8601: http://en.wikipedia.org/wiki/ISO_8601
