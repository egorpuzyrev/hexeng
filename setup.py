from distutils.core import setup
import py2exe

setup(
    #~ windows=[{"script":"main.py"}],
    console=['main.py'],
    options={'py2exe':
        {'optimize': 2,
        'ascii': False,
        #~ 'compressed': 2,
        'excludes': [
                     #~ '_ssl', 'doctest', 'pdb', 'unittest', 'difflib',
                     #~ 'inspect',
                     #~ 'numbers',
                     #~ 'optparse', 'pickle', 'calendar', 'email',
                     #~ 'http', 'xml', 'PySide', 'PyQt4', 'PyQt5', 'PyQt',
                     #~ 'multiprocessing', 'socket', 'select', 'bz2', 'html',
                     #~ '_bz2', 'tcl'
                     ],
        'includes': [
                     'numbers',
                     ],
        #~ 'dll_excludes': ['pyside-python3.4.dll', 'shiboken-python3.4.dll',
        #~ 'QtNetwork4.dll', 'QtGui4.dll', 'QtNetwork4.dll']
        # ~ 'excludes': ['PyQt4', 'PyQt5']
        }
    }
)
