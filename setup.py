"""
Setup file for CMUJ Wiki MkDocs plugins
"""

from setuptools import setup, find_packages

setup(
    name='cmuj-wiki-plugins',
    version='1.0.0',
    description='Custom MkDocs plugins for CMUJ Wiki',
    author='CMUJ Wiki Team',
    packages=find_packages(where='plugins'),
    package_dir={'': 'plugins'},
    install_requires=[
        'mkdocs>=1.4.0',
    ],
    entry_points={
        'mkdocs.plugins': [
            'quiz_builder = quiz_builder:QuizBuilderPlugin',
        ]
    },
    python_requires='>=3.8',
)
