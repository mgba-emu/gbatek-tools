from setuptools import setup, find_packages

classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Games/Entertainment",
    "Topic :: Documentation"
]

setup(name="gbatek",
      version="0.1.0",
      author="Vicki Pfau",
      author_email="vi@endrift.com",
      url="http://github.com/mgba-emu/gbatek-tools/",
      packages=find_packages(),
      install_requires=["beautifulsoup4", "Markdown"],
      classifiers=classifiers
      )
