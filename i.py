import os
import sys
import glob
import argparse
import configparser
import re
# companions of i.py
from ltx import LatexCompiler
from op import FileOpener

ini = 'i.ini'
ini_template = '''[tex]
target = foo.tex
compiler =
draft = wordig.py -a "..." -s "..." %(target)s
final = wordig.py -a "..." -s "..." %(target)s
final_compiler =
after =
main = \\input{preamble}
    \\begin{document}
    \\maketitle
    \\input{\\1}
    \\end{document}'''

def parse_args() -> argparse.Namespace:

    # about = 'i.ini should be like:\n{}'.format(ini_template)

    # parser = argparse.ArgumentParser(
    #     epilog = about,
    #     formatter_class = argparse.RawDescriptionHelpFormatter,
    #     description = 'Find and compile a tex file using ltx.py. Options unknown to this script are passed to ltx.py.'
    # )
    parser = argparse.ArgumentParser(
        description = "Find and compile a tex file using ltx.py. Options unknown to this script are passed to ltx.py."
    )
    parser.add_argument(
        'tex',
        nargs = '?'
    )
    parser.add_argument(
        '-U',
        dest = 'list_bool',
        action = 'store_true',
        default = False,
        help = 'Enumerate every tex file to select and update i.ini.'
    )
    parser.add_argument(
        '-D',
        dest = 'draft_bool',
        action = 'store_true',
        default = False,
        help = 'Run the draft pre-processing option specified in the configuration file, i.ini.'
    )
    parser.add_argument(
        '-F',
        dest = 'final_bool',
        action = 'store_true',
        default = False,
        help = 'Run the final pre-processing option.'
    )
    parser.add_argument(
        '-W',
        dest = 'wrap_bool',
        action = 'store_true',
        default = False,
        help = "Wrap up the specified file with the main option's."
    )
    parser.add_argument(
        '-N',
        dest = 'run_bool',
        action = 'store_false',
        default = True,
        help = "Don't compile only to update i.ini."
    )
    parser.add_argument(
        '-C',
        dest = 'create_ini_bool',
        action = 'store_true',
        default = False,
        help = 'Create i.ini.'
    )

    return parser.parse_known_args()


def run_preprocess(target) -> None:

    global args, preset_option

    if not os.path.exists(ini):
        print('i.ini is not found.')
        return

    conf = configparser.ConfigParser()
    conf.read(ini)

    if args.draft_bool:
        cmds = conf.get('tex', 'draft', fallback=False)
    else:
        cmds = conf.get('tex', 'final', fallback=False)

    if cmds:
        cmds = cmds.split('\n')
        for cmd in cmds:
            os.system(cmd)

    if args.final_bool:
        compiler = conf.get('tex', 'final_compiler', fallback=False)
        if compiler:
            compiler = compiler.split(' ')
            for i in compiler:
                preset_option.append(i)


def run_postprocess() -> None:

    if not os.path.exists(ini):
        return

    conf = configparser.ConfigParser()
    conf.read(ini)
    cmd = conf.get('tex', 'after', fallback=False)
    if cmd:
        os.system(cmd)


def write_tex(tex)  -> str:

    if os.path.exists(ini):
        conf = configparser.ConfigParser()
        conf.read(ini, encoding='utf-8')
        main = conf.get('tex', 'main', fallback=False)
        if main:
            main = main.replace('\\1', tex)

        with open('t@x.tex', mode='w') as f:
            f.write(main)

        basename = os.path.basename(tex)
        fnpattern = os.path.splitext(basename)[0]
        pdf = fnpattern + '.pdf'
        tex = 't@x.tex'
        return pdf
    else:
        return False


def compile_tex(tex) -> None:

    global args, preset_option

    if not args.run_bool:
        return

    if os.path.exists(ini):
        conf = configparser.ConfigParser()
        conf.read(ini)
        compiler = conf.get('tex', 'compiler', fallback=False)
        if compiler:
            compiler = compiler.split(' ')
            for i in compiler:
                preset_option.append(i)

    if type(tex) is list:
        for i in tex:
            do_compile(i)
    else:
        do_compile(tex)


def do_compile(tex) -> None:

    global args, compile_option, preset_option

    if args.draft_bool or args.final_bool:
        run_preprocess(tex)

    if args.wrap_bool:
        pdf = write_tex(tex)
        if pdf:
            tex = 't@x.tex'

    compile_option = compile_option + preset_option
    print('{} {}'.format(tex, compile_option))
    LC = LatexCompiler(tex, compile_option)
    LC.compile()

    if args.wrap_bool:
        if os.path.exists('t@x.pdf'):
            if os.path.exists(pdf):
                os.remove(pdf)
            os.rename('t@x.pdf', pdf)

    run_postprocess()


def update_ini(selection) -> None:

    conf = configparser.ConfigParser()

    if os.path.exists(ini):
        conf.read(ini)
        conf.set('tex', 'target', selection)
    else:
        conf['tex'] = {'target': selection}

    with open(ini, 'w') as f:
        conf.write(f)


def count_tex_files() -> list:

    global args
    files = []

    if args.tex is None:
        fnpattern = '*.tex'
    else:
        fnpattern, ext = os.path.splitext(args.tex)
        if ext == '.':
            fnpattern += '.tex'
        elif not '*' in fnpattern:
            fnpattern = fnpattern.replace('.\\', '')
            fnpattern = '*{}*'.format(fnpattern) + '.tex'

    for i in glob.glob(fnpattern):
        files.append(i)

    if len(files) == 0:
        print('No tex files are found.')

    return len(files), files


def get_target() -> str or False:

    count, existing_files = count_tex_files()

    if count == 0:
        sys.exit()
    elif count == 1:
        return existing_files[0]
    else:
        if os.path.exists(ini):
            conf = configparser.ConfigParser()
            conf.read(ini)
            registered_files = conf.get('tex', 'target', fallback=False)
            if registered_files:
                registered_files = registered_files.split('\n')
                if len(registered_files) == 1:
                    return registered_files[0]
                else:
                    return enumerate_list(registered_files)
            else:
                return False
        else:
            return False


def enumerate_list(files) -> str or False:

    global args

    if args.tex is not None:
        tmp = files.copy()
        files.clear()
        for i in tmp:
            if args.tex in i:
                files.append(i)
        if len(files) == 1:
            return files[0]

    for i, v in enumerate(files):
        print('{}:{}'.format(i+1, v))
    selection = input('\nSelect a file by entering its number, or enter "0" for all: ')

    if selection == '':
        sys.exit()
    if selection == '0':
        return files

    tmp = selection.split()
    selection = []
    for i in tmp:
        if '-' in i:
            x = i.split('-')
            try:
                x = range(int(x[0]), int(x[1])+1)
                for n in x:
                    selection.append(n)
            except:
                print('Wrong selection.')
                return False
        else:
            try:
                selection.append(int(i))
            except:
                print('Wrong selection.')
                return False

    if len(selection) > 0:
        for i, v in enumerate(selection):
            selection[i] = files[v-1]
        return selection
    else:
        return False


def determine_from_list() -> str or False:

    count, files = count_tex_files()

    if count == 0:
        return False
    elif count == 1:
        return files[0]

    selection = enumerate_list(files)
    if selection:
        update_ini('\n'.join(selection))
        return selection
    else:
        return False


def create_ini() -> None:

    if os.path.exists(ini):
        answer = input('{} already exists. Are you sure to overwrite it? [y/N] '.format(ini))
        if answer.lower() == 'y':
            os.remove(ini)
        else:
            return

    with open(ini, mode='w', encoding='utf-8') as f:
        f.write(ini_template)
    opener = FileOpener()
    opener.open_txt(ini)


def determine_tex() -> None:

    if args.create_ini_bool:
        create_ini()
    elif args.list_bool:
        tex = determine_from_list()
        if tex:
            compile_tex(tex)
    else:
        tex = get_target()
        if tex:
            compile_tex(tex)
        else:
            tex = determine_from_list()
            if tex:
                compile_tex(tex)

global args, compile_option
global preset_option
preset_option = []
args, compile_option = parse_args()
determine_tex()