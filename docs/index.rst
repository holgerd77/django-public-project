.. django-big-projects-watch documentation master file, created by
   sphinx-quickstart on Mon Aug  6 14:08:32 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-big-projects-watch - Documentation
=========================================

Django Public Project (DPP) is a specialised **content management system** written in ``Python/Django`` 
**for building an information website  around big projects**. It is open source (BSD licence) and can be used by civic groups 
to monitor the progress of publicly funded projects but also from within governmental institutions
itself to bring transparency in the proceeding of a project, inform the interested public about
what is going on and thus enhance the acceptance of the project by the different stakeholders. 

Use Cases
---------
This software was first used by the **pirate party in the parliament of Berlin** to monitor the progress
of the **Berlin Brandenburg Airport project**, see http://ber.piratenfraktion-berlin.de to get an
impression of the software (sorry, german).
 
Other possible use cases are:

* Construction/Infrastructure Projects
* IT/Software Projects
* Environmental Projects
* Law Making Processes

.. image:: images/screenshot_main_page.png 

Features
--------
DPP provides an **admin interface** for entering/updating:

* A general project description
* The goals of a project
* The project structure
* A timeline of events
* The various actors and stakehoders
* Project documents
* Questions around the project
* Web sources wherever possible

On the **frontend side**, it lays out the project data in a clearly represented way, 
interlinks between the different project elements and provides:

* A dashboard on the main page bringing together the most relevant, current information
* Universal search
* A document viewer for pdfs
* User comments interlinking different project elements
* Relevant tag clouds for document content
* Supported languages: English (beta), German

Manual
------

.. toctree::
   :maxdepth: 2
   
   users
   developers

Ressources
----------

* `Source Code on GitHub <https://github.com/holgerd77/django-big-projects-watch>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

