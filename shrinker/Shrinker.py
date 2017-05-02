import sys
sys.path.append('../config')
sys.path.append('../log')
sys.path.append('../entities')
sys.path.append('../utils')
from config.Config import Config
from log.Logging import logging
from entities.Media import Media
from utils.FileUtils import FileUtils
from glob import glob

class Shrinker:

    def __init__(self, sourcePath):
        self.numberOfErrors = 0
        self.sourcePath = sourcePath
        self.destinationPath = Config.get('shrinker.path.destination')

    def run(self):
        for file in self.__getFilenamesToShrink():
            try:
                self.__shrink(file)
            except:
                self.__handleError(file)

    def __getFilenamesToShrink(self):
        extensions = tuple(Config.get('shrinker.path.sources.file.extensions').split(','))
        return FileUtils.findFilesRecursivelly(self.sourcePath, extensions, Config.get('shrinker.max.number.of.files'))

    def __shrink(self, file):
        media = Media(file)
        if media.isVideo():
            print('shrinking video ' + file)
        elif media.isPicture():
            print('shrinking picture:\nFrom: ' + file + '\nTo  : ' + self.destinationPath + '(' + media.getNextNewFileName() + ')')
        else:
            print('shrinking unknown format' + file)

    def __handleError(self, file):
        self.numberOfErrors = self.numberOfErrors + 1
        logging.error('Error shrinking %s. Error number %s.', str(file), str(self.numberOfErrors), exc_info=True)
        if self.numberOfErrors == int(Config.get('shrinker.max.number.of.errors')):
            raise ValueError('Too many errors. Something is wrong. Aborting execution.')