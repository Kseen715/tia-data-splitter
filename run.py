import pandas as pd
import colorama as cl
import sys
import os
import argparse


def get_input_files() -> list:
    # read all files from the input folder
    files = []
    for file in os.listdir('input'):
        if file.endswith('.csv'):
            files.append(file)

    return files


def get_file_data(file: str) -> pd.DataFrame:
    # read the file
    # remove first line of file
    with open('input/' + file, 'r') as f:
        lines = f.readlines()
    with open('input/' + file, 'w') as f:
        if 'sep=' in lines[0]:
            f.writelines(lines[1:])
        else:
            f.writelines(lines)

    data = pd.read_csv('input/' + file)
    return data


def move_file_to_success(file: str):
    # move the file to the success folder
    # if file already exists, replace it
    if os.path.exists('output/success/' + file):
        os.remove('output/success/' + file)
    os.rename('input/' + file, 'output/success/' + file)


def move_file_to_failure(file: str):
    # move the file to the failure folder
    # if file already exists, replace it
    if os.path.exists('output/failure/' + file):
        os.remove('output/failure/' + file)
    os.rename('input/' + file, 'output/failure/' + file)


def is_data_successful(data: pd.DataFrame) -> bool:
    # check if 'ShortestPathLength' column exists and last value is 0
    if 'ShortestPathLength' in data.columns:
        return data['ShortestPathLength'].iloc[-1] == 0
    else:
        return False


def split_filename(file: str):
    remove = '.csv'
    file = file.replace(remove, '')
    substrs = file.split(' ')
    if len(substrs) < 3:
        substrs.append('0')
    return substrs[0], substrs[1], substrs[2]


def main_v1():
    if not os.path.exists('input'):
        os.makedirs('input')

    files = get_input_files()
    if len(files) == 0:
        print(cl.Fore.RED +
              'No files found in the input folder. Exiting...' + cl.Fore.RESET)
        sys.exit()

    if not os.path.exists('output'):
        os.makedirs('output')

    if not os.path.exists('output/success'):
        os.makedirs('output/success')

    if not os.path.exists('output/failure'):
        os.makedirs('output/failure')

    print(cl.Fore.GREEN + 'Files found in the input folder:' + cl.Fore.RESET)
    for file in files:
        print('> "' + file + '"')

    for file in files:
        try:
            name, seed, num = split_filename(file)

            rename = name + ' ' + seed + ' ' + num + '.csv'
            os.rename('input/' + file, 'input/' + rename)
            file = rename

            data = get_file_data(file)
            if is_data_successful(data):

                move_file_to_success(file)
                print(cl.Fore.GREEN + seed + '[' + num + ']' + cl.Fore.RESET)
            else:
                move_file_to_failure(file)
                print(cl.Fore.RED + seed + '[' + num + ']' + cl.Fore.RESET)
        except:
            print(cl.Fore.RED + 'Error processing file: ' + file + cl.Fore.RESET)


if __name__ == '__main__':
    LATEST_VERSION = 1
    version = LATEST_VERSION
    args = argparse.ArgumentParser()
    args.add_argument('-v', '--version', type=int,
                      help='version of the script to run')
    args = args.parse_args()
    if args.version is not None:
        version = args.version

    if not version > LATEST_VERSION and version > 0:
        print(cl.Fore.CYAN + '===--- Running script v' +
              str(version) + cl.Fore.RESET)
    else:
        print(cl.Fore.RED + 'Invalid version number' + cl.Fore.RESET)
        sys.exit()

    if version == 1:
        main_v1()
    else:
        print(cl.Fore.RED + 'Unhandled version number' + cl.Fore.RESET)
        sys.exit()
