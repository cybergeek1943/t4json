from setuptools import setup

with open('README.md', 'r') as rm:
    long_description: str = rm.read()

setup(
    name='t4json',
    packages=['t4json'],
    version='v1.0.1',
    license='MIT',
    description='Tools to work with JSON data easily and quickly.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Isaac Wolford',
    author_email='cybergeek.1943@gmail.com',
    url='https://github.com/cybergeek1943/t4json',
    download_url='https://github.com/cybergeek1943/t4json/archive/refs/tags/v1.0.1.tar.gz',
    keywords=['json', 'tool', 'tools', 'data', 'structures', 'flattening', 't4json', 'flatten', 'nested'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
)
