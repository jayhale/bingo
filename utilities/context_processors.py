from bingo import __version__

from utilities.models import Announcement


def version(request):
    return { 'version': __version__ }


def announcements(request):
    return { 'announcements': Announcement.get_current_announcements() }