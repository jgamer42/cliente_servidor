from actions.download import Download
from actions.upload import Upload
ACTION_MAPS = {
    "upload":Upload(),
    "download":Download()
}