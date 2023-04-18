from setuptools import setup, find_packages
import os

setup(
    name='tpl.py',
    version=os.getenv('__VERSION__'),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'template.py=template_py:main',
            'tpl.py=template_py:main'
        ]
    },
    install_requires=[
        'jinja2',
        'cryptography'
    ],
)