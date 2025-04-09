#! usr/bin/env python3
import os
import argparse
import hashlib
import shutil
import logging
import time

def syncFolders(original, replica, log, timeInterval):
    if not os.path.isdir(replica):
        print(f"{replica} filepath does not exist. Please make sure the files you're synchronizing exist.")
        raise SystemExit
    
    if not os.path.isdir(original):
        print(f"{original} filepath does not exist. Please make sure the files you're synchronizing exist.")
        raise SystemExit

    while True:
        try:  
            checkFolders(original, replica)
            time.sleep(timeInterval)
        except KeyboardInterrupt:
            print('Script interrupted.')
            raise SystemExit
    

#Compares the checksums the file content in md5
def checksumFileContent(oF, rF):
    with open(oF, 'rb') as fileO, open(rF, 'rb') as fileR:
        return hashlib.md5(fileO.read()).hexdigest() == hashlib.md5(fileR.read()).hexdigest()
           

#Compares the files on the folders and removes any file that is not on the Original folder
def checkFolders(originalFolder, replicaFolder):
    filesOriginal = os.listdir(originalFolder)
    filesReplica = os.listdir(replicaFolder)

    #Compares the file list of both folders and deletes extra files on the replica folder
    filesToDelete = set(filesReplica) - set(filesOriginal)
    for file in filesToDelete:
        os.remove(os.path.join(replicaFolder, file))
        log = f'REMOVED file: {file}'
        logging.info(log)
        print(log)
    

    #Iterates each file in the original and checks if its present on the replica folder and copies or updates it accordingly
    #Additionaly, I did this with logging confirmed files in mind
    #(to test, uncomment the try/except block and syncedFiles[]list
    #And enable the exception on the checksum condition and also down below)
    #
    #syncedFiles = []
    for file in filesOriginal:
        originalFile = os.path.join(originalFolder, file)
        replicaFile = os.path.join(replicaFolder, file)
        
        #try:
        if file in filesReplica:
            if checksumFileContent(originalFile, replicaFile):
                #raise Exception
                continue
            else:
                os.remove(replicaFile)
                shutil.copy(originalFile, replicaFile)
                log = f'UPDATED file: {file}'
        else:
            shutil.copy(originalFile, replicaFile)
            log = f'COPIED file: {file}'
        logging.info(log)
        print(log)
        '''
        except:
            syncedFiles.append(file)

    print(f'Files that were already up to date:{syncedFiles}')
    '''
    print('All files are synchronized.')    
if __name__ == '__main__':                

    parser = argparse.ArgumentParser('Check sync')
    parser.add_argument('-o','--original', required=True, help='Path to source')
    parser.add_argument('-r','--replica', required=True, help='Path to replica')
    parser.add_argument('-l','--log', required=True, help='Path to log file')
    parser.add_argument('-t','--time', required=True, help='Time in seconds', type=int)
    args = parser.parse_args()
    
    originalPath = args.original
    replicaPath = args.replica
    logPath = args.log
    timeInterval = args.time

    
    logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', level=logging.INFO, filename=f'{logPath}'+ 'logs.txt')
    syncFolders(originalPath, replicaPath, logPath, timeInterval)