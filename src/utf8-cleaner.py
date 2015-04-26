import codecs

sourceFileName = "matches1.json"
targetFileName = "matches_1.json"

BLOCKSIZE = 1048576 # or some other, desired size in bytes
with codecs.open(sourceFileName, "r", "iso-8859-1") as sourceFile:
    with codecs.open(targetFileName, "w", "utf-8") as targetFile:
        while True:
            contents = sourceFile.read(BLOCKSIZE)
            if not contents:
                break
            targetFile.write(contents)