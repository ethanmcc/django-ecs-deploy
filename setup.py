import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ecs-deploy',
    version='0.1.11',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A Django app that provides a command to deploy a Django app '
    'to AWS ECS based on Django settings.',
    long_description=README,
    url='https://github.com/ethanmcc/django-ecs-deploy',
    author='Ethan McCreadie',
    author_email='ethanmcc@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
