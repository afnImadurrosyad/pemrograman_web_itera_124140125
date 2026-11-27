import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    README = f.read()

requires = [
    'plaster_pastedeploy',
    'pyramid>=2.0.2',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_retry',
    'waitress',
    'alembic',
    'pyramid_tm',
    'SQLAlchemy>=2.0.31',
    'zope.sqlalchemy',
    'psycopg2-binary',
    'python-dotenv',
    'marshmallow>=3.19,<4.0',
]

tests_require = [
    'WebTest',
    'pytest',
]

setup(
    name='products_api',
    version='0.0',
    description='REST API Manajemen Kategori dan Produk (Praktikum PAW Pertemuan 7)',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Afnan Imadurrosyad',
    author_email='afnan.124140125@student.itera.ac.id',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = products_api:main',
        ],
        'console_scripts': [
            'initialize_products_api_db = products_api.scripts.initialize_db:main',
        ],
    },
)
