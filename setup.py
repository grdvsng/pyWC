try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Module analog Linux WC utility.',
    'author': 'Sergey Trishkin',
    'url': 'None',
    'download_url': 'None',
    'author_email': 'grdvsng@gmail.com',
    'version': '0.9',
    'install_requires': ['pyWC'],
    'packages': ['wc'],
    'scripts': ['bin\\'],
    'name': 'pyWC',
}

setup(**config)