import codecs

if __name__ == '__main__':

    BLOCKSIZE = 1048576 # or some other, desired size in bytes

    dataDirectoryPrefix = 'data/'

    sourceFiles = ['matches1.json', 'matches2.json', 'matches3.json', 'matches4.json', 'matches5.json',
        'matches6.json']
    targetFiles = ['m1.json', 'm2.json', 'm3.json', 'm4.json', 'm5.json', 'm6.json']
    for i in xrange(len(sourceFiles)):
        sourceFileName = sourceFiles[i]
        targetFileName = targetFiles[i]
        with codecs.open(dataDirectoryPrefix + sourceFileName, "r", "iso-8859-1") as sourceFile:
            with codecs.open(dataDirectoryPrefix + targetFileName, "w", "utf-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)
