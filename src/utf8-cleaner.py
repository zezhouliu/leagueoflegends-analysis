import codecs

if __name__ == '__main__':


    BLOCKSIZE = 1048576 # or some other, desired size in bytes

    sourceFiles = ['matches1.json']
    targetFiles = ['m1.json']
    for i in xrange(len(sourceFiles)):
        sourceFileName = sourceFiles[i]
        targetFileName = targetFiles[i]
        with codecs.open(sourceFileName, "r", "iso-8859-1") as sourceFile:
            with codecs.open(targetFileName, "w", "utf-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)