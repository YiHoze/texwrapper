import os
import sys
import glob
import argparse
import configparser
import subprocess
import re

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))


class ScriptScribe(object):

    def __init__(self):

        self.dbFile = 'scripts.db'
        self.dbFile = os.path.join(dirCalled, self.dbFile)
        if os.path.exists(self.dbFile):
            self.database = configparser.ConfigParser()
            self.database.read(self.dbFile, encoding='utf-8')
        else:
            print('{} is not found.'.format(self.dbFile))
            sys.exit()

        self.parse_args()

        if self.section:
            if self.args.update_bool:
                self.update()
            elif self.args.insert_bool:
                self.insert_new()
            elif self.args.remove_bool:
                self.remove()
            else:
                self.pick_script()
        else:
            if self.args.burst_bool:
                self.burst_database()
            else:
                self.parser.print_help()
                self.enumerate_scripts()


    def parse_args(self) -> None:

        self.parser = argparse.ArgumentParser(
            add_help=False,
            description = 'Extract a script from "scripts.db" to run it.'
        )
        self.parser.add_argument(
            'script',
            nargs = '*'
        )
        self.parser.add_argument(
            '-I',
            dest = 'insert_bool',
            action = 'store_true',
            default = False,
            help = 'Insert a new script file into the database file.'
        )
        self.parser.add_argument(
            '-U',
            dest = 'update_bool',
            action = 'store_true',
            default = False,
            help = 'Update the database with the file being in the current directory.'
        )
        self.parser.add_argument(
            '-R',
            dest = 'remove_bool',
            action = 'store_true',
            default = False,
            help = 'Remove the specified script from the database file.'
        )
        self.parser.add_argument(
            '-B',
            dest = 'burst_bool',
            action = 'store_true',
            default = False,
            help = 'Take out every script.'
        )
        self.parser.add_argument(
            '-N',
            dest = 'run_bool',
            action = 'store_false',
            default = True,
            help = 'Extract but do not run the specified script.'
        )
        self.parser.add_argument(
            '-C',
            dest = 'clear_bool',
            action = 'store_true',
            default = False,
            help = 'Delete the extracted script file after a run.'
        )

        self.args, unknown_options = self.parser.parse_known_args()
        if len(self.args.script) > 0:
            self.section = self.args.script[0]
            self.script_arguments = self.args.script
            del self.script_arguments[0]
            self.script_arguments = unknown_options + self.script_arguments
        else:
            self.section = None


    def check_section(self) -> bool:

        if self.database.has_section(self.section):
            return True
        else:
            print('"{}" is not included in the database.'.format(self.section))
            return False


    def confirm_to_overwrite(self, file) -> bool:

        if not self.args.run_bool:
            return True

        if file is None:
            print('Ensure the script database file is set properly.')
            return False
        else:
            if os.path.exists(file):
                answer = input('"{}" already exists. Are you sure to overwrite it? [y/N] '.format(file))
                if answer.lower() == 'y':
                    os.remove(file)
                    return True
                else:
                    return False
            else:
                return True


    def write_from_database(self, filename, source) -> bool:

        if self.confirm_to_overwrite(filename):
            try:
                content = self.database.get(self.section, source)
            except:
                print('Ensure the script database is set properly.')
                return False
            ext = os.path.splitext(filename)[1].lower()
            if ext != '.cmd':
                content = content.replace('```', '')
            if ext == '.tsv':
                content = re.sub("$", "\t", content, flags=re.MULTILINE)
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False


    def pick_script(self) -> None:

        if self.args.run_bool:
            if not self.check_section():
                return

        options = self.database.options(self.section)
        for option in options:
            if 'output' in option:
                filename = self.database.get(self.section, option)
                if option == 'code_output':
                    codefile = filename
                source = option.split('_')[0]
                if not self.write_from_database(filename, source):
                    return

        if self.args.run_bool:
            ext = os.path.splitext(codefile)[1]
            cmd = self.script_arguments
            if ext == '.ps1':
                cmd.insert(0,'powershell.exe ./{}'.format(codefile))
            if ext == '.py':
                cmd.insert(0,'python.exe {}'.format(codefile))
            else:
                cmd.insert(0, codefile)

            if len(self.script_arguments) == 1:
                sargs = self.database.get(self.section, 'default_arguments', fallback=None)
                if sargs:
                    cmd.append(sargs)
            cmd = ' '.join(cmd)
            print(cmd)
            cmd = cmd.split(' ')
            subprocess.run(cmd)

            if self.args.clear_bool:
                os.remove(codefile)


    def if_exist(self, filename) -> bool:

        if os.path.exists(filename):
            return True
        else:
            print('"{}" does not exist in the current directory.'.format(filename))
            return False


    def read_script_file(self, filename) -> tuple[str, str]:

        ext = os.path.splitext(filename)[1].lower()

        if ext == '.py':
            script_type = '[Python]'
        elif ext == '.ps1':
            script_type = '[PowerShell]'
        elif ext == '.cmd':
            script_type = '[cmd]'
        elif ext == '.jsx':
            script_type = '[JavaScript]'
        elif ext == '.bas':
            script_type = '[Visual Basic]'
        elif ext == '.tsv':
            script_type = '[Tab-separated values]'
        else:
            script_type = '[Unknown]'

        with open(filename, mode='r', encoding='utf-8') as f:
            code = f.read()
        code = re.sub('%', '%%', code)
        if ext != '.cmd':
            code = re.sub('^', '```', code, flags=re.MULTILINE)

        found = re.search('(?<= description = ).*$', code, flags=re.MULTILINE)
        if found:
            description = found.group(0)
            description = re.sub("^'", "", description)
            description = re.sub("'$", "", description)
            description = re.sub('^"', '', description)
            description = re.sub('"$', '', description)
            description = '{} {}'.format(script_type, description)
        else:
            description = script_type

        return description, code

    #>myscript.py -I foo.py conf_output=foo.conf
    def insert_new(self) -> None:

        filename = os.path.basename(self.section)
        if not self.if_exist(filename):
            return

        self.section = os.path.splitext(filename)[0]
        if self.section in self.database.sections():
            print('"{}" is already included in the database.'.format(self.section))
            return

        description, code = self.read_script_file(filename)

        self.database.add_section(self.section)
        self.database.set(self.section, 'description', description)
        self.database.set(self.section, 'code_output', filename)
        self.database.set(self.section, 'code', code)
        self.check_auxiliary_files()

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully inserted.')


    # Read auxiliary files if specified
    def check_auxiliary_files(self) -> None:

        if len(self.args.script) > 0:
            for i in self.args.script:
                option_filename, filename = i.split('=')
                if not self.if_exist(filename):
                    continue
                option_content = re.sub('_output', '', option_filename)
                with open(filename, mode='r', encoding='utf-8') as f:
                    content = f.read()
                content = re.sub('%', '%%', content)
                content = re.sub('^', '```', content, flags=re.MULTILINE)
                self.database.set(self.section, option_filename, filename)
                self.database.set(self.section, option_content, content)


    def update(self) -> None:

        if not self.check_section():
            return

        filename = self.database.get(self.section, 'code_output')
        if not self.if_exist(filename):
            return

        description, code = self.read_script_file(filename)

        self.database.set(self.section, 'description', description)
        self.database.set(self.section, 'code', code)

        # Update auxiliary files if any.
        options = self.database.options(self.section)
        for option in options:
            if 'output' in option:
                filename = self.database.get(self.section, option)
                if not self.if_exist(filename):
                    continue
                with open (filename, mode='r', encoding='utf-8') as f:
                    content = f.read()
                content = re.sub('%', '%%', content)
                content = re.sub('^', '```', content, flags=re.MULTILINE)

                option_content = re.sub('_output', '', option)
                self.database.set(self.section, option_content, content)

        with open(self.dbFile, mode='w', encoding='utf-8') as f:
            self.database.write(f)
            print('Successfully updated.')


    def remove(self) -> None:

        if not self.check_section():
            return

        answer = input('Are you sure to remove "{}" from the database? [y/N] '.format(self.section))
        if answer.lower() == 'y':
            self.database.remove_section(self.section)
            with open(self.dbFile, mode='w', encoding='utf-8') as f:
                self.database.write(f)
                print('Successfully removed.')


    def enumerate_scripts(self) -> None:

        scripts = sorted(self.database.sections(), key=str.casefold)

        print()
        for i in scripts:
            description = self.database.get(i, 'description', fallback=None)
            if description is None:
                description = ''
            print('{:12} {}'.format(i,description))


    def burst_database(self) -> None:

        self.args.run_bool = False
        scripts = sorted(self.database.sections(), key=str.casefold)

        for i in scripts:
            self.script = i
            self.pick_script()


if __name__ == '__main__':
    ScriptScribe()