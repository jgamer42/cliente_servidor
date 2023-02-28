from actions.download import Download
from actions.upload import Upload
from actions.list import List
ACTION_MAPS = {
    "upload":Upload(),
    "download":Download(),
    "list":List(),
}