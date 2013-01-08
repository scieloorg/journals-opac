==================
Documento de Visão
==================

Motivações
==========

* Manter a arquitetura de aplicações e os serviços disponibilizados aos usuário em um padrão 
  internacional de qualidade, diminuir os :doc:`custos operacionais, de manutenção e suporte a rede 
  SciELO<characteristics>`, permitindo a atualização dos aplicações de forma automática equacionando 
  a qualidade tecnologica de todas as coleções da Rede SciELO e de coleções não certificadas que 
  fazem uso das aplicações da metodologia.

* Empoderar o desenvolvimento de novas aplicações e serviços, evoluindo a arquitetura das aplicações
  SciELO para um padrão de profissionalismo equiparado a grandes empresas do mercado 
  disponibilizando API's de desenvolvimento para todos os novos produtos produzidos dentro do 
  contexto do projeto SciELO.

* A evolução contínua e a necessidade inerente as profissões e produtos de tecnologia de se manterem 
  atualizados deve ser considerado um fator primordial para sustentabilidade de projetos que possuem 
  em seu cerne uma diversidade de produtos de tecnologia. A estagnação tecnológica a longo prazo 
  pode significar a falência de projetos onde a tecnologia tem um grande papel.

Antecedentes
============

A necessidade de reestruturar a arquitetura das aplicações de publicação de artigos, fascículos e
periódicos no contexto do projeto SciELO veio inicialmente pela equipe de desenvolvimentos que 
sentia muita dificuldade em manter a arquitetura das aplicações da metodologia SciELO evoluindo
de acordo com as novidades do mercado devido ao uso de processos, aplicações, linguagens e sistemas 
de bancos de dados obsoletos.

De acordo com as motivações citadas e a necessidade urgente de reestruturar a arquitetura 
tecnologica da metodologia SciELO, decidiu-se realizar uma série de desenvolvimentos com a intenção
de resgatar a arquitetura tecnológica da SciELO para um novo padrão de qualidade.

O Journals OPAC compreende a segunda fase de desenvolvimentos de um pacote de aplicações para 
a reestruturação da arquitetura de aplicações do projeto SciELO.

Escopo do Projeto
=================

Esta aplicação pretende dar suporte ao processo de publicação on-line da metodologia SciELO. Sua
função se resume em fornecer funcionalidades que permitam aos gestores de coleções criar seus
corpus_ de publicação para diversas coleções de países, temáticas e outras.

.. _Corpus: http://en.wikipedia.org/wiki/Text_corpus

Objetivo do Projeto
===================

Este projeto tem como objetivo criar uma ferramenta como serviço, para suporte a publicação
de periódicos científicos operados no contexto da Rede SciELO substituindo a atual ferramenta 
de publicação de artigos e periódicos.

Quais problemas esta aplicação deve solucionar?
===============================================

* Migrar toda rede SciELO para uso das novas aplicações.
* Mudança de paradigma para o uso de aplicações como serviço. (Application as a Service)
* Mudança de paradigma de uso de uma arquitetura decentralizada para uma arquitetura centralizada.

Macro Necessidades
==================

* Software as a service.
* Capacidade de instalação remota.
* Interoperação com os dados do SciELO Manager.
* Serviços de estatísticas de acessos.
* Serviços de interoperabilidade de metadados. (OAI-PMH, SWORD)
* Exportação de metadados (WoS, DOAJ).
* Gestão de páginas secundárias, seja por um usuário da equipe SciELO ou um usuário do tipo editor.
* Gestão de corpo editorial, seja por um usuário da equipe SciELO ou um usuário do tipo editor.
* API's para acesso a todo dado produzido pelas coleções.
* Exportação de metadados para formatos legados, json e xml.
* Interface Web
* Interface Mobile

Requisitos Funcionais
=====================

* Toda a configuração deve ser realizada via interface web.
* Os dados de revista, fascículo, sessões e artigo devem ser sincronizados com o `SciELO Manager`__
  (ferramenta de gestão do catálogo), de maneira que sempre que houver atualização nos dados estes 
  sejam replicados para o OPAC.
* O sistema deve permitir que o administrador controle a visibilidade de revistas, fascículos e 
  artigos.
* O sistema deve permitir que o administrador habilite/desabilite/configure as funcionalidades da 
  caixa de serviços.
* O sistema deve suportar internacionalidação.
* O sistema deve ser capaz de apresentar gráficos de uso do conteúdo acessado.
* O sistema deve ser capaz de apresentar de forma diferenciada os artigos que possuem o texto 
  completo marcado.

Requisitos não definidos
------------------------

* A criação de coleções fica a cargo apenas de usuários administradores do SciELO, a rede não poderá
  criar coleções através do OPAC?
  
* Editores terão quais permissões no sistema? para edição de corpo editorial e páginas secundárias 
  apenas, ou para dados do periódico também?

* O sistema deve permitir a gestão de alguns dados do periódico, tais como: Sobre a revista, Corpo 
  editorial, Instruções aos autores, Assinaturas e o Rodapé (markdown?). Ou essa funcionalidade será
  uma aplicação no Journal Manager?

* O mockup home_periodico defini serviços de notícias e notas do editor. Esse produto será
  desenvolvido no contexto deste projeto? 

  * Este serviço poderia ser implementado junto com serviços de redes sociais, ou seja, ao indicar
    uma url de twitter, facebook ou outros serviços, uma aba é habilitada montrando os highlights
    postados pelos editores nessas redes sociais.

.. _SciELOManager: http://manager.scielo.org/

__ SciELOManager_


Requisitos Não Funcionais
=========================

Glossário
=========

DOAJ
----

JSON (Java Script Object Notation)
----------------------------------

OAI-PMH 
-------

O `OAIPMH`_ é um protocolo para disseminação de metadados contidos em repositórios.

.. _OAIPMH: http://www.openarchives.org/pmh/

OPAC
----

Software as a service
---------------------

Essa característica é dada a aplicações que podem ser utilizadas apenas criando um usuário e senha, 
e a partir desta conta de usuário todos os serviços e aplicações ficam disponíveis para este 
usuário. Essa característica de arquitetura de software vem sendo largamente utilizada em serviços 
que requerem alto grau de complexidade na manutenção e operação. Com essa arquitetura a complexidade
de manutenção e operação passa a ser gerida de forma  centralizada, entretanto, todos os recursos e 
serviços da aplicação são implementados em um ambiente decentralizado de gestão de conteudo.

SWORD
-----

Web of Science (WoS)
--------------------




