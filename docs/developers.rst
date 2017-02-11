.. _developers:

==========
Developers
==========

Running the Test Suite
======================

Tests for ``DPP`` are organized in an own django project called ``bpw_tests`` located under the
folder ``tests``. For running the test suite the following libraries are required:

* `Selenium <http://selenium-python.readthedocs.org/en/latest/>`_ 2.45+
* `django-dynamic-fixture <https://github.com/paulocheque/django-dynamic-fixture>`_ 1.8+

The following types of tests are implemented:

Test Server
-----------
A test server is necessary to run some of the tests (e.g. testing RSS feeds). The data for the 
test server configuration can be created with::

	./init_test_project.sh

This doesn't has to be done every time before running the tests, but at least once and every time
after updating the ``DPP`` library.

The test server can than be started with::

    ./testserver.sh

The test server serves a normal ``DPP`` instance and both the frontend site and the admin should be
normally accessible through the browser:

* http://127.0.0.1:8010/
* http://127.0.0.1:8010/admin/

Browser/Selenium Tests
----------------------
The purpose of Selenium tests is to test the front-end functionality of the site. Tests are
organized in the app ``browser`` and can be run from within the ``tests`` directory with::

    python manage.py test browser #whole test suite
    python manage.py test browser.GenericTest #one test case
    python manage.py test browser.GenericTest.test_main_page #a single test method

Testing the 404 Template
------------------------
When ``DEBUG`` is set to ``True`` in ``settings.py``, ``404 template`` can be tested via the following
url::

    http://yourdevelopmenturl/404test/


How to contribute: Translation
==============================

General How-To
--------------
The main area for contribution for this project is translation, since the scope of the software is relatively
wide. So if you have got some time, speak English as a base language and another language like Spanish, Russian, 
French,... you are very welcome to help out (you don't need to be a developer for this task)!

You find the basic english language file called ``django.po`` on the 
`DPP GitHub Page <https://github.com/holgerd77/django-public-project>`_
in the following folder::
    
    public_project/locale/en/LC_MESSAGES/
    
Open this file and copy its contents. Then write the translation of the ``msg`` id strings between the 
double quotes after the ``msstr`` attribute. For longer strings you can use a format like this::

    #: models.py:123
    msgid "Structural parts of the project being stable over time."
    msgstr ""
    "Structural parts of the project being stable over time, e.g. 'Terminals', "
    "'Gates', 'Traffic Control', 'Integration of Public Transportation', not too "
    "much (<10), often useful as well: one entry for the project as a whole."
    
Just replace the ``msgstr`` with the translation in your language. If there is already a ``msgstr`` in 
english in the ``django.po`` file, use this string as a translation basis instead of ``msgid`` and
replace the english string with your language translation.

When you are ready with your translation open an issue on GitHub and past your text there or (advanced
developer version) make a pull request.

.. note:: If you have got limited time: please choose accuracy over speed, it's more helpful if you translate
          20 strings in an appropriate manner and take some time to think about the translation than translating
          50 strings and often missing the context or have spelling errors!


Generating/compiling message files
----------------------------------

For generating the message files for a specific locale from the source identifiers, change to the ``public_project``
app directory and generate the message file for the desired locale with::

    django-admin.py makemessages -l de

Then translate the missing identifier strings and compile the message files with::

    django-admin.py compilemessages

.. _release_notes:

Release Notes
=============
**Changes in version 0.7.2-beta** (2017-02-11) 

* Slugified/more meaningful URLs for topics, questions, events and participants
* New ``DPP_CUSTOM_JS`` and ``DPP_CUSTOM_CSS`` settings to include custom Javscript code or 
  CSS styles in the project (see: :ref:`custom_js_css`)
* Added admin website configuration settings for optionally not showing goals and questions categories and
  deactivating user comments, new migration ``0004_activation_flags_for_goals_questions_comments``

**Changes in version 0.7.1-beta** (2015-08-31)

* Updated ``Bootstrap`` from ``2.3`` to ``3.3``
* Improved menu navigation on mobile devices

**Changes in version 0.7.0-beta** (2015-08-27)

* Support for ``Django 1.8`` (support for older versions dropped)
* Switched to ``Django`` internal migrations. South dependencies are removed, but you can still find the
  old ``South`` migration files in the ``south_migrations`` folder. To make sure the update runs smoothly
  make sure you have applied all ``South`` migrations from the previous releases. In doubt update to the
  latest ``0.6`` release first and run the ``migrate`` command within ``South`` context before switching
  to this release. Then from ``0.7`` run the ``migrate`` command with the ``--fake-initial`` flag: ``python manage.py migrate --fake-initial``.
* Updated requirements of various library dependencies
* Fixed a bug for document comments

**Changes in version 0.6.3-beta** (2014-12-08)

* Fixed some unnecessary error messages caused by crawlers

**Changes in version 0.6.2-beta** (2014-10-18)

* Minor layout and admin improvements

**Changes in version 0.6.1-beta** (2014-10-18)

* Layout improvements for sites not using all customizations from new DPP version

**Changes in version 0.6-beta** (2014-08-21)

* Replaced structuring of participants by participant type with a more flexible concept allowing the
  **grouping participants to other participants (groups)** by a new attribute ``belongs_to`` in admin and
  a new many-to-many model ``Membership``. A membership is described by a ``function`` and a boolean field
  ``active``, connecting two participants. This is replacing the former concept ``responsible_participants``
  and ``former_responsible_participants``, which could be found in ``Project`` tabe. Both fields were
  removed. 
  DB changes: migrations ``0002_auto__del_field_participant_type.py``, ``0003_auto.py``, ``0008_auto_add_membership.py``.
* **Project Parts (Topics) can now also be hierarchically structured**, every project part object now has a new
  attribute ``main_project_part`` allowing to connect project parts to a main topic. This new structure
  (as well as the participant grouping) will be visible in the frontend as well.
  DB changes: migration ``0004_auto_add_field_projectpart_main_project_part.py``
* **New SiteCategory model** for providing intro texts to the website categories ("Home", "Questions", ...)
  and connecting documents and websites with categories, **replacing the old model Project (deleted)**.
  DB changes: migrations ``0005_auto_add_sitecategory.py``, ``0006_intro_texts_to_site_category.py``
  (for automatic data transfer from ``Project`` instance) and ``0007_auto_del_project.py``.
* **Direct integration of TinyMCE as HTML editor** for descriptive admin fields by overwriting Django admin
  templates. ``public_project`` app in ``INSTALLED_APPS`` in ``settings.py`` now has to be placed before (!)
  Django admin app, new ``TEMPLATE_CONTEXT_PROCESSOR`` ``public_project.context_processors.uploaded_images_list``
  (also has to be added to ``settings.py``) for loading images in Admin to be selectable by TinyMCE editor
* Introduction of new **main category for goals**
* Restructuring, icons and help text for admin, more information on overview pages
* Translation of admin interface
* Many **layout improvements**, overhaul of overview all overview pages with expand/collapse boxes and displaying
  number of sub elements
* New **universal search box**
* Completely revamped documentation

**Changes in version 0.5-alpha (Renaming Release)** (2013-05-27)

This release is just for renaming the Django app. Due to the development of the software it came up,
that the focus of the software is broader than actually thought, so the name ``django-big-projects-watch`` (BPW)
is misleading and the software was renamed to ``django-public-project`` (DPP). This comes with a lot of
hassle and won't happen again in the lifecyle of this software, but I felt, that in this early stage
of the software, it is the only chance to make such a step.

If you already have a deployment of the software installed and have problems upgrading please contact
me (@HolgerD77).

On ``GitHub`` the software moved to a new repository https://github.com/holgerd77/django-public-project 
with a new commit history. The ``South`` history has been restarted as well.

Steps to manually upgrade:

1. BACKUP YOUR DATABASE! BACKUP YOUR PROJECT FOLDER!
2. Create a JSON dump of your project with the ``-n`` option for preserving natural keys, leave out
   the ``South`` tables: ``python manage.py dumpdata -n -e contenttypes -e auth.Permission -e south > bpw_dpp_dump.json``
3. Rename the suffix of ``django-public-project`` specific settings in ``settings.py`` from
   ``BPW`` to ``DPP``
4. Remove ``big_projects_watch`` from ``INSTALLED_APPS`` in your ``settings.py`` file
   and add ``public_project``.
5. Enter a new database name (for security reasons, leave old DB untouched) in your ``settings.py``.
6. Run ``python manage.py syncdb``, ``python manage.py migrate``, don't create a superuser
7. Search and replace all occurrences of ``big_projects_watch`` in your JSON DB dump with 
   ``public_project`` (e.g. in vi use ":%s/big_projects_watch/public_project/g"), keep a copy of the unmodified file!
8. Load your JSON dump in the new DB with ``python manage.py loaddata yourjsonfile.json``.
9. Test your application. Sorry for the inconvenience.


**Changes in version 0.4-alpha** (2013-05-04)

* New **activity feed on main page**, integrating different activities in the system like an admin user
  adding a new object (e.g. a new event, participant, ...) or an visitor on the website commenting
  on an object. New model ``ActivityLog`` (see Migration 0016), activities are always bound to objects
  in the system, concept is flexible and expandable so that new activities around system objects can
  be added in the future
* **RSS feeds** for various pages of the system, closely connected to the activity concept.
  Feeds for the different new system objects, new comments on certain objects, a general activity feed,
  a general comment feed and a feed for new research requests (see further down)
* **Own pages/urls for questions, expanded editorial possibilities**: every question now has an own
  url and expanded possibilities to be described, new model fields for ``Question`` model class
  (see Migration 0018)
* **Integration of questions in system comments**: questions can now be referenced by site visitors
  in there comments and questions can be commented itself as well
* **New research requests associated with questions**: site owners can now give research requests
  to the crowd, describing tasks to be done or information to be found in documents. A research 
  request is always associated with a question and can further - similar to comments - be associated
  with different system objects. Site admins can directly enter new requests on the associated
  question page.
* **Experimental version of a public API** Various objects in the system can now be accessed via
  a public JSON API if desired


**Changes in version 0.3-alpha** (2013-04-08)

* Layout overhall (category colors, bigger headlines, breadcrumb navigation, UI tweaks)
* ``WITH_PUBLIC_DOCS`` setting in ``settings.py`` replaced with ``BPW_IE_COMPATIBLE_PDF_VIEWER``
  (see: :ref:`installation`)
* New detail info boxes for events, documents, used on main page to highlight newest events, documents
* Introduced search tags as new information concept (new DB models ``SearchTag``, ``SearchTagCacheEntry``,
  use ``South`` when upgrading): provided in Django admin for Events, Participants, ProjectParts, used
  for tag cloud generation and displaying documents containing these search tags on detail pages for
  Events, Participants, ProjectParts
* Search tag clouds (click induces search) on main page, document pages
* One unified crowdsource concept, merging the former concepts ``DocumentRelations`` into a broader
  ``Comments`` concept. ATTENTION! THESE CHANGES COME ALONG WITH HEAVY DB CHANGES AND NEED MANUAL 
  WORK TO GET THINGS WORKING AGAIN!
  
  * When upgrading create a dump from your ``DocumentRelation``, ``Comment`` table entries first
  * ``DocumentRelation`` model is completely removed, entries have to be manually copied into
    ``Comment`` table 
  

**Changes in version 0.2-alpha** (2013-01-22)

* Layout based on Twitter Bootstrap
* Participants, ProjectParts, ProjectGoals, Events as basic project entities
* Modeling of questions around the project
* Document upload / PDF viewer based on pdf.js
* Crowdsourcing of comments / document relations

**Changes in version 0.1-pre-alpha** (2012-08-08)

* Initial verion

