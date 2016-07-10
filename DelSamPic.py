# coding=utf-8

from hashlib import md5

import os
import sys


class DelSamFiles(object):
    # blockSize = 64 * 1024
    dirPath = os.path.join(os.getcwd(), sys.argv[-1])
    fileNamesList = []

    def checkCommand(self):
        if len(sys.argv) == 3:
            return True
        else:
            print 'Command error!'
            print 'Example: C:\>python DelSamPic.py ./Dir1'
            return False

    '''
    md5 file with filename (MD5)
    '''
    def getFileMD5(self, fileName):
        getMD5 = md5()
        thisFile = open(os.path.join(self.dirPath, fileName), 'rb')
        getMD5.update(thisFile.read())
        thisFile.close()
        return getMD5.hexdigest()

    def makeFilesIDArray(self):
        array = {}
        for self.dirPath, dirName, self.fileNamesList in os.walk(self.dirPath):
            for fileName in self.fileNamesList:
                array[fileName] = self.getFileMD5(fileName)
        return array

    def delSameFiles(self):
        files_array = self.makeFilesIDArray()
        for fileKey in files_array:
            for fileNextKey in files_array:
                if files_array[fileNextKey] != 0 and fileKey != fileNextKey \
                        and files_array[fileKey] == files_array[fileNextKey]:
                    files_array[fileNextKey] = 0
                    try:
                        os.remove(os.path.join(self.dirPath, fileNextKey))
                    except WindowsError:
                        pass


if __name__ == '__main__':
    DSF = DelSamFiles()
    if not DSF.checkCommand():
        sys.exit(0)
    DSF.delSameFiles()
    print("Finish.")
