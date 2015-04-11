from Screens.Screen import Screen
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.config import config
from Tools.LoadPixmap import LoadPixmap
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from SDG_Vhannibal import SDG_VhannibalHelper
from SDG_Morpheus import SDG_MorpheusHelper
from SDG_Satdreamgr import SDG_SatdreamgrHelper
from Components.Label import Label
from Components.Button import Button
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.Harddisk import harddiskmanager
from Components.PluginComponent import plugins
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Plugins.Plugin import PluginDescriptor
import os
import sys
from enigma import *
from Screens.MessageBox import MessageBox
from Components.config import config, ConfigSubsection, ConfigText, ConfigYesNo
from time import *
import gettext
try:
    cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/SettingsSatDreamGr/po', [config.osd.language.getText()])
    _ = cat.gettext
except IOError:
    pass

config.settingsloader = ConfigSubsection()
config.settingsloader.keepterrestrial = ConfigYesNo(False)
config.settingsloader.keepsatellitesxml = ConfigYesNo(False)
config.settingsloader.keepcablesxml = ConfigYesNo(False)
config.settingsloader.keepterrestrialxml = ConfigYesNo(False)
config.settingsloader.keepbouquets = ConfigText('', False)

def main(session, **kwargs):
    try:
        session.open(SDG_Menu)
    except:
        print '[Settings] Pluginexecution failed'


def autostart(reason, **kwargs):
    if reason == 0:
        print '[PluginMenu] no autostart'


def menu(menuid, **kwargs):
    if menuid == 'cam':
        return [(_('Settings E2'),
          main,
          'settings_setup',
          45)]
    return []


def Plugins(**kwargs):
    return PluginDescriptor(name=_('Settings E2'), description=_('Morpheus,Vhannibal,Cyrus'), where=PluginDescriptor.WHERE_MENU, fnc=menu)


sdg_main = '<screen name="SDG_Menu" position="center,center" size="600,405" title="Settings E2" >\n\t\t<widget source="list" render="Listbox" position="20,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" >\n\t\t<convert type="TemplatedMultiContent">\n\t\t{"template": [\n\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t\t\t</widget>\n                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/exit_key.png" position="80,360" size="40,32" zPosition="1" alphatest="blend"/>\n                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/key_ok.png" position="240,360" size="40,32" zPosition="1" alphatest="blend"/>\n                   <widget name="exit_key" position="110,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />\n                   <widget name="key_ok" position="270,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />\n                   </screen>'

class SDG_Menu(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = sdg_main
        self.session = session
        self.drawList = []
        self.setup_title = _('Settings E2')
        self.onLayoutFinish.append(self.layoutFinished)
        self['list'] = List()
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)
        self.refresh()

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='%s/images/%s' % (os.path.dirname(sys.modules[__name__].__file__), image))
        return (pixmap, description)

    def refresh(self):
        self.drawList = []
        self.drawList.append(self.buildListEntry(_('Morpheus883 settings'), 'morphd.png'))
        self.drawList.append(self.buildListEntry(_('Vhannibal settings'), 'Vhannibal.png'))
        self.drawList.append(self.buildListEntry(_('Cyrus settings'), 'downloads.png'))
        self['list'].setList(self.drawList)

    def openSelected(self):
        index = self['list'].getIndex()
        if index == 0:
            SDG_MorpheusHelper(self.session).load()
        elif index == 1:
            SDG_VhannibalHelper(self.session).load()
        elif index == 2:
            SDG_SatdreamgrHelper(self.session).load()

    def quit(self):
        self.close()

    def layoutFinished(self):
        self.setTitle(self.setup_title)
