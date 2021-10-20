from setuptools import setup

setup(
    name='rss_reader',
    version=f'1.3',
    description='Read rss feed',
    author='PavelBarashkin',
    author_email='pavelb7c8@gmail.com',
    packages=['rss_reader'],
    install_requires=['beautifulsoup4',
                      'requests',
                      'lxml',
                      'dateutil'],
    entry_points={'console_scripts': ['rss_reader=rss_reader.rss_reader:main']}
    )
