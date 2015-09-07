from setuptools import setup, find_packages


setup(
    name="triager",
    version="0.1",
    description="Triager Webapp.",
    url="https://github.com/VaclavDedik/triager",
    keywords="triage machine_learning bug webapp",
    license="MIT",

    author="Vaclav Dedik",
    author_email="vaclav.dedik@gmail.com",

    packages=find_packages(),
    install_requires=[
        'classifier>=0.1',
        'Flask>=0.10.1',
        'Jinja2>=2.7.2',
        'sqlalchemy>=1.0.8',
        'flask-sqlalchemy>=2.0',
        'flask-wtf>=0.12.0',
        'flask-script>=2.0.5',
        'flask-login>=0.2.11',
        'croniter>=0.3.8',
        'joblib>=0.8.4',
        'requests>=2.7.0',
        'numpy>=1.8.0rc1',
        'pandas>=0.15.0'
    ],
    dependency_links=[
        'http://github.com/VaclavDedik/classifier/tarball/master#egg=classifier-0.1'
    ]
)
