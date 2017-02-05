from setuptools import setup

setup(name='aqicn',
      packages=['aqicn'],
      version='0.1',
      description='Python SDK for aqicn.org API',
      url='https://github.com/miczal/aqicn-sdk',
      author='miczal',
      author_email='mpierscinski@gmail.com',
      license='MIT',
      install_requires=[
          'requests',
          'pytest',
      ],
      keywords = ['pollution', 'aqicn', 'API', 'SDK'])
