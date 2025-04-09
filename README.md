#One-way Folder Synchronization
  ##Introduction
  This script synchronizes the content between two folders, a source and replica respectively(one-way).
  The synchronization is made periodically and every change(copy, update or removal) made to the replica folder is logged (on the console and in a log file)

  ##Usage
  The folder paths, log path and time interval are entered as the following arguments on the CLI:
      -o ORIGINAL, Path to source
      -r REPLICA, Path to replica
      -l LOG, Path to log file
      -t TIME, Time in seconds
    For example:
      python folderSync.py -o (source folder path) -r (replica folder path) -l (log file path) -t (time interval (int))
      
  ##Requirements
  - Python 3.x
  - libraries: os, argparse, hashlib, shutil, logging, time
