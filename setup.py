from setuptools import setup, find_packages

try:
    with open("requirements/base.txt") as f:
        required = [l.strip('\n') for l in f if
                    l.strip('\n') and not l.startswith('#')]
except IOError:
    required = []

setup(
    name="config42",
    packages=find_packages(),
    version='0.1',
    license='GPLv3+',
    description="Configuration manager for cloud native application, support configuration stored"
                " in memory, in files, in databases",
    author="Amine Ben Asker",
    author_email="ben.asker.amine@gmail.com",
    url="https://github.com/yurilaaziz/config42",
    download_url='https://github.com/yurilaaziz/config42/releases/tag/0.1',
    keywords="Pretty configuration manager, Key value data store, cloud native configuration",
    install_requires=required,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
