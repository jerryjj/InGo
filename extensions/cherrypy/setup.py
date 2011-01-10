from setuptools import setup, find_packages

setup(
    #name='fi.infigo.ingo.cherrypy',
    name='inGo.ext.cherrypy',
    version='0.1',
    description='CherryPy extension for Ingo',
    author='Jerry Jalava',
    author_email='jerry.jalava@infigo.fi',
    url='',
    install_requires=[
        "inGo>=0.1",
        "inGo.web>=0.1",
        "CherryPy>=3.1.2"
    ],
    # extras_require = {
    #     'genshi': ['Genshi>=0.4.4'],
    # },
    #test_suite='nose.collector',
    #packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    package_data={
        'ingo': [
            '*.yml',
            'static/*/*'
        ]
    },
    zip_safe=False,
    entry_points="""
    [ingo.features]
    web = ingo.ext.web.cherry:list_features
    """,
)
