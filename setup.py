from setuptools import setup

import os

setup(
    name='django-public-project',
    version='0.6.0',
    description='CMS for building an information website around public projects',
    author='Holger Drewes',
    author_email='Holger.Drewes@googlemail.com',
    url='https://github.com/holgerd77/django-public-project',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    packages=[
        'public_project',
        'public_project.management',
        'public_project.management.commands',
        'public_project.migrations',
        'public_project.templatetags',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.5,<1.6',
        'pdfminer==20110515',
        'Pillow',
        'django-tastypie>=0.9,<1.0',
        'South',
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
