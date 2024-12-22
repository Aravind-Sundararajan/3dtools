import py3dtools

vtp2stl = py3dtools.get_vtp2stl()
stl2obj = py3dtools.get_stl2obj()
vtp2stl.convert_files('test', 'test')
stl2obj.convert_files('test', 'test')
