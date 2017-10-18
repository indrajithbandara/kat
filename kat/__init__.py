import logging
import disco
import platform

__version__ = '7.0.2'
__revision__ = '3'
__license__ = 'BSD 2-Clause License'
__author__ = 'TheRooChan'
__copyright__ = 'Copyright (c) 2017, TheRooChan, Eevee'
__credits__ = ['Modernnecro', 'Smidgey', 'Eevee', 'TheRooChan/Espy']
__maintainer__ = 'TheRooChan'
__email__ = ''
__status__ = 'Beta'
__date__ = '18th October 2017'
__repository__ = 'http://github.com/TheRooChan/katherine'

# Shut up apport, which is buggered up on Ubuntu 16.04.3 LTS over Py3.6
# This is really annoying me when doing dev.
logging.getLogger('py.warnings').setLevel('ERROR')
