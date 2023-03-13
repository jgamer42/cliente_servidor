from actions.download import Download
from actions.upload import Upload
from actions.list import List
from actions.add import Add
ACTION_MAPS = {
    "upload":Upload(),
    "download":Download(),
    "list":List(),
    "add":Add()
}