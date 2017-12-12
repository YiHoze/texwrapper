import os, glob

extensions = {"aux", "bbl", "blg", "idx", "ilg", "ind", "lof", "log", "lop", "loq", "lot", "minted*", "mw", "nav", "out", "synctex*", "snm", "toc*", "upa", "upb", "vrb"}

for ext in extensions:
    pattern = '*.' + ext
    for file in glob.glob(pattern):
        os.remove(file)