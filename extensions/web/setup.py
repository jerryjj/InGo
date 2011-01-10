from setuptools import setup, find_packages

setup(
    name='inGo.web',
    version='0.1',
    description='Web extension for Ingo',
    author='Jerry Jalava',
    author_email='jerry.jalava@infigo.fi',
    url='',
    namespace_packages = ['ingo', 'ingo.web', 'ingo.ext', 'ingo.ext.web'],
    install_requires=[
        "inGo>=0.1",
        "Routes>=1.12"
    ],
    test_suite='nose.collector',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={
        'ingo': [
            '*.yml',
        ]
    },
    zip_safe=False,
    entry_points="""
    [ingo.features]
    web = ingo.web:list_features
    """,
)
