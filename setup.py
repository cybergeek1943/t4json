from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as rm:
    long_description: str = rm.read()

setup(
    name='t4json',
    packages=['t4json'],
    version='v1.3.3',
    license='MIT',
    install_requires=['requests'],
    description='Tools to work with JSON data easily and quickly.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Isaac Wolford',
    author_email='cybergeek.1943@gmail.com',
    url='https://cybergeek1943.github.io/t4json/',
    download_url='https://github.com/cybergeek1943/t4json/archive/refs/tags/v1.3.3.tar.gz',
    keywords=['json', 'tool', 'tools', 'data', 'structures', 'flattening', 't4json', 'flatten', 'nested'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
