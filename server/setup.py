from setuptools import setup

setup(
    name='server',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'psycopg2',
        'pytest',
        'python-dotenv',
        'shapely',
    ],
)