
import os
import sys
import configparser
import argparse
import subprocess


def check_TeXLive():

    try:
        subprocess.check_call('mktexlsr.exe --version')
    except OSError:
        print("Make sure TeX Live is included in PATH.")
        sys.exit()


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description ='Configure your documentation environment for LaTeX.'
    )
    parser.add_argument(
        '-s',
        dest = 'store_to_local',
        action = 'store_true',
        default = False,
        help = 'If one or more files are specified, copy them into the local TEXMF directory.'
    )
    parser.add_argument(
        '-H',
        dest = 'texmfhome',
        action = 'store_true',
        default = False,
        help = 'Set TEXMFHOME as an environment variable.'
    )
    parser.add_argument(
        '-L',
        dest = 'local_conf',
        action = 'store_true',
        default = False,
        help = "Create local.conf with the user's local font directory."
    )
    parser.add_argument(
        '-e',
        dest = 'texedit',
        action = 'store_true',
        default = False,
        help = 'Set TEXEDIT as an environment variable.'
    )
    parser.add_argument(
        '-p',
        dest = 'sumatrapdf',
        action = 'store_true',
        default = False,
        help = 'Set Sumatra PDF to enable inverse search. (jumping back to the corresponding point in the source tex file)'
    )
    parser.add_argument(
        '-r',
        dest = 'set_repository',
        action = 'store_true',
        default = False,
        help = 'Set the main TeX Live repository.'
    )
    parser.add_argument(
        '-u',
        dest = 'update_texlive',
        action = 'store_true',
        default = False,
        help = 'Update TeX Live.'
    )
    parser.add_argument(
        '-c',
        dest = 'cache_font',
        action = 'store_true',
        default = False,
        help = 'Cache fonts for XeLaTeX.'
    )
    parser.add_argument(
        '-l',
        dest = 'luaotfload',
        action = 'store_true',
        default = False,
        help = 'Update the font database for LuaLaTeX.'
    )
    parser.add_argument(
        '-f',
        dest = 'format_rebuild',
        action = 'store_true',
        default = False,
        help = 'Rebuild formats. This could help when 64-bit LuaLaTeX is not working properly.'
    )
    parser.add_argument(
        '-b',
        dest = 'batch',
        action = 'store_true',
        default = False,
        help = 'Get every option done at once.'
    )
    parser.add_argument(
        '-q',
        dest = 'confirmation_bool',
        action = 'store_false',
        default = True,
        help = 'Proceed without asking for confirmation.'
    )

    return parser.parse_args()


def confirm(msg) -> str:

    if args.confirmation_bool:
        answer = input(msg)
        return answer
    else:
        return 'y'


def store_to_local() -> None:

    print('\n[Copying latex style files]')
    try:
        latex_style = config.get('Sphinx Style', 'latex')
        texmf_local = config.get('TeX Live', 'texmflocal')
    except:
        print('Make sure to have docenv.conf set properly.')
        return
    query = "These files are going to be copied into '{}'\n{}\nEnter [Y] to proceed, [n] to abandon, or another directory: ".format(texmf_local, latex_style.replace(', ', '\n'))
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texmf_local = answer
    files = latex_style.split(', ')
    for afile in files:
        src = os.path.join(inipath, afile)
        if os.path.exists(src):
            cmd = 'copy {} {}'.format(src, texmf_local)
            os.system(cmd)
    cmd = 'dir {}'.format(texmf_local)
    os.system(cmd)
    os.system('mktexlsr.exe')


def set_texmfhome() -> None:

    print('\n[Setting TEXMFHOME]')
    try:
        texmfhome = config.get('TeX Live', 'TEXMFHOME')
    except:
        print('Make sure to have docenv.conf set properly.')
        return
    query = "Are you sure to set the TEXMFHOME environment variable to  '{}'?\nEnter [Y] to proceed, [n] to abandon, or another path: ".format(texmfhome)
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texmfhome = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXMFHOME -value '{}'\"".format(texmfhome)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXMFHOME'\""
    os.system(cmd)


def set_texedit() -> None:

    print('\n[Setting TEXEDIT]')
    try:
        texedit = config.get('TeX Live', 'TEXEDIT')
    except:
        print('Make sure to have docenv.conf set properly.')
        return
    query = "Are you sure to set the TEXEDIT environment variable to  '{}'?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ".format(texedit)
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        texedit = answer
    cmd = "powershell \"set-itemproperty -path HKCU:\\Environment -name TEXEDIT -value '{}'\"".format(texedit)
    os.system(cmd)
    cmd = "powershell \"(get-itemproperty -path HKCU:\\Environment).'TEXEDIT'\""
    os.system(cmd)


def set_sumatrapdf() -> None:

    print('\n[Setting Sumatra PDF')
    try:
        sumatra = config.get('Sumatra PDF', 'path')
        editor = config.get('Sumatra PDF', 'inverse-search')
    except:
        print('Make sure to have docenv.conf set properly.')
        return
    query = "Are you sure to use '{}' to enable the inverse search feature of Sumatra PDF?\nEnter [Y] to proceed, [n] to abandon, or another text editor with its option: ".format(editor)
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    if not (answer.lower() == 'y' or answer == ''):
        editor = answer
    # cmd = []
    # cmd.append(sumatra)
    # cmd.append('-inverse-search')
    # cmd.append(editor)
    cmd = [sumatra, '-inverse-search', editor]
    subprocess.Popen(cmd)


def create_local_conf() -> None:

    print('\n[local.conf]')
    try:
        local_conf = config.get('LOCAL.CONF', 'path')
        content = config.get('LOCAL.CONF', 'content')
    except:
        print('Make sure to have docenv.conf set properly')
        return
    query = "'{}' will be created to include {}\nEnter [Y] to proceed, [n] to abandon. ".format(local_conf, content)
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    else:
        with open(local_conf, mode='w') as f:
            f.write(content)


def update_texlive() -> None:

    print('\n[Updating the TeX Live]')
    query = 'Are you sure to update the TeX Live?\nEnter [Y] to proceed or [n] to abandon: '
    answer = confirm(query)
    if answer.lower() == 'n':
        return
    else:
        os.system('tlmgr.bat update --self --all')


def set_repository() -> None:

    repository = get_repository('main')
    if repository:
        os.system('tlmgr.bat option repository {}'.format(repository))
    repository = get_repository('private')
    if repository:
        os.system('tlmgr.bat repository add {} private'.format(repository))
        os.system('tlmgr.bat pinning add private "*"')
    os.system('tlmgr.bat repository list')


def get_repository(kind) -> str or False:

    print('\n[Setting the {} repository]'.format(kind))
    option = 'repository_{}'.format(kind)
    url = config.get('TeX Live', option, fallback=False)
    if url:
        query = "Are you sure to set '{}' as the {} repository?\nEnter [Y] to proceed, [n] to abandon, or another repository: ".format(url, kind)
        answer = confirm(query)
        if (answer.lower() == 'y' or answer == ''):
            return url
        elif answer.lower() == 'n':
            return False
        else:
            return answer
    else:
        return False


def cache_font() -> None:

    print('\n[Caching fonts]')
    query = 'Are you sure to cache fonts for XeLaTeX?\nEnter [Y] to proceed or [n] to abandon: '
    answer = confirm(query)
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'fc-cache.exe -v -r'
        os.system(cmd)


def luaotfload() -> None:

    query = 'Are you sure to update the font database for LuaLaTeX?\nEnter [Y] to proceed or [n] to abandon: '
    answer = confirm(query)
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'luaotfload-tool --update --force --verbose=3'
        os.system(cmd)


def format_rebuild() -> None:

    query = 'Are you sure to rebuild formats for LuaLaTeX?\nEnter [Y] to proceed or [n] to abandon: '
    answer = confirm(query)
    if (answer.lower() == 'y' or answer == ''):
        cmd = 'fmtutil-sys --all'
        os.system(cmd)

def ToContinue(func) -> bool:

    if args.confirmation_bool:
        query = '\nDo you want to continue this batch configuration? [Y/n] '
        answer = confirm(query)
    else:
        answer = 'y'
    if answer.lower() == 'n':
        return False
    else:
        func()
        return True


def configure() -> None:

    if args.batch:
        if not ToContinue(store_to_local):
            return None
        if not ToContinue(set_texmfhome):
            return None
        if not ToContinue(create_local_conf):
            return None
        if not ToContinue(set_texedit):
            return None
        if not ToContinue(set_sumatrapdf):
            return None
        if not ToContinue(set_repository):
            return None
        if not ToContinue(update_texlive):
            return None
        if not ToContinue(cache_font):
            return None
        ToContinue(luaotfload)
    else:
        if args.store_to_local:
            store_to_local()
        if args.texmfhome:
            set_texmfhome()
        if args.local_conf:
            create_local_conf()
        if args.texedit:
            set_texedit()
        if args.sumatrapdf:
            set_sumatrapdf()
        if args.set_repository:
            set_repository()
        if args.update_texlive:
            update_texlive()
        if args.cache_font:
            cache_font()
        if args.format_rebuild:
            format_rebuild()
        if args.luaotfload:
            luaotfload()


inipath = os.path.dirname(__file__)
ini = os.path.join(inipath, 'docenv.conf')
if os.path.exists(ini):
    config = configparser.ConfigParser()
    config.read(ini)
else:
    print('docenv.conf is not found.')
    sys.exit()

check_TeXLive()
args = parse_args()
configure()