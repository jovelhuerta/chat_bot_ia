from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages

setup(
    name='oberyn-gateway',
    version='0.0.1',
    packages= find_packages('src'),
    package_dir={'':'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=[
        "setuptools==70.0.0",
        "groq",
        "pyTelegramBotAPI",
        "pymongo",
        "langchain-ollama",
        "ollama",
        "langchain-groq",
        "langchain-core"
    ],
    zip_safe=True,
)