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

Next Section (coming...)
========================

This is some text. 