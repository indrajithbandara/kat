import logging

# Shut up apport, which is buggered up on Ubuntu 16.04.3 LTS over Py3.6
logging.getLogger('py.warnings').setLevel('ERROR')
