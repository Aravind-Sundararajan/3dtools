__version__='0.0.3'

__all__ = ['get_vtp2stl', 'get_stl2obj', 'get_mirrorobj']


def get_vtp2stl():
    from . import vtp2stl
    return vtp2stl

def get_stl2obj():
    from . import stl2obj
    return stl2obj

def get_mirrorobj():
    from . import mirrorobj
    return mirrorobj
