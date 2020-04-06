# dataset2database
----------------------
About
----------------------

The package is made as a solution when using video inputs in Machine Learning models. As extracting and storing frames in `.JPEG` files will quickly increase the memory requirements and more importantly the number of `inodes`, the package provides a convenient alternative. Video frames are stored as blobs at database file `.db` which can be read as quickly as the `.JPEG` files but without the additional large memory requirements.

----------------------
Dataset structure
----------------------

The package assumes a fixed dataset structure such as:

```
<dataset>    
  │
  └──<class 1>
  │     │
  │     │─── <video_data_1.mp4>
  │     │─── <video_data_2.mp4>
  │     │─── ...
  │    ...      
  │
  └───<class 2>
  │      │
  │      │─── <video_data_1.mp4>
  │      │─── <video_data_2.mp4>
  │      │─── ...
 ...    ...

```

-------------------------
Installation through git
-------------------------

Please make sure, Git is installed in your machine:
```
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/alexandrosstergiou/dataset2database.git
```


-------------------------
Installation through pip
-------------------------

You can install the latest stable python version from PyPI
```
$ pip install dataset2database
```
