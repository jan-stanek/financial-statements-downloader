from setuptools import setup

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='financial-statements-downloader',
    version='0.1.1',
    keywords='czech republic financial statements business register',
    description='Simple application for downloading financial statements from czech business register.',
    long_description=long_description,
    author='Jan Staněk',
    author_email='stanej16@fit.cvut.cz',
    license='MIT',
    url='https://github.com/jan-stanek/financial-statements-downloader',
    zip_safe=False,
    packages=['financial_statements_downloader'],
    entry_points={
        'console_scripts': [
            'financial_statements_downloader = financial_statements_downloader:main',
        ]
    },
    install_requires=[
        'click',
        'tika',
        'tinydb',
        'beautifulsoup4',
        'html5lib'
    ],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
