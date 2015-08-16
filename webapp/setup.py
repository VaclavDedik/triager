from setuptools import setup, find_packages


setup(
    name="triager",
    version="0.1",
    description="Triager Webapp.",
    url="https://github.com/VaclavDedik/masters-thesis/webapp",
    keywords="triage machine_learning bug webapp",
    license="MIT",

    author="Vaclav Dedik",
    author_email="vaclav.dedik@gmail.com",

    packages=find_packages(),
    install_requires=[
        'classifier',
        'Flask',
        'Jinja2',
        'sqlalchemy==1.0.8',
        'flask-sqlalchemy==2.0',
        'flask-wtf==0.12.0',
        'rq==0.5.4',
        'joblib==0.8.4',
        'numpy',
        'pandas'
    ],
)
