try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='InGo.sms.labyrintti',
    version='0.1',
    description='Labyrintti SMS Gateway plugin',
    author='Jerry Jalava',
    author_email='jerry.jalava@infigo.fi',
    url='',
    install_requires=[
        "inGo",
        "inGo.ext.sms",
        "httplib2"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    paster_plugins=['PasteScript', 'inGo'],
    entry_points="""
    [ingo.ext.sms.plugins]
    labyrintti = labyrintti_sms:make
    """,
)