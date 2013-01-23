Data model
==========

Resources
---------

* List all journals
    * /journal/
* Get journal
    * /journal/:journal_id/
* List issues bound to a journal
    * /issue/:journal_id/
* Get issue
    * /issue/:journal_id/:issue_id/
* Get article
    * /article/:article_id/


Journal
-------

.. code-block:: javascript

    {
      "abstract_keyword_languages": null,
      "acronym": "AISS",
      "collections": "/api/v1/collections/1/",
      "contact": null,
      "copyrighter": "Istituto Superiore di Sanità",
      "cover": null,
      "created": "2010-04-09T00:00:00",
      "creator": "/api/v1/users/1/",
      "ctrl_vocabulary": "nd",
      "current_ahead_documents": 0,
      "editor_address": "Viale Regina Elena 299, 00161 Italy Rome, Tel.: 0039 06 4990 2945, Fax: 0039 06 4990 2253",
      "editor_address_city": "",
      "editor_address_country": "",
      "editor_address_state": "",
      "editor_address_zip": "",
      "editor_email": "annali@iss.it",
      "editor_name": "",
      "editor_phone1": "",
      "editor_phone2": null,
      "editorial_standard": "vancouv",
      "eletronic_issn": "",
      "final_num": "",
      "final_vol": "",
      "final_year": null,
      "frequency": "Q",
      "id": 1,
      "index_coverage": "chemabs\nembase\nmedline\npascal\nzoological records",
      "init_num": "1",
      "init_vol": "1",
      "init_year": "1965",
      "is_indexed_aehci": false,
      "is_indexed_scie": false,
      "is_indexed_ssci": false,
      "issues": [
        { "id": 1,
          "data": {
            "cover": null,
            "created": "2010-04-01T01:01:01",
            "ctrl_vocabulary": "nd",
            "editorial_standard": "vancouv",
            "id": 1,
            "is_marked_up": false,
            "is_press_release": false,
            "is_trashed": false,
            "label": "45 (4)",
            "number": "4",
            "order": 4,
            "publication_end_month": 12,
            "publication_start_month": 10,
            "publication_year": 2009,
            "resource_uri": "/api/v1/issues/1/",
            "sections": [
            {
              "id": 514,
              "articles": [
                "AISS-JHjashA",
              ]
            }
            ],
            "suppl_number": null,
            "suppl_volume": null,
            "total_documents": 17,
            "updated": "2012-11-08T10:35:37.193612",
            "volume": "45"
            }
        }
      ],
      "languages": [
        "en",
        "it"
      ],
      "logo": null,
      "medline_code": null,
      "medline_title": null,
      "missions": [
        {'en': 'To disseminate information on researches in public health'}
      ],
      "national_code": null,
      "notes": "",
      "other_previous_title": "",
      "other_titles": [],
      "previous_ahead_documents": 0,
      "print_issn": "0021-2571",
      "pub_level": "CT",
      "pub_status": "current",
      "pub_status_history": [
        {
          "date": "2010-04-01T00:00:00",
          "status": "current"
        }
      ],
      "pub_status_reason": "",
      "publication_city": "Roma",
      "publisher_country": "IT",
      "publisher_name": "Istituto Superiore di Sanità",
      "publisher_state": "",
      "resource_uri": "/api/v1/journals/1/",
      "scielo_issn": "print",
      "secs_code": "",
      "short_title": "Ann. Ist. Super. Sanità",
      "sponsors": [
        1
      ],
      "study_areas": [
        "Agricultural Sciences"
      ],
      "subject_descriptors": "public health",
      "title": "Annali dell'Istituto Superiore di Sanità",
      "title_iso": "Ann. Ist. Super. Sanità",
      "updated": "2012-11-08T10:35:00.448421",
      "url_journal": null,
      "url_online_submission": null,
      "use_license": {
        "disclaimer": "",
        "id": 1,
        "license_code": "",
        "reference_url": null,
        "resource_uri": "/api/v1/uselicenses/1/"
      },
      "sections": [
        {
          "id": 514,
          "resource_uri": "/api/v1/sections/514/",
          "titles": [
            {"en": "WHO Publications"}
          ]
        }
      ]
    }


Article
-------

.. code-block:: javascript

    {
      "abstract": {
        "en": "<p>Trout farming, that represents the most important sector for aquaculture inland production in Italy, can cause negative effects on aquatic ecosystems. Recently, in the framework of Water Frame Directive 2000/60/EC and national law DL 152/2006, concerning the sustainable uses of water resources, multi-criteria approaches have been suggested to evaluate the impact of fish farming on aquatic ecosystems. In this study trout farms of central Italy were selected to investigate the effects of their effluents, on receiving water bodies using a multi-criteria approach based on physicochemical parameters, microbiological and macrobenthonic indicators, detected in sampling stations located upstream/downstream the trout farm. Moreover, antibiotic susceptibility against antibiotics allowed and/or forbidden by current law (D.lgs 193/56/06) was tested on E. coli strains. The results indicate variations of chemical parameters and biological indicators from upstream to downstream sites in some of the investigated farms. Antibiotic resistance of E. coli strains suggested a large use of tetracycline and a possible past use of chloramphenicol. This study represents a first contribute to the knowledge of fish farm impacts on aquatic systems in Central Italy.
</p>",
        "it": "<p>La troticoltura rappresenta il settore più importante per la produzione ittica in Italia ed è in grado di causare effetti negativi sugli ecosistemi acquatici. Recentemente, dopo l'emanazione della Direttiva Europea 2000/60/CE sulla tutela delle acque, e il suo recepimento a livello nazionale con il DL 152/2006 riguardante gli usi sostenibili delle risorse idriche, è stata consigliata l'adozione di un approccio multi-livello nella valutazione dell'impatto causato dagli impianti di acquacoltura. dieci troticolture dell'Italia centrale sono state selezionate per esaminare gli effetti dei loro scarichi sugli ecosistemi acquatici, utilizzando un approccio multi-livello. Sono stati analizzati parametri fisici, chimici, indicatori microbiologici e i macroinvertebrati bentonici in stazioni di campionamento situate a monte e a valle degli impianti. La resistenza a tre antibiotici consentiti ed ad uno proibito dall'attuale legge (DL 193/56/06) è stata testata su ceppi di E. coli. I risultati ottenuti mostrano cambiamenti dei parametri chimici e degli indicatori biologici e microbiologici nei siti a valle di alcuni impianti. La resistenza agli antibiotici in ceppi di E. coli ha mostrato un ampio uso delle tetracicline e un possibile uso passato del cloramfenicolo. In conclusione, questo studio rappresenta un primo contribuito alla conoscenza degli impatti sui sistemi acquatici causati dagli impianti di troticoltura dell' Italia centrale.</p>"
      },
      "journal-id": "aiss",
      "lpage": "302",
      "journal-title": "Annali dell'Istituto Superiore di Sanit\u00e0",
      "fpage": "299",
      "contrib-group": {
        "author": [
          {
            "role": "ND",
            "given-names": "Ahmet",
            "surname": "Soysal",
            "affiliations": [
              "A01"
            ]
          },
          {
            "role": "ND",
            "given-names": "Hatice",
            "surname": "Simsek",
            "affiliations": [
              "A01"
            ]
          },
          {
            "role": "ND",
            "given-names": "Dilek",
            "surname": "Soysal",
            "affiliations": [
              "A02"
            ]
          },
          {
            "role": "ND",
            "given-names": "Funda",
            "surname": "Alyu",
            "affiliations": [
              "A03"
            ]
          }
        ]
      },
      "default-language": "en",
      "volume": "46",
      "number": "3",
      "pub-date": {
        "year": "2010"
      },
      "issn": "0021-2571",
      "publisher-loc": "Roma",
      "abbrev-journal-title": "Ann. Ist. Super. Sanit\u00e0",
      "affiliations": [
        {
          "addr-line": "Izmir",
          "ref": "A01",
          "institution": "Dokuz Eylul University",
          "country": "Turkey"
        },
        {
          "ref": "A02",
          "institution": "Dokuz Eylul University",
        },
        {
          "addr-line": "Izmir",
          "ref": "A03",
          "institution": "Ataturk Training and Research Hospital",
          "country": "Turkey"
        }
      ],
      "keyword-group": {
        "en": [
          "health-care waste",
          "waste management"
        ],
        "pt": [
          "rifiuti sanitari",
          "Uso de Medicamentos",
          "Inqu\u00e9ritos de Morbidade"
        ],
        "it": [
          "Personas con Discapacidad",
          "gestione dei rifiuti"
        ]
      },
      "subjects": {
        "wos": [
          "PUBLIC, ENVIRONMENTAL",
          "OCCUPATIONAL HEALTH"
        ]
      },
      "article-ids": {
        "publisher-id": "S0021-25712010000300013"
      },
      "publisher-name": "Istituto Superiore di Sanit\u00e0",
      "title-group": {
        "en": "Management of health-care waste in Izmir, Turkey",
        "it": "Gestione dei rifiuti sanitari in Izmir, Turchia"
      }
    }


Sponsor
-------

.. code-block:: javascript

    {
      "acronym": "",
      "address": "",
      "address_complement": "",
      "address_number": "",
      "cel": "",
      "city": "",
      "complement": "",
      "country": "",
      "created": "2012-11-08T10:34:59.844065",
      "email": "",
      "fax": "",
      "id": 1,
      "name": "Istituto Superiore di Sanit\u00e0",
      "phone": "",
      "resource_uri": "/api/v1/sponsors/1/",
      "state": "",
      "updated": "2012-11-08T10:34:59.844096",
      "zip_code": null
    }




References
==========

* iso 639-1: http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
* iso 8601: http://en.wikipedia.org/wiki/ISO_8601
