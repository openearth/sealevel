import pathlib


def get_src_dir():
    """get the source directory from this repository"""
    # this assumes setup.py develop / pip install -e
    return pathlib.Path(__file__).parent.parent.parent
