from setuptools import setup, find_packages


setup(
    name="classifier",
    version="0.1",
    description="Text classification library.",
    url="https://github.com/VaclavDedik/masters-thesis/classifier",
    keywords="classifier machine_learning text",
    license="MIT",

    author="Vaclav Dedik",
    author_email="vaclav.dedik@gmail.com",

    packages=find_packages(),
    install_requires=[
        'numpy',
        'nltk',
        'scipy',
        'scikit-learn'
    ],
)
