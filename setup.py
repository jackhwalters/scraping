try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='scraping',
    version='1.0',
    description='Python CLI and browser interface for scraping and ranking text off websites',
    author='Jack Walters',
    author_email='jackwalterswork@gmail.com',
    packages=['src'],
    install_requires=['nose==1.3.7', 'beautifulsoup4==4.9.1', 'requests==2.24.0', 'Flask==1.1.2',
        'bs4==0.0.1', 'certifi==2020.6.20', 'chardet==3.0.4' , 'click==7.1.2', 'idna==2.10', 
        'itsdangerous==1.1.0', 'Jinja2==2.11.2', 'lxml==4.3.0', 'MarkupSafe==1.1.1', 'python-docx==0.8.7', 
        'soupsieve==2.0.1', 'urllib3==1.25.10', 'Werkzeug==1.0.1']
    )
