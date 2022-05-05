from setuptools import setup

with open("README.md", "r") as fh:

    long_description = fh.read()

setup(name='dataset2database',
      version='1.2',
      description='Script for creating SQL files from video files',
      url='https://github.com/alexandrosstergiou/dataset2database',
      author='Alexandros Stergiou',
      author_email='alexstergiou5@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['dataset2database'],
      install_requires=[
          'numpy',
          'opencv-python',
          'tqdm'
      ],
      zip_safe=False)
