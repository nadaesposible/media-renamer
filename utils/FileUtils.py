from fnmatch import filter
from os.path import isfile
from os.path import join
from os.path import exists
from os.path import dirname
from os import walk
from os import makedirs
from shutil import copyfile
from shutil import move

class FileUtils:

    @staticmethod
    def findFilesRecursivelly(sourcePath, extensions, maxNumberOfFiles):
        matches = []
        for root, dirnames, filenames in walk(sourcePath):
            for filename in filenames:
                if filename.lower().endswith(extensions):
                    matches.append(join(root, filename))
                    if len(matches) >= maxNumberOfFiles:
                        return matches
        return matches

    @staticmethod
    def cp(media, destinationPath):
        destinationFile = FileUtils.__getDestinationFilename(destinationPath, media)
        FileUtils.__createDestinationDirectory(destinationFile)
        copyfile(media.sourceFile, destinationFile)

    @staticmethod
    def mv(media, destinationPath):
        destinationFile = FileUtils.__getDestinationFilename(destinationPath, media)
        FileUtils.__createDestinationDirectory(destinationFile)
        move(media.sourceFile, destinationFile)

    @staticmethod
    def __getDestinationFilename(destinationPath, media):
        fullDestinationPath = join(destinationPath, FileUtils.__getDestinationSubdirectory(media))
        destinationFile = join(fullDestinationPath, media.getNextNewFileName())
        while isfile(destinationFile):
            destinationFile = join(fullDestinationPath, media.getNextNewFileName())
        return destinationFile

    @staticmethod
    def __getDestinationSubdirectory(media):
        subdir = media.getCreateYear()
        if media.isPicture():
            return join('Pictures', subdir)
        elif media.isVideo():
            return join('Videos', subdir)
        else:
            return join('Unknown', subdir)

    @staticmethod
    def __createDestinationDirectory(filename):
        if not exists(dirname(filename)):
            try:
                makedirs(dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise