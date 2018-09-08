from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pi3-switch',
    description='This simple program will switch to the given i3 workspace '
                'with slightly different behavior if there are two outputs.',
    long_description=long_description,
    version='0.3.1',
    license='MIT',
    author='Michał Wieluński',
    author_email='michal@landmaj.pl',
    url='https://gitlab.com/landmaj/pi3-switch',
    install_requires=[
        'i3ipc==1.5.1',
        'pynput==1.4',
    ],
    packages=['pi3'],
    zip_safe=True,
    entry_points={
        'console_scripts': ['pi3-switch = pi3.switch:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Window Managers',
      ],
)
