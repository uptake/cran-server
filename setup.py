import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='cranserver',
    version='1.0.0',
    url='http://github.com/UptakeOpenSource/cran-server',
    license='MIT',
    maintainer='Troy de Freitas',
    maintainer_email='troy.defretas@uptake.com',
    description='An application for serving CRAN packages in a cloud environment.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
