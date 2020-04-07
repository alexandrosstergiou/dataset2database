# dataset2database

![supported versions](https://img.shields.io/badge/python-2.7%2C%203.5-green.svg)
[![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=dataset2database&video&to&sql&converter&url=https://github.com/alexandrosstergiou/dataset2database&hashtags=VideoConverter)
----------------------
About
----------------------

The package is made as a solution when using video inputs in Machine Learning models. As extracting and storing frames in `.JPEG` files will quickly increase the memory requirements and more importantly the number of `inodes`, the package provides a convenient alternative. Video frames are stored as blobs at database file `.db` which can be read as quickly as the `.JPEG` files but without the additional large memory requirements.

----------------------
Package requirements
----------------------
The two required packages are `opencv` for image/frame loading and `numpy` for array manipulation. Make sure that both are installed before running any functions.

**Multiprocessing:** The code uses multiprocessing for improving speeds, thus the total time required for the conversion varies across different processors. The code has been tested on an AMD Threadripper 2950X with an average conversion time of 48 minutes for ~500K videos.


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

----------------------
Usage
----------------------

The main code is at the `jpgs2single.py` file. To run the convertor simply call the `convert` function with the base directory of the dataset and the destination directory for where to save the generated databases.

```python
from dataset2database import convert
#or
from jpgs2singlefile import convert

convert(my_dataset_dir, my_target_dir)

```

----------------------
Frames.db files
----------------------
Video frames are stored in `frames.db` files with their video name and frame number as their `ObjID` and the frames array are stored as `blobs`. The name format is basically **<_video_name_>/_frame_ _ _[frame number in 5-digit format]_**

![dataset2database](images/dataset2database.gif)

**File viewer:** If you want to ensure that everything has been converted correctly, you can use [_SQLiteStudio_](https://sqlitestudio.pl/index.rvt) which provides an easy to use multi-platform interface (available for Windows, Mac and Ubuntu).

----------------------
Database loading
----------------------
Loading the database can easily be done with an SQL `SELECT` command based on a list of all frames with specified `ObjId`s. Then, with the help of `np.fromstring()` and `cv2.imdecode()` functions the images can be again converted to `uint8` arrays.

An example of data loading in python can be found below:

```python
import sqlite3
import cv2
import numpy as np

con = sqlite3.connect('my_video_database.db')
cur = con.cursor()


# retrieve entire video from database (frames are unordered)
frame_names = ["{}/{}".format(my_path.split('/')[-1],'frame_%05d'%(index+1)) for index in frame_indices]
sql = "SELECT Objid, frames FROM Images WHERE ObjId IN ({seq})".format(seq=','.join(['?']*len(frame_names)))
row = cur.execute(sql,frame_names)

ids = []
frames = []
i = 0

row = row.fetchall()
# Video order re-arangement
for ObjId, item in row:
  #--- Decode blob
  nparr  = np.fromstring(item, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  ids.append(ObjId)
  frames.append(img)
  i+=1

# Ensuring correct order of frames
frames = [frame for _, frame in sorted(zip(ids,frames), key=lambda pair: pair[0])]

# (if required) array conversion [frames x height x width x channels]
frames = np.asarray(frames)

cur.close()
con.close()

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

The latest stable release is also available for download through pip
```
$ pip install dataset2databse
```
