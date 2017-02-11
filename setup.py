from setuptools import setup
 
import os

setup(
    name='django-public-project',
    version='0.7.2',
    description='Custom CMS for making public projects, political processes or enquiry commission work more transparent',
    author='Holger Drewes',
    author_email='Holger.Drewes@gmail.com',
    url='https://github.com/holgerd77/django-public-project',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    packages=[
        'public_project',
        'public_project.management',
        'public_project.management.commands',
        'public_project.migrations',
        'public_project.templatetags',
        'public_project.utils',
        'example_project',
        'example_project.ep_setup_app',
        'example_project.ep_setup_app.management',
        'example_project.ep_setup_app.management.commands',
        'example_project.example_project',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.8,<1.9',
        'pdfminer==20110515',
        'Pillow',
        'django-tastypie>=0.12,<1.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
)
