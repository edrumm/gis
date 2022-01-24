from setuptools import setup
import os

# not working
path = os.path.join('file://localhost/', os.getcwd(), 'GDAL-3.4.1-cp38-cp38-win_amd64.whl')

setup(
    name='server',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'gdal',
        'geojson',
        'psycopg2',
        'pyshp',
        'pytest',
        'python-dotenv',
        'shapely',
    ],
    dependency_links=[
        path,
    ],
)