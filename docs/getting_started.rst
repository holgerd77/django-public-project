.. _getting_started:

===============
Getting Started
===============

Introduction
============

Django Public Project (DPP) can be best described as a **special kind of Content Management System (CMS)**, tailored
to the peculiarities of big projects, which often tend to becoming fairely complex and intrasparent when they
evolve. Below is a screenshot of the front-end view of the example project:

.. image:: images/screenshots/v06/example_project_dashboard.png

Use Cases
---------

With DPP it is possible to build up an in-depth information website around a big project which can be used...

* ... **by administration** to inform the public about the progress of an ongoing project and so increase
  acceptance for it.
* ... **by civic groups** to monitor the progress of a project.
* ... **by parliament** for an enquiry around a project where certain problems occured.

Features
--------

DPP comes with an **administration interface**, where various high-level information around a
project can be inserted and maintained. Which important *stakeholders* are involved in the project?
What are *important events*? How is the *project structured*? All this information is then presented
as a **front-end website** visible for end-users.

*Notable features of the software are:*

* Extensive admin interface
* Beautifully layouted front-end website
* Tags and external links for all project objects
* Full-text search
* Document manangement with integrated PDF viewer
* Advanced commenting system for end-users
* Languages available: EN/DE

.. image:: images/screenshots/v06/example_project_admin.png

Technology
----------

DPP is build with ``Python/Django`` and comes as a ``Django app`` providing all the data models necessary together 
with the templates for the front end layout. This app can be integrated in a ``Django`` project representing 
the concrete project to be targeted.

.. warning:: This software currently is in ``beta`` status. It can be used in a productive environment,
             but please follow closely the :ref:`release_notes` if you want to make an update of the software
             and have an eye on changes in Django model declarations, software dependencies or config settings. 


.. _installation:

Installation
============

Requirements
------------

For installing DPP you need the following ``Python/Django`` libraries, probably best installed in 
an own ``virtualenv`` environment:

* Python 2.7+ (Python 3.x not yet supported)
* `Django <https://www.djangoproject.com/>`_ 1.8 (1.9+ not yet supported)
* `PDFMiner <http://www.unixuser.org/~euske/python/pdfminer/index.html>`_ (Version 20110515 to avoid dependency errors!)
* Pillow 2.5.2+ (Replacing PIL, for Django ImageField type)
* `Tastypie <http://tastypieapi.org/>`_ 0.12+ (for API access)

For PDF conversion to jpg files for having an IE compatible PDF viewer, you need to have the 
``ImageMagick`` library with the ``convert`` command installed in your shell environment:

* `ImageMagick (convert tool) <http://www.imagemagick.org/>`_

.. note:: There are some fabric tasks which can help you set up an environment for DPP located in
          an own GitHub repository which can be found here: https://github.com/holgerd77/django-public-project-fabric-tasks/

Installation with Pip
---------------------
``DPP`` is on the ``Python Package Index`` and you can install the software with all dependencies
with::

    pip install django-public-project

Manual Installation
-------------------
If you want to have the latest version of ``DPP``, you can install the sources manually 
with ``PIP`` (or directly clone the GitHub repository)::

    pip install -e git+https://github.com/holgerd77/django-public-project.git@master#egg=django-public-project

Then install the requirements above. There is a ``requirements.txt`` file in the main directory
of the repository you can use::

    pip install -r requirements.txt

Project Creation
---------------- 
Create your ``Django`` project::

    django-admin.py startproject myprojectwatch

Add the Django apps installed to your ``settings.py`` file (of course you also need the admin app which
is essential for DPP)::

    INSTALLED_APPS = (
        ...
        'public_project', # Since DPP changes some admin templates, app has to be placed before admin
        'django.contrib.admin',
        'tastypie',
    )

Sync your database respectively use migrations for DPP::

    python manage.py syncdb (due to database dependencies, don't create a superuser yet)
    python manage.py migrate
    python manage.py createsuperuser

Configuration
=============

DPP is not really an app which you would install beside many other Django apps and integrate it in a more
complex website. It is more a content management system already coming with an url structure and a given
layout capsuled in a single app. So DPP takes control of more things than the normal Django app.

URL structure
-------------
The urlpatterns for your project are completely coming from DPP, with an exception of the admin url,
which should be adoptable for security reasons. So your minimal urls.py should look similar to this,
importing the main url patterns from ``public_project.urls``::

    from django.conf import settings
    from django.conf.urls import patterns, include, url
    
    from django.contrib import admin
    admin.autodiscover()
    
    from public_project.urls import urlpatterns
    
    urlpatterns += patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )

    # Necessary for being able to use image upload in DEBUG mode
    if settings.DEBUG:
        urlpatterns += patterns('',
            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT})
        )

Now you should be able to enter both the admin view and an emtpy front-end dashboard site 
when you start a dev server. The site itself is not yet ready for prime time at this moment.

.. image:: images/screenshots/v06/example_project_admin.png


Basic settings
--------------
Since I'm not sure, if there are still some static references to static or media files somewhere in the code,
you should use the following ``STATIC_URL`` and ``MEDIA_URL`` settings::

   MEDIA_URL = '/media/'
   STATIC_URL = '/static/'

For being able to get email notifications about comments and document relations, you need to configure
the Django email settings properly::

    EMAIL_FROM = 'admin@yourmailaccount.com'
    EMAIL_HOST = 'smtp.yoursmtpserver.com'
    EMAIL_HOST_USER =  'YOURUSERNAME'
    EMAIL_HOST_PASSWORD = 'YOURSECUREPASSWORD'
   

DPP uses the request template context processor in its views and adds its own context processors,
add them to the ``settings.py`` file::
   
    from django.conf import global_settings
    ...
    
    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        "django.core.context_processors.request",
        "public_project.context_processors.uploaded_images_list",
    )

Language Selection
------------------
At the moment DPP supports the following languages:

* English (en) (experimental and not yet used in production, probably you have to correct some stuff)
* German (de)

The language is chosen depending on the ``LANGUAGE_CODE`` param in the ``settings.py`` module, e.g.::

    LANGUAGE_CODE = 'de-de'


Document upload/viewer
----------------------

The document viewer in DPP is based on the Mozilla pdf.js library (included in DPP) when using modern
browsers like Google Chrome, Firefox or Safari.

For being able to view on site pdf documents with the Microsoft Internet Explorer there exists a basic 
alternative pdf viewer. For this viewer, single pages are converted to png files and are stored on disk
and you need to have the ``ImageMagick`` library installed and make sure that the ``convert`` command 
from this library can be used from within your project path.

Since this approach can take a lot of disk space for large documents and root access to the server is
needed, you have to activate IE compatible pdf viewer usage with the following setting in your 
``settings.py`` file::

    DPP_IE_COMPATIBLE_PDF_VIEWER = True

If this setting is set to false (default) a warning message will be shown on the document page for IE
users, prompting them to use an alternative browser.

If this setting is set to true, documents are saved as the original pdf file and a corresponding 
document_x folder containing the pngs in your media folder. Please test-upload a pdf document and 
see if these files are generated. Then test the url with the pdf viewer for this document in both 
the MSIE and another browser.

.. note:: The conversion process of a pdf document takes place in the background and may take a while
          for large documents.

.. _custom_js_css:

Custom JS/CSS Code
------------------
If you want to include custom Javascript code or CSS styles into your project - e.g. to add analytics
to the site or customize the layout, you can use the following settings::

  DPP_CUSTOM_JS = 'alert("This should show up on every page!")' #Example JS Code
  
  DPP_CUSTOM_CSS = 'body { margin: 20px; }' #Example CSS Style

Site Domain
-----------
For urls in comment emails to work properly, you have to edit the ``Site`` object, which Django
should have created in the ``Sites`` section in the Django admin.

Provide your fully qualified domain name there (e.g. 'yourproject.yourdomain.com'), without
trailing 'http://'.


JSON API
--------
Since ``v.0.4`` DPP comes with a public API, which let developers access the public data of the
system, leaving out internal comments and user comments. The API supports no authentication mechanism
yet and will be accessible by everyone without limitation. To activate the API, add the following to 
your ``settings.py`` file::

    DPP_PUBLIC_API = True

For the API to work you have got to have `Tastypie <http://tastypieapi.org/>`_ 0.9.15+ installed::

    pip install django-tastypie

And add ``tastypie`` to your ``INSTALLED_APPS``.

When the API is working there will be an extra link in the footer leading to to API overview page::

    http://yourproject.org/api/

.. note:: The API is still in an experimental/early stage, many features are missing and
          usage params will probably change in the future.


Where to go from here?
----------------------
The main set-up process for your project website is now finished and the site is ready to be filled
with some data.

**Congratulations! :-)** 

Start by adding/changing some configuration parameters and introductory texts in the ``SiteConfig``
and ``SiteCategory`` menu.

In the next chapter you will learn how to use the admin interface and how to build up an information
website around your project.

