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
        # main dependencies
        'classifier',
        'Flask',
        'Jinja2',
        # supporting dependencies
        'numpy',
        'pandas'
    ],
)
