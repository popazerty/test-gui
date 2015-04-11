from Screens.Screen import Screen
from Screens.Console import Console
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Components.Label import Label
menu_s = '/usr/lib/enigma2/python/Plugins/Satdreamgr/SDGBackup/dreambox-fullbackup.sh'

def main(session, **kwargs):
    try:
        session.open(SDGBackup)
    except:
        print '[SDGBackup] Pluginexecution failed'


def autostart(reason, **kwargs):
    if reason == 0:
        print '[PluginMenu] no autostart'


def menu(menuid, **kwargs):
    if menuid == 'cam':
        return [(_('SDGBackup Dreambox Enigma2'),
          main,
          'sdgbackup_setup',
          45)]
    return []


def Plugins(**kwargs):
    return PluginDescriptor(name=_('SDGBackup Dreambox Enigma2'), description=_('SDGBackup Dreambox Enigma2'), where=PluginDescriptor.WHERE_MENU, fnc=menu)


class SDGBackup(Screen):
    skin = '\n        <screen position="center,center" size="460,400" title="SDGBackup Dreambox Enigma2" >\n        <widget name="menu" position="10,10" size="420,380" scrollbarMode="showOnDemand" />\n\t\t<widget name="myRedBtn" position="10,320" size="100,40" backgroundColor="red" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;20"/>\n\t\t<widget name="myGreenBtn" position="120,320" size="100,40" backgroundColor="green" valign="center" halign="center" zPosition="2"  foregroundColor="white" font="Regular;20"/>\n        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.location = ''
        menu = []
        menu.append((_('Start SDGBackup on USB'), '/media/usb'))
        menu.append((_('Start SDGBackup on HDD'), '/media/hdd'))
        self['myRedBtn'] = Label(_('Cancel'))
        self['myGreenBtn'] = Label(_('OK'))
        self['menu'] = MenuList(menu)
        self['actions'] = ActionMap(['OkCancelActions',
         'SetupActions',
         'ColorActions',
         'WizardActions',
         'DirectionActions'], {'ok': self.go,
         'green': self.go,
         'cancel': self.close}, -1)

    def go(self):
        returnValue = self['menu'].l.getCurrentSelection()[1]
        if returnValue:
            self.location = returnValue
            self.session.openWithCallback(self.greek, MessageBox, _('Confirm your selection, or exit'), MessageBox.TYPE_YESNO)

    def greek(self, answer):
        if answer:
            self.session.open(Console, _('Backup is running...'), ['%s %s' % (menu_s, self.location)])
