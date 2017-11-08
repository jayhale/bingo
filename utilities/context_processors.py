from bingo import __version__

def version(request):
    return { 'version': __version__ }