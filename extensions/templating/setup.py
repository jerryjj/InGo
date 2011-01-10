try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='inGo.ext.templating',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    namespace_packages = ['ingo', 'ingo.ext', 'ingo.ext.templating', 'ingo.ext.templating.engines'],
    install_requires=[
        "inGo",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'ingo': ['*.yml']},
    zip_safe=False,
    paster_plugins=['PasteScript', 'inGo'],
    entry_points="""
    """,
)
