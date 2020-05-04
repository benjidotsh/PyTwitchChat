import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytwitchchat",
    version="0.1.0",
    author="Benjamin Janssens",
    author_email="benji.janssens@gmail.com",
    description="Python package to interact with the chat of a Twitch channel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benjiJanssens/PyTwitchChat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
