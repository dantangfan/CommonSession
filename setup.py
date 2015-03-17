from setuptools import setup, find_packages

setup(
    name="CommonSession",
    description="Use or extend this module to add session for your web app",
    version="0.10",
    author="Dantangfan",
    author_email="dantangfan@gmail.com",
    url="github.com/dantangfan/CommonSession",
    license="LGPL",
    packages=find_packages(),
    install_requires=[
        'redis',
    ]
)