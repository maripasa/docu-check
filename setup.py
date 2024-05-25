import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='docucheck',
    version="0.0.1",
    author="Ásafe Duarte",
    author_email="asafexi@proton.me",
    description=(
        'docucheck is a command line tool that has the purpose to'
        'automate the verification of documents related to Brazilian'
        'companies using their CNPJ '
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maripasa/DocuCheck",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'rich',
        'selenium',
        'webdriver_manager',
    ],
    entry_points={
        'console_scripts': [
            'docucheck = docucheck.__main__:main'
        ]
    },
)
