#!/usr/bin/env python3
import os
import subprocess


def cd(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        print('bash: cd: %s: No such file or directory' % path)


def handle_cd_inp(inp):
    try:
        path = inp[1]
        if path == '~':
            path = os.getenv('HOME')
        elif path == '-':
            path = '..'
    except IndexError:
        path = os.getenv('HOME')
    return path


def printenv(_keys):
    env = os.environ
    if _keys == 'all':
        for param in env.keys():
            print("%s=%s" % (param, env[param]))
    else:
        for _key in _keys:
            value = env.get(_key)
            if value:
                print(value)


def export(arg):
    for item in arg:
        if '=' in item:
            var = item.split('=', 1)
            key, value = var[0], var[1]
            os.environ[key] = value
        else:
            key = item
            os.environ[key] = ''


def unset(keys):
    for key in keys:
        try:
            os.environ.pop(key)
        except KeyError:
            pass


def exec_shell(inp):
    command = inp[0]
    if command.startswith('./'):
        if os.access(command, os.X_OK):
            subprocess.run(command)
        else:
            print("intek-sh: %s: Permission denied" % command)
    else:
        path_group = os.environ.get('PATH')
        # path_group = None
        if path_group:
            paths = path_group.split(':')
            for path in paths:
                if os.path.isdir(path):
                    source = os.listdir(path)
                    if command in source:
                        if os.access(os.path.join(path, command), os.X_OK):
                            subprocess.run(inp)
                        else:
                            print("intek-sh: %s: Permission denied" % command)
                        break
            else:
                print('intek-sh: %s: command not found' % command)
        else:
            print('intek-sh: %s: command not found' % command)
    # path = '/home/pan/pan'
    # if os.access(os.path.join(path, command), os.X_OK):
    #     print("Permission OK")
    # else:
    #     print("intek-sh: %s: Permission denied" % command)


def print_exit_ouput(inp):
    print('exit')
    try:
        if inp[1] and not inp[1].isdigit():
            print('intek-sh: exit:')
    except IndexError:
        pass


def main():
    loop = True
    while loop:
        try:
            inp = input('intek-sh$ ').split()
            print(inp)
        except EOFError:
            return
        if inp:
            command = inp[0]
            if command.startswith('exit'):
                print_exit_ouput(inp)
                break
            elif command == 'cd':
                path = handle_cd_inp(inp)
                if not path:
                    print("intek-sh: cd: HOME not set")
                else:
                    cd(path)
            elif command == 'printenv':
                keys = inp[1:]
                if not keys:
                    keys = 'all'
                printenv(keys)
            elif command == 'export':
                arg = inp[1:]
                export(arg)
            elif command == 'unset':
                keys = inp[1:]
                unset(keys)
            else:
                exec_shell(inp)


if __name__ == '__main__':
    main()
