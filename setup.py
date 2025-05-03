from setuptools import setup, find_packages

setup(
    name="capydetect",
    version="1.0",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    python_requires='>=3.8',
    author="Podshivalov Andrew Sokolov Aleksei",
    description="Капибара детектор",
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'Parcer_CAPY'),
            'version': ('setup.py', '1.0.0'),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
        }
    },

)