import OOPapi as api
from pypac import PACSession, get_pac
from pypac.parser import PACFile

thread = api.Connection('http://rutracker.org/forum')
thread.obtaindata()
a = thread.refreshcookies()