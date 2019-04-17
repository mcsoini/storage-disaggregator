import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StoreDisagg",
    version="0.1",
    author="StoreDisagg contributors listed in AUTHORS",
    author_email="soini@posteo.de",
    description="Ex-post energy storage operation disaggregation by time scales.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcsoini/storedisagg,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD 2-Clause License",
        "Operating System :: OS Independent",
    ],
)
