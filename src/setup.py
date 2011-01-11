# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='inGo',
    version='0.1',
    description='InGo Framework',
    long_description=''
    classifiers=[
        #"Development Status :: 5 - Production/Stable",
        #"Development Status :: 4 - Beta",
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD Licens",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    license="BSD"
    author='Jerry Jalava',
    author_email='jerry.jalava@infigo.fi',
    url='http://ingo.infigo.fi',
    install_requires=[
        "Paste>=1.7.2", "PasteDeploy>=1.3.3", "PasteScript>=1.7.3",
        "Tempita>=0.2",
        "PyYAML",
        "Unipath",
        "python-gettext"
    ],
    setup_requires=[],
    namespace_packages = ['ingo', 'ingo.ext'],
    packages=find_packages(exclude=['ez_setup']),    
    test_suite='nose.collector',
    #tests_require=['WebTest', 'BeautifulSoup'],
    include_package_data=True,
    package_data={
        'ingo': [
            '*.yml',
            'public/*/*'
        ]
    },
    entry_points="""
    [paste.paster_create_template]
    ingo_extension = ingo.paster.templates:ExtensionTemplate
    """,
)
