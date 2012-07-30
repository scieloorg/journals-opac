Journals OPAC (Catálogo Online de revistas da coleção SciELO)
==============================================================

Ferramenta que expõe, para o usuário final, o catálogo de uma coleção SciELO.


Necessidades:
--------------

* Facilidade de instalação.
* Interoperação com os dados do SciELO Manager.


Requisitos:
-----------

* Toda a configuração deve ser realizada via interface web.
* Os dados de revista, fascículo, sessões e artigo devem ser sincronizados
  com o SciELO Manager (ferramenta de gestão do catálogo), de maneira que
  sempre que houver atualização nos dados estes sejam replicados para o
  OPAC.
* O sistema deve permitir que o administrador controle a visibilidade de
  revistas, fascículos e artigos.
* O sistema deve permitir que o administrador habilite/desabilite/configure
  as funcionalidades da caixa de serviços.
* O sistema deve suportar internacionalidação.
* O sistema deve permitir a gestão de alguns dados do periódico, tais como:
  Sobre a revista, Corpo editorial, Instruções aos autores, Assinaturas e
  o Rodapé (markdown?).


Modelo de dados:
----------------

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
          "missions": {"es": <string>, "en": <string>, "pt": <string>},
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
          "journal_ref": {"id": <id>, "title": <string>},
          "articles": [
            {}
          ]
        }
