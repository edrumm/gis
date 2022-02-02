from setuptools import setup
import os

# Path to GDAL wheel
# gdal_path = os.path.join('file://localhost/', os.getcwd(), 'GDAL-3.4.1-cp38-cp38-win_amd64.whl')

# fiona_path = os.path.join('file://localhost/', os.getcwd(), 'Fiona-1.8.20-cp38-cp38-win_amd64.whl')

setup(
    name='server',
    packages=['server'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors',
        'geojson',
        'pillow',
        'psycopg2',
        'pyshp',
        'pytest',
        'python-dev-tools',
        'python-dotenv',
        'shapely',
    ],
)