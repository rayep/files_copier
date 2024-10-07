"""
Files Copier

Utility to copy files from source to target directory.
Supports recursive copying & sub-directory creation.

Author - Ray A.
"""

from shutil import copytree
from os import W_OK, R_OK, access
from os.path import isfile, isabs, abspath, exists, join, normpath, isdir
from argparse import ArgumentParser

_args = ArgumentParser(
    prog="copier.py", description="A Simple File Directory Copier")
_args.add_argument("-s", action='store', required=True, dest='src',
                   type=str, help="Source directory path to copy from.")
_args.add_argument("-d", action='store', required=True, dest='dst',
                   type=str, help="Target directory path to copy files to.")
args = _args.parse_args()


class DirNotFoundError(OSError):
    """Directory not found error"""


class DirReadAccessFailed(OSError):
    """Dir read access failed/denied"""


class DirWriteAccessFailed(OSError):
    """Dir write access failed/denied"""


def make_abspath(path: str):
    """Create absolute path for the provided path string"""
    return normpath(path) if isabs(path) else abspath(path)


def check_directory_access(path: str):
    """Check directory access for source & target"""
    abs_path = make_abspath(path)
    if not isdir(path):
        raise DirNotFoundError(path)

    def _access(_type: int):
        if _type == R_OK:
            if not access(abs_path, R_OK):
                raise DirReadAccessFailed(abs_path)
        else:
            if not access(abs_path, W_OK):
                raise DirWriteAccessFailed(abs_path)
        return abs_path
    return _access


def check_file_exists(dirpath: str):
    """Check if the file exists"""
    def exist_check(filepath: str):
        full_path = join(dirpath, filepath)
        return exists(full_path) if isfile(full_path) else False
    return exist_check


def ignore_files(source_path: str, target_path: str):
    """Returns a list of files that are not present in the target directory"""
    def check_files(*args):
        source_dir, files = args
        parsed_target_dir = source_dir.replace(source_path, target_path)
        existing_files = list(
            filter(check_file_exists(parsed_target_dir), files))
        return existing_files
    return check_files


def copier(source_dir: str, target_dir: str):
    """Copier Utility"""
    return copytree(
        source_dir,
        target_dir,
        ignore=ignore_files(source_dir, target_dir),
        dirs_exist_ok=True)


src_dir = check_directory_access(args.src)(R_OK)
trg_dir = check_directory_access(args.dst)(W_OK)

copier(src_dir, trg_dir)
