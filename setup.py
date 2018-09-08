from setuptools import setup

setup(
    name='pi3-switch',
    version='0.0.1',
    license='MIT',
    author='Michał "landmaj" Wieluński',
    author_email='michal@landmaj.pl',
    install_requires=['i3ipc==1.5.1'],
    entry_points={
        'console_scripts': ['pi3-switch = pi3.switch:main']
    }
)
