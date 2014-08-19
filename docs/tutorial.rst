.. _tutorial:

========
Tutorial
========

The Example Project
===================

There is an **example project "Tower of Babel"** coming with the DPP sources as a ready-configured ``Django project``
containing some test data.

This tutorial is referencing the example project in the different sections. If you want you can take it 
as a basis when starting to learn, add some additional data, edit entries and play around a bit to 
get a feeling for the software. It is also possible though to directly start
entering your own project data or build up an own first example.

For using the example project find the ``example_project`` folder in your DPP installation directory and copy
the folder to your own location.

Go to your folder copy and run the following scripts to init the project::

	./init_example_project.sh
	./create_example_data.sh

.. note:: If you are running Windows and you don't have configured a way to run shell scripts from the 
          command line you have to look at both script files and run the commands manually (if you 
          rewrite these scripts as Windows batch files you are very welcome to make a pull request on
          GitHub!).

You can then start the server with ``./runserver.sh`` and should be able to reach the admin interface
and front-end website via the URLs provided.

.. image:: images/screenshots/v06/example_project_dashboard.png

Website Configuration and Categories
====================================

Before you start giving some structure to your project by providing topics and entering information
about the different stakeholders and important events, you probably want to start with some general 
set-up of your site.

.. image:: images/screenshots/v06/example_project_admin.png

Website Configuration
---------------------
In the "Website Configuration" menu in your project admin you can enter a title for your project,
a short intro text for the main page and some other generic texts like contact information for the 
"Contact" page or a short footer text.

.. image:: images/screenshots/v06/admin_website_configuration_form.png

Enter/edit some text and have a look, how your text is formatted at the front-end website.

Side Quest: Adding Images
-------------------------
All longer description fields in the admin come with a simple WYSIWYG editor providing some basic formatting
options like text formatting or text alignment. It is also possible to adding an image to your
description.

For using an image in a description field you have to first upload it by going to the **"Images" menu** from
the admin overview page and then add a new image. Upload the image, give it a meaningful title and
provide attribution information if you took the image from an external source (this will be displayed
publicly on the website).




