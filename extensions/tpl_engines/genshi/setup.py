try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='inGo.ext.templating.genshi',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "inGo",
        "inGo.ext.templating"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    paster_plugins=['PasteScript', 'inGo'],
    entry_points="""
    [ingo.features]
    templating = ingo.ext.templating.engine:list_features
    """,
)
