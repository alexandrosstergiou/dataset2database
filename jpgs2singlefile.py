import os
import numpy as np
import glob
import sqlite3
import cv2
import sys
import subprocess
import time
import multiprocessing
import signal
import logging
from concurrent.futures import ProcessPoolExecutor as Pool

def file2sql(video_i):
    logging.info('dataset2database:: -> processing {}'.format(video_i))
    filename_db = os.path.join(video_i,'frames.db')
    con = sqlite3.connect(filename_db, timeout=0.1)
    cur = con.cursor()

    for file_i in glob.glob(video_i+'/*.jpg'):
    	#--- Read image as a binary blob
        with open(file_i, 'rb') as f:
             image_bytes = f.read()
        f.close()

        #--- Decode raw bytes to get image size
        nparr  = np.fromstring(image_bytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image_size = img_np.shape[1]

        #--- Extract file name without extension
        objid = os.path.join(video_i.split('/')[-1],file_i.split('/')[-1].split('.')[0])

        #--- Insert image and data into table
        cur.execute("insert into Images VALUES(?,?)", (objid,sqlite3.Binary(image_bytes)))
        os.remove(file_i)
    con.commit()
    cur.close()
    con.close()


def worker(file_i):
    # Print informational message
    logging.info('dataset2database:: process #{} is converting file: {}'.format(multiprocessing.current_process().name,file_i))
    sys.stdout.flush()

    # Only consider videos
    if '.mp4' not in file_i:
      return

    # Get file without .mp4 extension
    name, ext = os.path.splitext(file_i)
    name = os.path.join(*(name.split(os.path.sep)[1:]))

    # Create destination directory for video
    dst_directory_path = os.path.join(dst_dir, name)

    try:
        # Case that video path already exists
        if os.path.exists(dst_directory_path):
            # Case that frames have already been extracted
            if not os.path.exists(os.path.join(dst_directory_path, 'frame_00001.jpg')):
                subprocess.call('rm -r {}'.format(dst_directory_path), shell=True)
                logging.info('dataset2database:: remove {}'.format(dst_directory_path))
                os.makedirs(dst_directory_path)
            else:
                return
        else:
            os.makedirs(dst_directory_path)
            filename_db = os.path.join(dst_directory_path,'frames.db')
            create_db(filename_db)
    except:
        logging.info('dataset2database:: Exception in {}'.format(dst_directory_path))
        return


    subprocess.call(['ffmpeg', '-i', file_i, '-hide_banner', '-loglevel', 'quiet', '-vf', 'scale=-1:360', '{}/frame_%05d.jpg'.format(dst_directory_path)])





def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)



#--- Simple database creator
def create_db(filename):
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS Images")
    cursor.execute("CREATE TABLE Images(ObjId STRING, frames BLOB)")
    db.commit()
    db.close()


def convert(base_dir,dst_dir):

    start = time.time()

    #--- Extract files from folder following pattern
    files   = glob.glob(base_dir+"*/*.mp4")
    n_files = len(files)
    logging.info('dataset2database:: Number of files in folder: ', n_files)


    for c in os.listdir(base_dir):

        # --- FRAME EXTRACTION IS DONE HERE
        base_files = glob.glob(os.path.join(base_dir,c)+"/*.mp4")
        try:
            with Pool() as p1:
                p1.map(worker, base_files)

        except KeyboardInterrupt:
            logging.warning("dataset2database:: Caught KeyboardInterrupt, terminating")
            p1.terminate()
            p1.join()

        # --- DATABASE POPULATION IS DONE HERE
        dist_files = glob.glob(os.path.join(dst_dir,c)+"/*")
        try:
            with Pool() as p2:
                p2.map(file2sql, dist_files)

        except KeyboardInterrupt:
            logging.warming("dataset2database:: Caught KeyboardInterrupt, terminating")
            p2.terminate()
            p2.join()


    end = time.time()
    logging.info('dataset2database:: Conversion to SQLite database was sucessful in %d secs' %(end-start))
