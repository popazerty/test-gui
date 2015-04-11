from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.config import getConfigListEntry, config
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from SDG_ActionBox import SDG_ActionBox
from SDG_Deflate import SDG_Deflate
from SDG_Settings import SDG_Settings
from SDG_SettingsList import SDG_SettingsList
from SDG_Common import TMP_IMPORT_PWD, TMP_SETTINGS_PWD
from urlparse import urlparse
import xml.etree.cElementTree
import httplib
import shutil
import os
import datetime
import gettext
try:
    cat = gettext.translation('lang', '/usr/lib/enigma2/python/Plugins/Satdreamgr/po', [config.osd.language.getText()])
    _ = cat.gettext
except IOError:
    pass

Vhannibal_HOST = 'sgcpm.com'
Vhannibal_PATH = '/enigma2/Vhannibal/'

class SDG_VhannibalHelper:

    def __init__(self, session):
        self.session = session

    def download(self):
        self.loaded = True
        self.list = []
        try:
            conn = httplib.HTTPConnection(Vhannibal_HOST)
            conn.request('GET', Vhannibal_PATH + 'lista.xml')
            httpres = conn.getresponse()
            if httpres.status == 200:
                mdom = xml.etree.cElementTree.parse(httpres)
                root = mdom.getroot()
                for node in root:
                    if node.tag == 'MAIN':
                        sat = ''
                        date = ''
                        url = ''
                        for x in node:
                            if x.tag == 'SAT':
                                sat = x.text
                            elif x.tag == 'DATE':
                                date = x.text
                            elif x.tag == 'URL':
                                url = x.text

                        self.list.append([sat, date, url])

            else:
                self.session.open(MessageBox, _('Cannot download Vhannibal list'), MessageBox.TYPE_ERROR)
                self.loaded = False
        except Exception as e:
            print e
            self.session.open(MessageBox, _('Cannot download Vhannibal list'), MessageBox.TYPE_ERROR)
            self.loaded = False

    def load(self):
        self.session.openWithCallback(self.show, SDG_ActionBox, _('Downloading Vhannibal list'), _('Downloading ...'), self.download)

    def show(self, ret = None):
        if self.loaded:
            self.session.open(SDG_Vhannibal, self.list)


vhannibal_main = '<screen name="SDG_Vhannibal" position="center,center" size="600,405" title="Vhannibal list" >\n\t\t\t<widget source="list" render="Listbox" position="10,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t\t{"template": [\n\t\t\t\t\t\tMultiContentEntryText(pos = (10, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 0),\n\t\t\t\t\t\tMultiContentEntryText(pos = (450, 5), size = (120, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t\t],\n\t\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t\t"itemHeight": 40\n\t\t\t\t\t}\n\t\t\t\t</convert>\n\t\t\t</widget>\t\n                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/exit_key.png" position="80,360" size="40,32" zPosition="1" alphatest="blend"/>\n                   <ePixmap pixmap="/usr/share/enigma2/Satdreamgr-HD/buttons/key_ok.png" position="240,360" size="40,32" zPosition="1" alphatest="blend"/>                   \n                   <widget name="exit_key" position="110,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />\n                   <widget name="key_ok" position="270,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />\n                   </screen>'

class SDG_Vhannibal(SDG_SettingsList):

    def __init__(self, session, list):
        SDG_SettingsList.__init__(self, session, list)
        self.skin = vhannibal_main
