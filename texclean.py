import os, glob

extensions = {"aux", "bbl", "blg", "idx", "ilg", "ind", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "vrb"}

for ext in extensions:
    fnpattern = '*.' + ext
    for afile in glob.glob(fnpattern):
        os.remove(afile)