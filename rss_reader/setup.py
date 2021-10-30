from setuptools import setup

setup(
    name='rss_reader',
    version=f'1.4',
    description='Read rss feed',
    author='PavelBarashkin',
    author_email='pavelb7c8@gmail.com',
    packages=['rss_reader'],
    package_data={
        "": ["rss_reader/fonts/*"]
                },
    install_requires=['beautifulsoup4==4.10.0',
                      'requests==2.26.0',
                      'lxml==4.6.3',
                      'python-dateutil==2.8.2',
                      'xhtml2pdf==0.2.5'],
    entry_points={'console_scripts': ['rss_reader=rss_reader.rss_reader:main']}
    )
