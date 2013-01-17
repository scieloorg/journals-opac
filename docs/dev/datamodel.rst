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
        "en": "<p>OBJECTIVE: To analyze the use of medicines and the main therapeutic groups consumed by persons with physical, hearing and visual disabilities. METHODS: A cross-sectional study was performed, where data from the 2002 Inqu\u00e9rito Multic\u00eantrico de Sa\u00fade no Estado de S\u00e3o Paulo (ISA-SP - S\u00e3o Paulo State Multicenter Health Survey), as well as the 2003 Inqu\u00e9rito de Sa\u00fade no Munic\u00edpio de S\u00e3o Paulo (ISA-Capital - City of S\u00e3o Paulo Health Survey), Southeastern Brazil, were analyzed. Respondents who reported having disabilities were studied, according to variables that comprise the database: geographic area, gender, income, age group, ethnic group, use of medicines and types of drugs consumed. RESULTS: The percentage of use of drugs by persons with disabilities was 62.8% among the visually impaired; 60.2% among the hearing impaired; and 70.1% among the persons with physical disabilities. Individuals with physical disabilities consumed 20% more medications than non-disabled ones. Among persons with visual disabilities, the most frequently consumed drugs were diuretics, agents of the renin-angiotensin system and analgesics. Persons with hearing disabilities used more analgesics and agents of the renin-angiotensin system. Among those with physical disabilities, analgesics, antithrombotics and agents of the renin-angiotensin system were the most frequently consumed medicines. CONCLUSIONS: There was a greater use of medicines among persons with disabilities than non-disabled ones. Persons with physical disabilities were those who most consumed medicines, followed by the visually impaired and the hearing impaired.</p>",
        "es": "<p>OBJETIVO: Analizar el consumo de medicamentos y los principales grupos terap\u00e9uticos consumidos por personas con deficiencias f\u00edsicas, auditivas o visuales. M\u00c9TODOS: Estudio transversal en que fueron analizados datos de la Pesquisa Multicentrica de Salud en el Estado de Sao Paulo (ISA-SP) en 2002 y de la Pesquisa de Salud en el Municipio de Sao Paulo (ISA-Capital), realizado en 2003. Los entrevistados que refirieron deficiencias fueron estudiados seg\u00fan las variables que componen el banco de datos: \u00e1rea, sexo, renta, grupo etario, raza, consumo de medicamentos y tipos de medicamentos consumidos. RESULTADOS: El porcentaje de consumo entre las personas con deficiencia fue de: 62,8% entre los visuales; 60,2% entre los auditivos y de 70,1% entre los f\u00edsicos. Las personas con deficiencia f\u00edsica consumieron 20% m\u00e1s medicamentos que los no deficientes. Entre las personas con deficiencia visual, los medicamentos m\u00e1s consumidos fueron los diur\u00e9ticos, agentes del sistema renina-angiotensina y analg\u00e9sicos. Personas con deficiencia auditiva utilizaron m\u00e1s analg\u00e9sicos y agentes del sistema renina-angiotensina. Entre individuos con deficiencia f\u00edsica, analg\u00e9sicos, antitromb\u00f3ticos y agentes del sistema renina-angiotensina fueron los medicamentos m\u00e1s consumidos. CONCLUSIONES: Hubo mayor consumo de medicamentos entre las personas con deficiencias al compararse con los no deficientes, siendo los individuos con deficiencia f\u00edsica los que m\u00e1s consumieron f\u00e1rmacos, seguidos de los deficientes visuales y auditivos</p>",
        "pt": "<p>OBJETIVO: Analisar o consumo de medicamentos e os principais grupos terap\u00eauticos consumidos por pessoas com defici\u00eancias f\u00edsicas, auditivas ou visuais. M\u00c9TODOS: Estudo transversal em que foram analisados dados do Inqu\u00e9rito Multic\u00eantrico de Sa\u00fade no Estado de S\u00e3o Paulo (ISA-SP) em 2002 e do Inqu\u00e9rito de Sa\u00fade no Munic\u00edpio de S\u00e3o Paulo (ISA-Capital), realizado em 2003. Os entrevistados que referiram defici\u00eancias foram estudados segundo as vari\u00e1veis que comp\u00f5em o banco de dados: \u00e1rea, sexo, renda, faixa et\u00e1ria, ra\u00e7a, consumo de medicamentos e tipos de medicamentos consumidos. RESULTADOS: A percentagem de consumo entre as pessoas com defici\u00eancia foi de: 62,8% entre os visuais; 60,2% entre os auditivos e 70,1% entre os f\u00edsicos. As pessoas com defici\u00eancia f\u00edsica consumiram 20% mais medicamentos que os n\u00e3o-deficientes. Entre as pessoas com defici\u00eancia visual, os medicamentos mais consumidos foram os diur\u00e9ticos, agentes do sistema renina-angiotensina e analg\u00e9sicos. Pessoas com defici\u00eancia auditiva utilizaram mais analg\u00e9sicos e agentes do sistema renina-angiotensina. Entre indiv\u00edduos com defici\u00eancia f\u00edsica, analg\u00e9sicos, antitromb\u00f3ticos e agentes do sistema renina-angiotensina foram os medicamentos mais consumidos. CONCLUS\u00d5ES: Houve maior consumo de medicamentos entre as pessoas com defici\u00eancias quando comparados com os n\u00e3o-deficientes, sendo os indiv\u00edduos com defici\u00eancia f\u00edsica os que mais consumiram f\u00e1rmacos, seguidos de deficientes visuais e auditivos.</p>"
      },
      "journal-id": "rsp",
      "lpage": "610",
      "journal-title": "Revista de Sa\u00fade P\u00fablica",
      "fpage": "601",
      "contrib-group": {
        "author": [
          {
            "role": "ND",
            "given-names": "Shamyr Sulyvan",
            "surname": "Castro",
            "affiliations": [
              "A01"
            ]
          },
          {
            "role": "ND",
            "given-names": "Americo Focesi",
            "surname": "Pelicioni",
            "affiliations": [
              "A02"
            ]
          },
          {
            "role": "ND",
            "given-names": "Chester Luiz Galv\u00e3o",
            "surname": "Cesar",
            "affiliations": [
              "A03"
            ]
          },
          {
            "role": "ND",
            "given-names": "Luana",
            "surname": "Carandina",
            "affiliations": [
              "A04"
            ]
          },
          {
            "role": "ND",
            "given-names": "Marilisa Berti de Azevedo",
            "surname": "Barros",
            "affiliations": [
              "A05"
            ]
          },
          {
            "role": "ND",
            "given-names": "Maria Cecilia Goi Porto",
            "surname": "Alves",
            "affiliations": [
              "A06"
            ]
          },
          {
            "role": "ND",
            "given-names": "Mois\u00e9s",
            "surname": "Goldbaum",
            "affiliations": [
              "A07"
            ]
          }
        ]
      },
      "default-language": "pt",
      "volume": "44",
      "pub-date": {
        "year": "2010",
        "month": "08"
      },
      "issn": "0034-8910",
      "publisher-loc": "S\u00e3o Paulo",
      "abbrev-journal-title": "Rev. Sa\u00fade P\u00fablica",
      "affiliations": [
        {
          "addr-line": "S\u00e3o Paulo",
          "ref": "A01",
          "institution": "Universidade de S\u00e3o Paulo",
          "country": "Brasil"
        },
        {
          "addr-line": "S\u00e3o Paulo",
          "ref": "A02",
          "institution": "Faculdades Metropolitanas Unidas",
          "country": "Brasil"
        },
        {
          "addr-line": "S\u00e3o Paulo",
          "ref": "A03",
          "institution": "USP",
          "country": "Brasil"
        },
        {
          "addr-line": "Botucatu",
          "ref": "A04",
          "institution": "Universidade Estadual Paulista Julio de Mesquita Filho",
          "country": "Brasil"
        },
        {
          "addr-line": "Campinas",
          "ref": "A05",
          "institution": "Universidade Estadual de Campinas",
          "country": "Brasil"
        },
        {
          "addr-line": "S\u00e3o Paulo",
          "ref": "A06",
          "institution": "Secretaria de Sa\u00fade do Estado de S\u00e3o Paulo",
          "country": "Brasil"
        },
        {
          "addr-line": "S\u00e3o Paulo",
          "ref": "A07",
          "institution": "USP",
          "country": "Brasil"
        }
      ],
      "keyword-group": {
        "en": [
          "Disabled Persons",
          "Drug Utilization",
          "Drugs of Continuous Use",
          "Morbidity Surveys"
        ],
        "pt": [
          "Pessoas com Defici\u00eancia",
          "Uso de Medicamentos",
          "Inqu\u00e9ritos de Morbidade"
        ],
        "es": [
          "Personas con Discapacidad",
          "Utilizaci\u00f3n de Medicamentos",
          "Medicamentos de Uso Cont\u00ednuo",
          "Encuestas de Morbilidad"
        ]
      },
      "subjects": {
        "wos": [
          "PUBLIC, ENVIRONMENTAL & OCCUPATIONAL HEALTH",
          "SOCIOLOGY"
        ]
      },
      "article-ids": {
        "publisher-id": "S0034-89102010000400003",
        "doi": "10.1590/S0034-89102010000400003"
      },
      "publisher-name": "Faculdade de Sa\u00fade P\u00fablica da Universidade de S\u00e3o Paulo",
      "title-group": {
        "en": "Use of medicines by persons with disabilities in S\u00e3o Paulo state areas, Southeastern Brazil",
        "es": "Uso de medicamentos por personas con deficiencias en \u00e1reas del Estado de Sao Paulo, Sureste de Brasil",
        "pt": "Uso de medicamentos por pessoas com defici\u00eancias em \u00e1reas do estado de S\u00e3o Paulo"
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
      "name": "Istituto Superiore di Sanità",
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
