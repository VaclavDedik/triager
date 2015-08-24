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
        'flask-script==2.0.5',
        'croniter==0.3.8',
        'joblib==0.8.4',
        'numpy',
        'pandas'
    ],
)
