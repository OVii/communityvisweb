from datetime import datetime
import os

__author__ = 'eamonnmaguire'


def prepareDirectoryAndGenerateFileName():
    BASE_PATH = '/tmp/bibs/'
    try:
        os.mkdir(BASE_PATH)
    except:
        pass
    bibFileSaveLocation = BASE_PATH + 'upload-' + str(datetime.now()) + '.bib'
    return bibFileSaveLocation


def saveFile(bibtex_file):
    bibFileSaveLocation = prepareDirectoryAndGenerateFileName()
    fout = open(bibFileSaveLocation, 'wb+')
    for line in bibtex_file:
        fout.write(line)
    fout.close()

    return bibFileSaveLocation


def saveTextToFile(bibtex_file):
    bibFileSaveLocation = prepareDirectoryAndGenerateFileName()
    fout = open(bibFileSaveLocation, 'wb+')
    fout.write(bibtex_file)
    fout.close()

    return bibFileSaveLocation
