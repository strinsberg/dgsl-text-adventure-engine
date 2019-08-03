from setuptools import setup

setup(
    name='dgsl_engine',
    version='0.2.0',
    packages=['dgsl_engine'],
    python_requires='>=3',
    entry_points={
        'console_scripts': ['dgsl=dgsl_engine.__main__:main']
    },
    data_files=[
        ('dgsl', []),
        ('dgsl/worlds', ['worlds/disaster_on_the_good_ship_lethbridge.world']),
        ('dgsl/saves', [])
    ]
)
