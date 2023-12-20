from pwny.types import *

PIPE_TYPE = 1

PIPE_INTERNAL = 10000
PIPE_STATIC = 20000
PIPE_DYNAMIC = 40000

"""
FS PIPE
"""

FS_BASE = 4

FS_TYPE_MODE = tlv_custom_type(TLV_TYPE_STRING, FS_BASE, PIPE_TYPE)

FS_PIPE_FILE = tlv_custom_pipe(PIPE_STATIC, FS_BASE, PIPE_TYPE)
