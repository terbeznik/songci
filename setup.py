import setuptools


with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="songci",
    version="0.0.6",
    author="Alexander Terbeznik",
    author_email="alexander.terbeznik@gmail.com",
    description="songci checks proxies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/terbeznik/songci",
    packages=["songci"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "tqdm",
        "beautifulsoup4",
        "colorama"
    ],
    entry_points={
        'console_scripts': [
            'songci = songci.__main__:main',
        ]
    }
)
