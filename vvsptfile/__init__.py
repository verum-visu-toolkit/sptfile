from .format import get_body_fmt_str
from .pack import pack
from .unpack import unpack, create_spt

pbar = None


def init_progress_bar(_pbar):
    global pbar
    pbar = _pbar
