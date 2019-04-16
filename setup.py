"""
Tool to deploy Qt in headless mode.
"""
import setuptools
import cuteci

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=cuteci.__application__,
    version=cuteci.__version__,
    author="Adrien Gavignet",
    author_email="adrien.gavignet@gmail.com",
    license="MIT",
    description="CuteCI is a simple tool allowing you to install Qt with desired packages in headless mode.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="qt deploy install headless docker",
    url="https://github.com/hasboeuf/cuteci",
    packages=setuptools.find_packages(),
    package_data={"cuteci": ["install-qt.qs"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
    entry_points={"console_scripts": ["cuteci=cuteci.deploy_qt:main"]},
)
