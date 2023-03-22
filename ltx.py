import os
import sys
import glob
import argparse
import configparser
import re
import shutil
# companion of ltx.py
from op import FileOpener

# LC = LatexCompiler('foo', ['-v', ...])
# LC.compile(clear=True, ...)

class LatexCompiler(object):

    def __init__(self, tex=None, argv=None):

        self.xindex_bool = False
        self.texindy_bool = False
        self.komkindex_bool = False
        self.options = {
            'xetex': False,
            'luatex': False,
            # 'alternative': False,
            'batch': False,
            'shell': False,
            'twice': False,
            'fully': False,
            'view': False,
            'compile': True,
            'index': False,
            'index_option': 'korean',
            'keep_aux': False,
            'bookmark_index': False,
            'bookmark_python': False,
            'clear': False,
            'bibtex': False,
            'python': False
        }

        self.tex = tex
        self.parse_args(argv)

        dirCalled = os.path.dirname(__file__)
        ini = os.path.join(dirCalled, 'docenv.conf')
        if os.path.exists(ini):
            config = configparser.ConfigParser()
            config.read(ini)
            self.compiler = config.get('LaTeX', 'compiler', fallback='xelatex.exe')
            # self.alternative_path = config.get('LaTeX', 'alternative_path', fallback=None)
        else:
            self.compiler = "xelatex.exe"


    def parse_args(self, argv=None) -> None:

    #     example = '''examples:
    # ltx.py -b -s foo.xxx
    #     Any filename extension is ignored.
    #     foo.tex is compiled in batch mode and shell commands are allowed during compilation.
    # ltx.py -L foo
    #     lualatex is used instead of xelatex.
    # ltx.py -w -i foo
    #     foo.tex is compiled twice and index entries (foo.idx) are sorted by xindex in between.
    # ltx.py -i -I french -n foo
    #     foo.idx is sorted by French without compilation.
    # ltx.py -i -I foo.ist foo
    #     foo.idx is sorted by komkindex with foo.ist after a compilation.
    # ltx.py -i -m foo
    #     foo.ind is altered so that index entries are added as bookmarks.
    #     Use "-M" to bookmark ones from python docstrings.
    # ltx.py -f -a foo
    #     If foo.idx exists, foo.tex is compiled four times and foo.idx is sorted in between.
    #     Otherwise, it is compiled three times.
    #     Without "-a", every auxiliary file is deleted after compilation is completed.
    # ltx.py -B foo
    #     Bibtex runs after a compilation.
    # ltx.py -p foo
    #     Pythontex runs after a compilation.
    # ltx.py -c
    #     Auxiliary files are cleared.
    # '''

        # parser = argparse.ArgumentParser(
        #     epilog = example,
        #     formatter_class = argparse.RawDescriptionHelpFormatter,
        #     description = 'Let LuaLaTeX or XeLaTeX generate a PDF file from a TeX file.'
        # )
        parser = argparse.ArgumentParser(
            description = "Let LuaLaTeX or XeLaTeX compile TeX files to generate PDF files."

        )
        parser.add_argument(
            'tex',
            type = str,
            nargs = '?',
            help = 'Specify a TeX file.'
        )
        parser.add_argument(
            '-L',
            dest = 'luatex',
            action = 'store_true',
            default = False,
            help = 'Use LuaLaTeX.'
        )
        parser.add_argument(
            '-X',
            dest = 'xetex',
            action = 'store_true',
            default = False,
            help = 'Use XeLaTeX.'
        )
        # parser.add_argument(
        #     '-A',
        #     dest = 'alternative',
        #     action = 'store_true',
        #     default = False,
        #     help = 'Use compilers in the directory set to the alternative_path option in docenv.conf'
        # )
        parser.add_argument(
            '-b',
            dest = 'batch',
            action = 'store_true',
            default = False,
            help = 'Do not halt even with syntax errors. (batch-mode)'
        )
        parser.add_argument(
            '-s',
            dest = 'shell',
            action = 'store_true',
            default = False,
            help = 'Allow an external program to run during a XeLaTeX run. (shell-escape)'
        )
        parser.add_argument(
            '-w',
            dest = 'twice',
            action = 'store_true',
            default = False,
            help = 'Compile twice.'
        )
        parser.add_argument(
            '-f',
            dest = 'fully',
            action = 'store_true',
            default = False,
            help = 'Compile fully.'
        )
        parser.add_argument(
            '-v',
            dest = 'view',
            action = 'store_true',
            default = False,
            help = 'Open the resulting PDF file to view.'
        )
        parser.add_argument(
            '-n',
            dest = 'compile',
            action = 'store_false',
            default = True,
            help = 'Pass over compilation but do other processes such as index sorting.'
        )
        parser.add_argument(
            '-i',
            dest = 'index',
            action = 'store_true',
            default = False,
            help = 'Sort index using xindex, texindy or komkindex.'
        )
        parser.add_argument(
            '-I',
            dest = 'index_option',
            default = 'korean',
            help = 'Specify a language to sort index entries. For example, \"german\" or \"ger\" for German. The default is \"korean\". An index style file, .ist or .xdy, is also acceptable.'
        )
        parser.add_argument(
            '-a',
            dest = 'keep_aux',
            action = 'store_true',
            default = False,
            help = 'Keep auxiliary files after a full compilation. Without this option, they are altogether deleted.'
        )
        parser.add_argument(
            '-m',
            dest = 'bookmark_index',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries. This option is available only with -f or -i options. This feature does not support komkindex.'
        )
        parser.add_argument(
            '-M',
            dest = 'bookmark_python',
            action = 'store_true',
            default = False,
            help = 'Bookmark index entries which are python functions extracted from docstrings. This option is available only with -f or -i options.'
        )
        parser.add_argument(
            '-c',
            dest = 'clear',
            action = 'store_true',
            default = False,
            help = 'Remove auxiliary files after compilation.'
        )
        parser.add_argument(
            '-B',
            dest = 'bibtex',
            action = 'store_true',
            default = False,
            help = 'Run bibtex.'
        )
        parser.add_argument(
            '-P',
            dest = 'python',
            action = 'store_true',
            default = False,
            help = 'Run pythontex.exe.'
        )

        args = parser.parse_args(argv)
        if args.tex:
            self.tex = args.tex
        self.pass_args(
            luatex = args.luatex,
            xetex = args.xetex,
            # alternative = args.alternative,
            batch = args.batch,
            shell = args.shell,
            twice = args.twice,
            fully = args.fully,
            view = args.view,
            compile = args.compile,
            index = args.index,
            index_option = args.index_option,
            keep_aux = args.keep_aux,
            bookmark_index = args.bookmark_index,
            bookmark_python = args.bookmark_python,
            clear = args.clear,
            bibtex = args.bibtex,
            python = args.python)


    def pass_args(self, **options) -> None:

        self.reconfigure(options)


    def reconfigure(self, options) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)


    def get_ready(self) -> None:

        if self.options['luatex']:
            self.compiler = 'lualatex.exe'
        if self.options['xetex']:
            self.compiler = 'xelatex.exe'
        # if self.options['alternative'] and self.alternative_path is not None:
        #     self.compiler = os.path.join(self.alternative_path, self.compiler).replace('/','\\')
        #     print(self.compiler)


        # Compile mode
        if 'xelatex' in  self.compiler.lower():
            if self.options['batch'] or self.options['fully']:
                self.compile_mode = '-interaction=batchmode '
            else:
                self.compile_mode = '-synctex=-1 '
            if self.options['shell']:
                self.compile_mode +=  '-shell-escape -8bit'
        else:
            if self.options['batch'] or self.options['fully']:
                self.compile_mode = '--interaction=batchmode '
            else:
                self.compile_mode = '--synctex=-1 '
            if self.options['shell']:
                self.compile_mode +=  '--shell-escape'

        # language by which to sort index
        xindex_languages = {
            'cze': '-c hz -l cs',
            'dan': '-c hz -l da',
            'eng': '-c hz -l en',
            'fre': '-c hz -l fr',
            'ger': '-c hz -l de',
            'ita': '-c hz -l it',
            'jap': '-c hz -l jp',
            'kor': '-c hz-ko -l ko',
            'nor': '-c hz -l no'
        }
        xindy_modules = {
            'rus': '-M lang/russian/utf8-lang',
            'spa': '-M lang/spanish/modern-utf8-lang'
        }
        if os.path.splitext(self.options['index_option'])[1] == '.xdy':
            self.index_style = '-M {}'.format(self.options['index_option'])
            self.texindy_bool = True
        elif os.path.splitext(self.options['index_option'])[1] == '.ist':
            self.index_style = '-s {}'.format(self.options['index_option'])
            self.komkindex_bool = True
        else:
            key = self.options['index_option'][:3].lower()
            if key in xindex_languages.keys():
                self.index_style = xindex_languages[key]
                self.xindex_bool = True
            elif key in xindy_modules.keys():
                self.index_style = xindy_modules[key]
                self.texindy_bool = True
            else:
                self.index_style = xindex_languages['eng']
                self.xindex_bool = True

        if self.tex is not None:
            basename = os.path.basename(self.tex)
            filename = os.path.splitext(basename)[0]
            self.tex = filename + '.tex'
            self.aux = filename + '.aux'
            self.idx = filename + '.idx'
            self.ind = filename + '.ind'
            self.pdf = filename + '.pdf'
            self.py = filename + '.pytxcode'
            if not os.path.exists(self.tex):
                print('{} is not found.'.format(self.tex))
                self.tex = None


    def compile_once(self, cmd_tex) -> None:

        os.system(cmd_tex)
        if self.options['bibtex']:
            self.run_bibtex()
        if self.options['index']:
            self.sort_index()
        if self.options['python']:
            self.pythontex()


    def compile_twice(self, cmd_tex) -> None:

        os.system(cmd_tex)

        if self.options['bibtex']:
            self.run_bibtex()
        if self.options['index']:
            self.sort_index()
        if self.options['python']:
            self.pythontex()

        os.system(cmd_tex)


    def compile_fully(self, cmd_tex) -> None:

        os.system(cmd_tex)
        if self.options['bibtex']:
            self.run_bibtex()
        if self.options['python']:
            self.pythontex()
        self.sort_index()
        os.system(cmd_tex)
        if os.path.exists(self.ind):
            os.system(cmd_tex)
            self.sort_index()
        os.system(cmd_tex)
        if not self.options['keep_aux']:
            self.clear_aux()


    def run_bibtex(self) -> None:

        os.system('bibtex.exe {}'.format(self.aux))


    def sort_index(self) -> None:

        if not os.path.exists(self.idx):
            print('{} is not found'.format(self.idx))
            return

        if self.xindex_bool:
            cmd = 'xindex.exe {} {}'.format(self.index_style, self.idx)
        elif self.texindy_bool:
            cmd = 'texindy.exe {} {}'.format(self.index_style, self.idx)
        elif self.komkindex_bool:
            cmd = 'komkindex.exe {} {}'.format(self.index_style, self.idx)

        print(cmd)
        os.system(cmd)
        if self.options['bookmark_index'] or self.options['bookmark_python']:
            self.bookmark_index()


    def bookmark_index(self) -> None:

        tmp = 't@mp.ind'
        if os.path.exists(tmp):
            os.remove(tmp)
        with open(tmp, mode = 'w', encoding = 'utf-8') as new_file, open(self.ind, mode = 'r', encoding = 'utf-8') as old_file:
            if self.options['bookmark_python']:
                for line in old_file.readlines():
                    new_file.write(self.bookmark_item(line, r'\\item (.+?)\(\)'))
            else:
                for line in old_file.readlines():
                    new_file.write(self.bookmark_item(line, r'\\item (.+?),'))
        os.remove(self.ind)
        os.rename(tmp, self.ind)


    def bookmark_item(self, line, pattern) -> str:

        entry = re.search(pattern, line)
        if entry:
            entry = entry.group(1).replace('\\spxentry{', '')
            page = re.findall(r'\\hyperpage\{(\d+)\}', line)
            append = ''
            for i in range(len(page)):
                append +=  '\t\\bookmark[level=2, page={}]{{{}}}\n'.format(page[i], entry)
            line +=  append
        return line


    def clear_aux(self) -> None:

        extensions = ("aux", "bbl", "blg", "idx", "ilg", "ind", "loe", "lof", "log", "lop", "loq", "lot", "mw", "nav", "out", "pre", "pyg.lst", "pyg.sty", "pytxcode", "synctex", "snm", "toc", "tmp", "upa", "upb", "vrb")
        for ext in extensions:
            fnpattern = '*.' + ext
            for afile in glob.glob(fnpattern):
                os.remove(afile)
        for dir in glob.glob('pythontex-files-*'):
            shutil.rmtree(dir)
        for dir in glob.glob('_minted-*'):
            shutil.rmtree(dir)


    def pythontex(self) -> None:

        os.system('pythontex.exe --runall=true {}'.format(self.py))


    def compile(self, **options) -> None:

        if len(options) > 0:
            self.reconfigure(options)

        self.get_ready()

        if not self.options['compile']:
            if self.tex:
                if self.options['index']:
                    self.sort_index()
                if self.options['bibtex']:
                    self.run_bibtex()
        else:
            if self.tex:
                cmd_tex = '{} {} "{}"'.format(self.compiler, self.compile_mode, self.tex)
                if self.options['fully']:
                    self.compile_fully(cmd_tex)
                elif self.options['twice']:
                    self.compile_twice(cmd_tex)
                else:
                    self.compile_once(cmd_tex)

        if self.options['clear']:
            self.clear_aux()

        if self.options['view']:
            if os.path.exists(self.pdf):
                opener = FileOpener()
                opener.open_pdf(self.pdf)


if __name__ == "__main__":
    LC = LatexCompiler()
    LC.compile()