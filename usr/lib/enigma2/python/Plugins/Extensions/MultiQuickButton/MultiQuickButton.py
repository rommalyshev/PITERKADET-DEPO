# -*- coding: utf-8 -*-

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.PluginComponent import plugins
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigLocations, ConfigText, ConfigSelection, getConfigListEntry, ConfigInteger, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Sources.List import List
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.LocationBox import LocationBox
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop
from QuickButtonList import QuickButtonList, QuickButtonListEntry
from QuickButtonXML import QuickButtonXML
from enigma import getDesktop
from Tools.Directories import *
import xml.sax.xmlreader
import keymapparser
import os
from os import path, chmod
from __init__ import _

functionfile = "/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/mqbfunctions.xml"
macrofile = "/etc/MultiQuickButton/mqb_macro.cfg"
config.plugins.QuickButton = ConfigSubsection()
config.plugins.QuickButton.enable = ConfigYesNo(default = True)
config.plugins.QuickButton.info = ConfigYesNo(default = True)
config.plugins.QuickButton.okexitstate = ConfigYesNo(default = False)
config.plugins.QuickButton.mainmenu = ConfigYesNo(default = True)
config.plugins.QuickButton.last_backupdir = ConfigText(default=resolveFilename(SCOPE_SYSETC))
config.plugins.QuickButton.backupdirs = ConfigLocations(default=[resolveFilename(SCOPE_SYSETC)])
MultiQuickButton_version = "2.7.13"
autostart=_("Autostart") + ": "
menuentry=_("Main menu") + ": "
info=_("Info") + ": "
okexit=_("OK/EXIT") + ": "

values = ("red","red_long","green","green_long","yellow","yellow_long","blue","blue_long","pvr","pvr_long","radio","radio_long","text","text_long", \
			"help_long","info","info_long","end","end_long","home","home_long","cross_up","cross_down","cross_left","cross_right","previous","next", \
			"channelup","channeldown","audio","ok","exit","play","pause","fastforward","stop","rewind","tv", "subtitle", \
			"mqb_voldown", "mqb_volup", "mqb_mute", "mqb_power", "mqb_power_long")

class MultiQuickButton(Screen):

	global HD_Res

	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720

	if sz_w == 1280:
		HD_Res = True
	else:
		HD_Res = False

	if HD_Res:
		skin = """
		<screen position="240,100" size="800,520" title="MultiQuickButton Panel %s" >
			<widget name="list" position="10,10" size="780,410" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="20,450" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="210,450" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_yellow.png" zPosition="2" position="420,450" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_blue.png" zPosition="2" position="610,450" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/key_0.png" zPosition="2" position="15,490" size="35,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/key_1.png" zPosition="2" position="205,490" size="35,25" alphatest="on" />
			<widget name="key_red" backgroundColor="#1f771f" zPosition="2" position="50,445" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_green" backgroundColor="#1f771f" position="240,445" zPosition="2" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_yellow" backgroundColor="#1f771f" position="450,445" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_blue" backgroundColor="#1f771f" position="640,445" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_0" backgroundColor="#1f771f" zPosition="2" position="50,484" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_1" backgroundColor="#1f771f" position="240,484" zPosition="2" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_2" backgroundColor="#1f771f" position="450,484" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_3" backgroundColor="#1f771f" position="640,484" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="background" backgroundColor="#220a0a0a" zPosition="1" position="0,450" size="800,80" font="Regular;20" halign="left" valign="center" />
		</screen>""" % (MultiQuickButton_version)
	else:
		skin = """
		<screen position="50,190" size="620,320" title="MultiQuickButton Panel %s" >
			<widget name="list" position="10,10" size="600,210" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="10,250" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="160,250" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_yellow.png" zPosition="2" position="330,250" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_blue.png" zPosition="2" position="490,250" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/key_0.png" zPosition="2" position="6,290" size="35,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/key_1.png" zPosition="2" position="156,290" size="35,25" alphatest="on" />
			<widget name="key_red" backgroundColor="#1f771f" zPosition="2" position="35,245" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_green" backgroundColor="#1f771f" position="185,245" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_yellow" backgroundColor="#1f771f" position="355,245" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_blue" backgroundColor="#1f771f" position="515,245" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_0" backgroundColor="#1f771f" position="35,285" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_1" backgroundColor="#1f771f" position="185,285" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_2" backgroundColor="#1f771f" position="355,285" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_3" backgroundColor="#1f771f" position="515,285" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="background" backgroundColor="#220a0a0a" zPosition="1" position="0,320" size="620,80" font="Regular;20" halign="left" valign="center" />
		</screen>""" % (MultiQuickButton_version)

	def __init__(self, session, args=None):
		Screen.__init__(self, session)
		self.session = session
		self.menu = args
		self.settigspath = ""
		

		self["background"] = Label('')
		self["key_red"] = Label(autostart)
		self["key_green"] = Label(menuentry)
		self["key_yellow"] = Label(_("Restore"))
		self["key_blue"] = Label(_("Backup"))
		self["key_0"] = Label(info)
		self["key_1"] = Label(okexit)
		self["key_2"] = Label("")
		self["key_3"] = Label("")
		self.createList()
		self["list"] = QuickButtonList(list=self.list, selection = 0)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "NumberActions", "EPGSelectActions"],
		{
			"ok": self.run,
			"cancel": self.close,
			"red": self.autostart,
			"green": self.setMainMenu,
			"yellow": self.restore,
			"blue": self.backup,
			"0": self.setInfo,
			"1": self.toggleOkExit,
			"info": self.showAbout,
		}, -1)
		self.onShown.append(self.updateSettings)
		
	def createList(self):
		self.a = None
		for button in values:
			if config.plugins.QuickButton.info.value:
				try:
					functionbutton = " ["
					path = "/etc/MultiQuickButton/quickbutton_" + button + ".xml"
					menu = xml.dom.minidom.parse(path)
					self.XML_db = QuickButtonXML(menu)
					for a in self.XML_db.getMenu():
						if a[1] == "1":
							if functionbutton == " [":
								functionbutton = _(a[0])
							else:
								functionbutton = functionbutton + " | " + _(a[0])
					if functionbutton == " [":
						space1 = " "
						space2 = " "
						functionbutton = " "
					else:
						space1 = " ["
						space2 = "]"
					globals()['functionbutton_%s' % button] = space1 + functionbutton + space2
					
				except Exception, a:
					self.a = a
			else:
				globals()['functionbutton_%s' % button] = " "
		self.list = []
		self.list.append(QuickButtonListEntry('',(_('red') + functionbutton_red, 'red')))
		self.list.append(QuickButtonListEntry('',((_('red') + _(' long')) + functionbutton_red_long, 'red_long')))
		self.list.append(QuickButtonListEntry('',(_('green') + functionbutton_green, 'green')))
		self.list.append(QuickButtonListEntry('',((_('green') + _(' long')) + functionbutton_green_long, 'green_long')))
		self.list.append(QuickButtonListEntry('',(_('yellow') + functionbutton_yellow, 'yellow')))
		self.list.append(QuickButtonListEntry('',((_('yellow') + _(' long')) + functionbutton_yellow_long, 'yellow_long')))
		self.list.append(QuickButtonListEntry('',(_('blue') + functionbutton_blue, 'blue')))
		self.list.append(QuickButtonListEntry('',((_('blue') + _(' long')) + functionbutton_blue_long, 'blue_long')))
		self.list.append(QuickButtonListEntry('',(_('TEXT') + functionbutton_text, 'text')))
		self.list.append(QuickButtonListEntry('',((_('TEXT') + _(' long')) + functionbutton_text_long, 'text_long')))
		self.list.append(QuickButtonListEntry('',((_('HELP') + _(' long')) + functionbutton_help_long, 'help_long')))
		self.list.append(QuickButtonListEntry('',(_('VU+ EPG / INFO') + functionbutton_info, 'info')))
		self.list.append(QuickButtonListEntry('',((_('VU+ EPG / INFO') + _(' long')) + functionbutton_info_long, 'info_long')))
		self.list.append(QuickButtonListEntry('',(_('HOME') + functionbutton_home, 'home')))
		self.list.append(QuickButtonListEntry('',((_('HOME') + _(' long')) + functionbutton_home_long, 'home_long')))
		self.list.append(QuickButtonListEntry('',(_('END') + functionbutton_end, 'end')))
		self.list.append(QuickButtonListEntry('',((_('END') + _(' long')) + functionbutton_end_long, 'end_long')))
		self.list.append(QuickButtonListEntry('',(_('Subtitle') + functionbutton_subtitle, 'subtitle')))
		self.list.append(QuickButtonListEntry('',(_('VU+ R-Button') + functionbutton_pvr, 'pvr')))
		self.list.append(QuickButtonListEntry('',((_('VU+ R-Button') + _(' long')) + functionbutton_pvr_long, 'pvr_long')))
		self.list.append(QuickButtonListEntry('',(_('RADIO') + functionbutton_radio, 'radio')))
		self.list.append(QuickButtonListEntry('',((_('RADIO') + _(' long')) + functionbutton_radio_long, 'radio_long')))
		self.list.append(QuickButtonListEntry('',(_('TV') + functionbutton_tv, 'tv')))
		self.list.append(QuickButtonListEntry('',(_('Cross Up') + functionbutton_cross_up, 'cross_up')))
		self.list.append(QuickButtonListEntry('',(_('Cross Down') + functionbutton_cross_down, 'cross_down')))
		self.list.append(QuickButtonListEntry('',(_('Cross Left') + functionbutton_cross_left, 'cross_left')))
		self.list.append(QuickButtonListEntry('',(_('Cross Right') + functionbutton_cross_right, 'cross_right')))
		self.list.append(QuickButtonListEntry('',(_('Channel +') + functionbutton_channelup, 'channelup')))
		self.list.append(QuickButtonListEntry('',(_('Channel -') + functionbutton_channeldown, 'channeldown')))
		self.list.append(QuickButtonListEntry('',(_('Forward >') + functionbutton_next, 'next')))
		self.list.append(QuickButtonListEntry('',(_('Backward <') + functionbutton_previous, 'previous')))
		self.list.append(QuickButtonListEntry('',(_('Volume +') + functionbutton_mqb_volup, 'mqb_volup')))
		self.list.append(QuickButtonListEntry('',(_('Volume -') + functionbutton_mqb_voldown, 'mqb_voldown')))
		self.list.append(QuickButtonListEntry('',(_('Mute') + functionbutton_mqb_mute, 'mqb_mute')))
		self.list.append(QuickButtonListEntry('',(_('Power') + functionbutton_mqb_power, 'mqb_power')))
		self.list.append(QuickButtonListEntry('',((_('Power') + _(' long')) + functionbutton_mqb_power_long, 'mqb_power_long')))
		self.list.append(QuickButtonListEntry('',(_('Audio') + functionbutton_audio, 'audio')))
		if config.plugins.QuickButton.okexitstate.value:
			self.list.append(QuickButtonListEntry('',('OK' + functionbutton_ok, 'ok')))
			self.list.append(QuickButtonListEntry('',(_('EXIT') + functionbutton_exit, 'exit')))
		self.list.append(QuickButtonListEntry('',(_('Play') + functionbutton_play, 'play')))
		self.list.append(QuickButtonListEntry('',(_('Pause') + functionbutton_pause, 'pause')))
		self.list.append(QuickButtonListEntry('',(_('Stop') + functionbutton_stop, 'stop')))
		self.list.append(QuickButtonListEntry('',(_('Rewind <<') + functionbutton_rewind, 'rewind')))
		self.list.append(QuickButtonListEntry('',(_('FastForward >>') + functionbutton_fastforward, 'fastforward')))
		
	def updateList(self):
		self.createList()
		self["list"].l.setList(self.list)

	def updateSettings(self):
		autostart_state = autostart
		menuentry_state = menuentry
		info_state = info
		okexit_state = okexit
		if config.plugins.QuickButton.enable.value:
			autostart_state += _("on")
		else:
			autostart_state += _("off")

		if config.plugins.QuickButton.mainmenu.value:
			menuentry_state += _("on")
		else:
			menuentry_state += _("off")

		if config.plugins.QuickButton.info.value:
			info_state += _("on")
		else:
			info_state += _("off")

		if config.plugins.QuickButton.okexitstate.value:
			okexit_state += _("on")
		else:
			okexit_state += _("off")

		self["key_red"].setText(autostart_state)
		self["key_green"].setText(menuentry_state)
		self["key_0"].setText(info_state)
		self["key_1"].setText(okexit_state)

	def run(self):
		returnValue = self["list"].l.getCurrentSelection()[0][1]
		title = self["list"].l.getCurrentSelection()[0][0]
		if returnValue is not None:
			if returnValue in values:
				path = '/etc/MultiQuickButton/quickbutton_' + returnValue + '.xml'
				if os.path.exists(path) is True:
					self.session.openWithCallback(self.updateAfterButtonChange, QuickButton, path, (_("Quickbutton Key : %s") % title))
				else:
					self.session.open(MessageBox,("file %s not found!" % (path)),  MessageBox.TYPE_ERROR)

	def updateAfterButtonChange(self, res = None):
		self.updateList()

	def backup(self):
		self.session.openWithCallback(
			self.callBackup,
			BackupLocationBox,
			_("Please select the backup path..."),
			"",
			config.plugins.QuickButton.last_backupdir.value
		)

	def callBackup(self, path):
		if path is not None:
			if pathExists(path):
				config.plugins.QuickButton.last_backupdir.value = path
				config.plugins.QuickButton.last_backupdir.save()
				self.settigspath = path + "MultiQuickButton_settings.tar.gz"
				if fileExists(self.settigspath):
					self.session.openWithCallback(self.callOverwriteBackup, MessageBox,_("Overwrite existing Backup?."),type = MessageBox.TYPE_YESNO,)
				else:
					com = "tar czvf %s /etc/MultiQuickButton/" % (self.settigspath)
					self.session.open(Console,_("Backup Settings..."),[com])
			else:
				self.session.open(
					MessageBox,
					_("Directory %s nonexistent.") % (path),
					type = MessageBox.TYPE_ERROR,
					timeout = 5
					)

	def callOverwriteBackup(self, res):
		if res:
			com = "tar czvf %s /etc/MultiQuickButton/" % (self.settigspath)
			self.session.open(Console,_("Backup Settings..."),[com])

	def restore(self):
		self.session.openWithCallback(
			self.callRestore,
			BackupLocationBox,
			_("Please select the restore path..."),
			"",
			config.plugins.QuickButton.last_backupdir.value
		)

	def callRestore(self, path):
		if path is not None:
			self.settigspath = path + "MultiQuickButton_settings.tar.gz"
			if fileExists(self.settigspath):
				self.session.openWithCallback(self.callOverwriteSettings, MessageBox,_("Overwrite existing Settings?."),type = MessageBox.TYPE_YESNO,)
			else:
				self.session.open(MessageBox,_("File %s nonexistent.") % (path),type = MessageBox.TYPE_ERROR,timeout = 5)
		else:
			pass

	def callOverwriteSettings(self, res):
		if res:
			com = "cd /; tar xzvf %s" % (self.settigspath)
			self.session.open(Console,_("Restore Settings..."),[com])

	def autostart(self):
		if config.plugins.QuickButton.enable.value:
			config.plugins.QuickButton.enable.setValue(False)
			config.plugins.QuickButton.mainmenu.setValue(False)
		else:
			config.plugins.QuickButton.enable.setValue(True)

		self.updateSettings()
		config.plugins.QuickButton.enable.save()
		self.session.openWithCallback(self.callRestart,MessageBox,_("Restarting Enigma2 to set\nMulti QuickButton Autostart"), MessageBox.TYPE_YESNO, timeout=10)

	def setMainMenu(self):
		if config.plugins.QuickButton.mainmenu.value:
			config.plugins.QuickButton.mainmenu.setValue(False)
		else:
			config.plugins.QuickButton.mainmenu.setValue(True)

		config.plugins.QuickButton.mainmenu.save()
		self.updateSettings()
		self.session.openWithCallback(self.callRestart,MessageBox,_("Restarting Enigma2 to load:\n") + _("Main menu") + _("Multi QuickButton settings"), MessageBox.TYPE_YESNO, timeout=10)

	def setInfo(self):
		if config.plugins.QuickButton.info.value:
			config.plugins.QuickButton.info.setValue(False)
		else:
			config.plugins.QuickButton.info.setValue(True)

		config.plugins.QuickButton.info.save()
		self.updateList()
		self.updateSettings()

	def toggleOkExit(self):
		self.mqbkeymapfile = "/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/keymap.xml"
		self.mqbkeymap = open(self.mqbkeymapfile, "r")
		self.text = self.mqbkeymap.read()
		self.mqbkeymap.close()
		self.keys = [	"<key id=\"KEY_OK\" mapto=\"ok\" flags=\"m\" />", \
				"<key id=\"KEY_EXIT\" mapto=\"exit\" flags=\"m\" />" ]

		if config.plugins.QuickButton.okexitstate.value:
			config.plugins.QuickButton.okexitstate.setValue(False)
			for self.key in self.keys:
				self.keyinactive = "<!-- " + self.key + " -->"
				if not self.keyinactive in self.text:
					self.text = self.text.replace(self.key, self.keyinactive)
		else:
			config.plugins.QuickButton.okexitstate.setValue(True)
			for self.key in self.keys:
				self.keyinactive = "<!-- " + self.key + " -->"
				if self.keyinactive in self.text:
					self.text = self.text.replace(self.keyinactive, self.key)

		self.mqbkeymap = open(self.mqbkeymapfile, "w")
		self.mqbkeymap.write(self.text)
		self.mqbkeymap.close()
		keymapparser.removeKeymap(self.mqbkeymapfile)
		keymapparser.readKeymap(self.mqbkeymapfile)
		config.plugins.QuickButton.okexitstate.save()
		self.updateList()
		self.updateSettings()

	def showAbout(self):
		self.session.open(MessageBox,("Multi Quickbutton idea is based on\nGP2\'s Quickbutton\nVersion: 2.7\nby Emanuel CLI-Team 2009\nwww.cablelinux.info\n ***special thanks*** to:\ngutemine & AliAbdul & Dr.Best ;-)\n\nChanges for VU+ by plnick\nplnick@vuplus-support.org\nwww.vuplus-support.org\nVersion %s" % (MultiQuickButton_version)),  MessageBox.TYPE_INFO)
  
	def callRestart(self, restart):
		if restart == True:
			self.session.open(TryQuitMainloop, 3)
		else:
			pass

class BackupLocationBox(LocationBox):
	def __init__(self, session, text, filename, dir, minFree = None):
		inhibitDirs = ["/bin", "/boot", "/dev", "/lib", "/proc", "/sbin", "/sys", "/usr", "/var"]
		LocationBox.__init__(self, session, text = text, filename = filename, currDir = dir, bookmarks = config.plugins.QuickButton.backupdirs, autoAdd = True, editDir = True, inhibitDirs = inhibitDirs, minFree = minFree)
		self.skinName = "LocationBox"

class QuickButton(Screen):

	global HD_Res

	try:
		sz_w = getDesktop(0).size().width()
	except:
		sz_w = 720

	if sz_w == 1280:
		HD_Res = True
	else:
		HD_Res = False

	if HD_Res:
		skin = """
		<screen position="240,100" size="800,520" title="QuickButton" >
			<widget name="list" position="10,10" size="780,450" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="15,487" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="205,487" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_yellow.png" zPosition="2" position="395,487" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_blue.png" zPosition="2" position="585,487" size="25,25" alphatest="on" />
			<widget name="key_red" backgroundColor="#1f771f" zPosition="2" position="50,480" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_green" backgroundColor="#1f771f" position="240,480" zPosition="2" size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_yellow" backgroundColor="#1f771f" position="430,480" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_blue" backgroundColor="#1f771f" position="620,480" zPosition="2"  size="180,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="background" backgroundColor="#220a0a0a" zPosition="1" position="0,480" size="800,40" font="Regular;20" halign="left" valign="center" />
		</screen>"""
	else:
		skin = """
		<screen position="60,90" size="600,420" title="QuickButton" >
			<widget name="list" position="10,10" size="580,350" scrollbarMode="showOnDemand" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="15,387" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="155,387" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_yellow.png" zPosition="2" position="295,387" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_blue.png" zPosition="2" position="435,387" size="25,25" alphatest="on" />
			<widget name="key_red" backgroundColor="#1f771f" zPosition="2" position="40,380" size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_green" backgroundColor="#1f771f" position="180,380" zPosition="2" size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_yellow" backgroundColor="#1f771f" position="320,380" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="key_blue" backgroundColor="#1f771f" position="460,380" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="background" backgroundColor="#220a0a0a" zPosition="1" position="0,380" size="600,40" font="Regular;20" halign="left" valign="center" />
		</screen>"""

	def __init__(self, session, path=None, title = "" ):
		Screen.__init__(self, session)
		self.session = session
		self.path = path
		self.newtitle = title
		self.changed = False
		self.e = None
		list = []
		try:
			menu = xml.dom.minidom.parse(self.path)
			self.XML_db = QuickButtonXML(menu)
			for e in self.XML_db.getMenu():
				if e[1] == "1":
					list.append(QuickButtonListEntry('green',(_(e[0]),e[0], '1')))
					
				else:
					list.append(QuickButtonListEntry('red',(_(e[0]),e[0], '')))
					
		except Exception, e:
			self.e = e
			list = []

		self["list"] = QuickButtonList(list=list, selection = 0)
		self["background"] = Label('')
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Save"))
		self["key_yellow"] = Label(_("delete"))
		self["key_blue"] = Label(_("Add"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.run,
			"cancel": self.cancel,
			"red": self.close,
			"green": self.save,
			"yellow": self.delete,
			"blue": self.add,
			"up": self.up,
			"down": self.down,
			"left": self.keyLeft,
			"right": self.keyRight
		}, -1)
		self.onExecBegin.append(self.error)
		self.onShown.append(self.updateTitle)

	def error(self):
		if self.e:
			self.session.open(MessageBox,("XML " + _("Error") + ": %s" % self.e),  MessageBox.TYPE_ERROR)
			self.close(None)

			
	def updateTitle(self):
		self.setTitle(self.newtitle)

	def run(self):
		returnValue = self["list"].l.getCurrentSelection()[0][2]
		name = self["list"].l.getCurrentSelection()[0][1]
		self.changed = True
		if returnValue is not None:
			idx = 0;
			if returnValue is "1":
				list = []
				self.XML_db.setSelection(name, "")
				for e in self.XML_db.getMenu():
					if e[1] == "1":
						list.append(QuickButtonListEntry('green',(_(e[0]),e[0], '1')))
						idx += 1
					else:
						list.append(QuickButtonListEntry('red',(_(e[0]),e[0], '')))

			else:
				list = []
				self.XML_db.setSelection(name, "1")
				for e in self.XML_db.getMenu():
					if e[1] == "1":
						list.append(QuickButtonListEntry('green',(_(e[0]),e[0], '1')))
						idx += 1
					else:
						list.append(QuickButtonListEntry('red',(_(e[0]),e[0], '')))

			self["list"].setList(list)

	def save(self):
		self.XML_db.saveMenu(self.path)
		self.changed = False
		self.cancel()

	def keyLeft(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.pageUp)
				if self["list"].l.getCurrentSelection()[0][1] != "--" or self["list"].l.getCurrentSelectionIndex() == 0:
					break

	def keyRight(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.pageDown)
				if self["list"].l.getCurrentSelection()[0][1] != "--" or self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1:
					break

	def up(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveUp)
				if self["list"].l.getCurrentSelection()[0][1] != "--" or self["list"].l.getCurrentSelectionIndex() == 0:
					break

	def down(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveDown)
				if self["list"].l.getCurrentSelection()[0][1] != "--" or self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1:
					break

	def getPluginsList(self):
		unic = []
		twins = [""]
		pluginlist = plugins.getPlugins([PluginDescriptor.WHERE_PLUGINMENU ,PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_EVENTINFO])
		pluginlist.sort(key = lambda p: p.name)
		for plugin in pluginlist:
			if plugin.name in twins:
				pass 
			else:
				unic.append((_(plugin.name), plugin.name, "plugins", ""))
				twins.append(plugin.name)
		return unic

	def getFunctionList(self):
		unic = []
		mqbfunctionfile = functionfile
		self.mqbfunctions = xml.dom.minidom.parse(mqbfunctionfile)
		for mqbfunction in self.mqbfunctions.getElementsByTagName("mqbfunction"):
			functionname = str(mqbfunction.getElementsByTagName("name")[0].childNodes[0].data)
			unic.append((_(functionname),functionname, "functions" ""))
		return unic

	def add(self):
		self.changed = True
		self.session.openWithCallback(self.setNewEntryType,ChoiceBox,_("MQB Functions and Plugins") ,self.getNewEntryType())

	def setNewEntryType(self, selection):
		if selection:
			if selection[1] == "functions":
				self.addfunction()
			elif selection[1] == "plugins":
				self.addplugin()
			elif selection[1] == "macros":
				self.addmacro()
			else:
				self.session.open(MessageBox,_("No valid selection"), type = MessageBox.TYPE_ERROR,timeout = 5)

	def getNewEntryType(self):
		entrytype = []
		entrytype.append((_("Add Functions to MQB Key"),"functions"))
		entrytype.append((_("Add Plugins to MQB Key"),"plugins"))
		entrytype.append((_("Add Macro to MQB Key"),"macros"))
		return entrytype

	def addfunction(self):
		self.changed = True
		try:
			self.session.openWithCallback(self.QuickPluginSelected,ChoiceBox,_("Functions") ,self.getFunctionList())
		except Exception,e:
			self.session.open(MessageBox,_("No valid function file found"), type = MessageBox.TYPE_ERROR,timeout = 5)

	def addplugin(self):
		self.changed = True
		self.session.openWithCallback(self.QuickPluginSelected,ChoiceBox,_("Plugins") ,self.getPluginsList())

	def addmacro(self):
		self.changed = True
		self.session.openWithCallback(self.QuickPluginSelected, MultiQuickButtonMacro)
		
	def QuickPluginSelected(self, choice):
		if choice:
			for entry in self["list"].list:
				if entry[0][0] == choice[0]:
					self.session.open(MessageBox,_("Entry %s already exists.") % (entry[0][0]),type = MessageBox.TYPE_ERROR,timeout = 5)
					return
			if choice[2] == "plugins":
				self.XML_db.addPluginEntry(choice[1])
			elif choice[2] == "functions":
				self.XML_db.addFunctionEntry(choice[1])
			elif choice[2] == "macros":
				self.XML_db.addMacroEntry(choice)
			else:
				return
			list = []
			for newEntry in self.XML_db.getMenu():
				if newEntry[1] == "1":
					list.append(QuickButtonListEntry('green',(_(newEntry[0]), _(newEntry[0]), '1')))
				else:
					list.append(QuickButtonListEntry('red',(_(newEntry[0]), _(newEntry[0]), '')))
					
			self["list"].setList(list)
			if len(self["list"].list) > 0:
				while 1:
					self["list"].instance.moveSelection(self["list"].instance.moveDown)
					if self["list"].l.getCurrentSelection()[0][1] != '--' or self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1:
						break

	def delete(self):
		self.changed = True
		name = self["list"].l.getCurrentSelection()[0][1]
		if name and name <> "--":
			self.XML_db.rmEntry(name)

			list = []
			for e in self.XML_db.getMenu():
				if e[1] == "1":
					list.append(QuickButtonListEntry('green',(_(e[0]),e[0], '1')))
				else:
					list.append(QuickButtonListEntry('red',(_(e[0]),e[0], '')))

			lastValue="--"
			tmplist = []
			for i in list:
				if i[0][1] == "--" and lastValue == "--":
					lastValue = ""
				else:
					tmplist.append(i)
					lastValue = i[0][1]
			list = tmplist
			self["list"].setList(list)

	def cancel(self):
		if self.changed is True:
			self.session.openWithCallback(self.callForSaveValue,MessageBox,_("Save Settings"), MessageBox.TYPE_YESNO)
		else:
			self.close(None)

	def callForSaveValue(self, result):
		if result is True:
			self.save()
			self.close(None)
		else:
			self.close(None)


class MultiQuickButtonMacro(Screen):
	skin = """
		<screen position="center,center" size="640,400" title="MultiQuickButton macro configuration" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="10,350" size="25,25" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="160,350" size="25,25" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_yellow.png" zPosition="2" position="330,350" size="25,25" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_blue.png" zPosition="2" position="490,350" size="25,25" alphatest="on" />
		<widget name="buttonred" backgroundColor="#1f771f" position="35,343" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
		<widget name="buttongreen" backgroundColor="#1f771f" position="185,343" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
		<widget name="buttonyellow" backgroundColor="#1f771f" position="355,343" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
		<widget name="buttonblue" backgroundColor="#1f771f" position="515,343" zPosition="2"  size="150,40" font="Regular;20" halign="left" valign="center" transparent="1" />
		<widget source="menu" render="Listbox" position="10,50" size="600,285" scrollbarMode="showOnDemand" enableWrapAround="1" >
			<convert type="TemplatedMultiContent" transparent="0">
				{"template": [
						MultiContentEntryText(pos = (5, 2), size = (600, 20), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
					],
				"fonts": [gFont("Regular", 22)],
				"itemHeight": 26
				}
			</convert>
		</widget>
		</screen>"""

	def __init__(self, session, args = 0):
		self.session = session
		Screen.__init__(self, session)
		
		self.title=_("MultiQuickButton macro configuration")
		try:
			self["title"]=StaticText(self.title)
		except:
			print 'self["title"] was not found in skin'
		
		self.list = self.readConfig()
		self["menu"] = List(self.list)
		
		self["buttonred"] = Label(_("Name"))
		self["buttongreen"] = Label(_("Modify"))
		self["buttonyellow"] = Label(_("Delete"))
		self["buttonblue"] = Label(_("Add"))
		self["setupActions"] = ActionMap(["ColorActions", "SetupActions",],
			{
				"green": self.save,
				"red": self.keyRed,
				"blue": self.addButton,
				"yellow": self.removeButton,
				"cancel": self.keyCancel,
				"ok": self.keyOk,
			}, -2)
		self.selectmacro = True
		self.configmacro = False
		self.addkey = False
		
		self.buttondic = {
					"011" : "0",
					"002" : "1",
					"003" : "2",
					"004" : "3",
					"005" : "4",
					"006" : "5",
					"007" : "6",
					"008" : "7",
					"009" : "8",
					"010" : "9",
					"116" : _("Power"),
					"139" : _("Menu"),
					"402" : _("Channel +"),
					"403" : _("Channel -"),
					"358" : _("VU+ EPG / Info"),
					"352" : _("OK"),
					"105" : _("Cross Left"),
					"106" : _("Cross Right"),
					"103" : _("Cross Up"),
					"108" : _("Cross Down"),
					"174" : _("EXIT"),
					"398" : _("red"),
					"401" : _("blue"),
					"399" : _("green"),
					"400" : _("yellow"),
					"207" : _("Play"),
					"119" : _("Pause"),
					"128" : _("Stop"),
					"167" : _("Record"),
					"208" : _("FastForward >>"),
					"168" : _("Rewind <<"),
					"107" : _("END"),
					"102" : _("HOME"),
					"392" : _("Audio"),
					"370" : _("Subtitle"),
					"168" : _("Rewind <<"),
					"388" : _("TEXT"),
					"377" : _("TV"),
					"385" : _("RADIO"),
					"393" : _("VU+ R-Button"),
					"138" : _("HELP"),
					"115" : _("Volume +"),
					"114" : _("Volume -"),
					"113" : _("Mute"),
					"407" : _("Forward >"),
					"412" : _("Backward <"),
					"P100" : (_("Pause") + " 0.1 sec"),
					"P500" : (_("Pause") + " 0.5 sec"),
					"P1000" : (_("Pause") + " 1.0 sec")
				}

	def readConfig(self):
		config_list = []
		if not os.path.exists(macrofile):
			system("touch %s" % macrofile)
			os.chmod(macrofile, 0644)
		content = open(macrofile).readlines()
		for line in content:
			line = line.strip().split(":")
			if len(line) == 2:
				config_list.append((line[0], line[1]))
		return config_list

	def writeConfig(self):
		text = ""
		if len(self.list):
			for button in self.list:
				if len(button) == 2:
					text += "%s:%s\n" % (str(button[0]), str(button[1]))
		f = open(macrofile, "w")
		f.write(text)
		f.close()

	def changeMacroName(self, ret = None):
		if ret and ret[0]:
			idx = ret[1]
			cur_old = self.list[idx]
			self.list[idx] = (str(ret[0]), cur_old[1])

	def keyOk(self):
		cur = self["menu"].getCurrent()
		if cur:
			self["buttonred"].setText(_("Cancel"))
			self["buttongreen"].setText(_("Save"))
			self["buttonyellow"].setText(_("Delete"))
			self["buttonblue"].setText(_("Add"))
			if self.configmacro == False and self.selectmacro == True:
				self.writeConfig()
				cur_macro = self["menu"].getCurrent()
				ret = (cur_macro[0], cur_macro[1], "macros")
				self.close(ret)
			elif self.configmacro == True and self.selectmacro == False and self.addkey == True:
				self.addkey = False
				self.macrolist.insert(self.new_key_idx, cur)
				idx = len(self.macrolist) -1
				self["menu"].setList(self.macrolist)
				self['menu'].setIndex(self.new_key_idx)

	def addButton(self):
		if self.configmacro == True and self.selectmacro == False  and self.addkey == False:
			if len(self.macrolist):
				self.new_key_idx = self["menu"].getIndex() + 1
			else:
				self.new_key_idx = 0
			self["buttonred"].setText(_("Cancel"))
			self["buttongreen"].setText(_("Ok"))
			self["buttonyellow"].setText("")
			self["buttonblue"].setText("")
			self.addkey = True
			self.buttonlist =[]
			for key in sorted(self.buttondic.iterkeys()):
				if key.startswith('P'):
					self.buttonlist.append(("--- " + self.buttondic[key] + " ---", key))
				else:
					self.buttonlist.append((_("Button : ") + self.buttondic[key], key))
			self["menu"].setList(self.buttonlist)
		elif self.selectmacro == True:
			number = len(self.list) + 1
			idx = self["menu"].getIndex() + 1
			self.list.insert(idx, ("Macro %d" % number,""))
			if len(self.list) == 1:
				idx = 0
			self['menu'].setList(self.list)
			self['menu'].setIndex(idx)

	def removeButton(self):
		if self.configmacro == True and self.selectmacro == False  and self.addkey == False:
			# hm, why we have to recreate the list if we remove entries which exists twice in the list ???
			curidx = self["menu"].getIndex()
			idx = -1
			new_macrolist = []
			for entry in self.macrolist:
				idx += 1
				if idx != curidx:
					new_macrolist.append(entry)
			self.macrolist = new_macrolist
			self['menu'].setList(self.macrolist)
			if len(self.macrolist) == curidx:
				self['menu'].setIndex(curidx - 1)
			else:
				self['menu'].setIndex(curidx)
		elif self.selectmacro == True:
			curidx = self["menu"].getIndex()
			idx = -1
			new_list = []
			for entry in self.list:
				idx += 1
				if idx != curidx:
					new_list.append(entry)
			self.list = new_list
			self['menu'].setList(self.list)
			if len(self.list) == curidx:
				self['menu'].setIndex(curidx - 1)
			else:
				self['menu'].setIndex(curidx)

	def save(self):
		if self.configmacro == True and self.selectmacro == False and self.addkey == False:
			self.selectmacro = True
			self.configmacro = False
			self.addkey = False
			self.new_config_value = ""
			for entry in self.macrolist:
				self.new_config_value = self.new_config_value + "," + entry[1]
			self.new_config_value = self.new_config_value.strip(",")
			i = self.current_macro
			macro = self.list[i][0]
			self.list[i] = (macro, self.new_config_value)
			self["buttonred"].setText(_("Name"))
			self["buttongreen"].setText(_("Modify"))
			self["menu"].setList(self.list)
			self.writeConfig()
		elif self.configmacro == False and self.selectmacro == True:
			if len(self.list):
				cur = self["menu"].getCurrent()
				self.selectmacro = False
				self.configmacro = True
				self.current_macro = self.list.index(cur)
				self.macrolist = []
				for key in cur[1].split(","):
					if key in self.buttondic:
						if key.startswith('P'):
							self.macrolist.append(("--- " + _(self.buttondic[key]) + " ---", key))
						else:
							self.macrolist.append((_("Button : ") + _(self.buttondic[key]), key))
				self["menu"].setList(self.macrolist)
				self["buttonred"].setText(_("Cancel"))
				self["buttongreen"].setText(_("Save"))

	def keyRed(self):
		if self.configmacro == False and self.selectmacro == True:
			cur = self["menu"].getCurrent()
			idx = self.list.index(cur)
			oldname = cur[0]
			self.session.openWithCallback(self.changeMacroName, InputMacroName, idx, oldname)
		
		elif self.configmacro == True and self.selectmacro == False and self.addkey == False:
			self.selectmacro = True
			self.configmacro = False
			self["buttonred"].setText(_("Name"))
			self["buttongreen"].setText(_("Modify"))
			self["buttonyellow"].setText(_("Delete"))
			self["buttonblue"].setText(_("Add"))
			self["menu"].setList(self.list)
		
		elif self.configmacro == True and self.selectmacro == False and self.addkey == True:
			self.addkey = False
			self["buttonred"].setText(_("Cancel"))
			self["buttongreen"].setText(_("Save"))
			self["buttonyellow"].setText(_("Delete"))
			self["buttonblue"].setText(_("Add"))
			self["menu"].setList(self.macrolist)

	def keyCancel(self):
		if self.configmacro == False and self.selectmacro == True:
			ret = None
			self.close(ret)
		else:
			self.keyRed()

class InputMacroName(Screen, ConfigListScreen):
	skin = """
		<screen name="InputMacroName" position="center,center" size="640,100" title="Input macro name" >
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_red.png" zPosition="2" position="10,50" size="25,25" alphatest="on" />
			<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/MultiQuickButton/pic/button_green.png" zPosition="2" position="160,50" size="25,25" alphatest="on" />
			<widget render="Label" source="key_red" backgroundColor="#1f771f" position="35,43" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget render="Label" source="key_green" backgroundColor="#1f771f" position="185,43" zPosition="2" size="250,40" font="Regular;20" halign="left" valign="center" transparent="1" />
			<widget name="config" zPosition="2" position="10,5" size="620,200" transparent="1" />
		</screen>
		"""

	def __init__(self, session, idx, oldname):
		Screen.__init__(self, session)
		self.title=_("Input name for MQB macro")
		try:
			self["title"]=StaticText(self.title)
		except:
			print 'self["title"] was not found in skin'
		self.listidx = idx
		self.macroname = NoSave(ConfigText(default = oldname, visible_width = 50, fixed_size = False))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Ok"))
		self["shortcuts"] = ActionMap(["SetupActions", "ColorActions", "InputActions"],
		{
			"ok": self.keyGo,
			"cancel": self.keyCancel,
			"red": self.keyCancel,
			"green": self.keyGo,
		}, -1)
		self.list = []
		ConfigListScreen.__init__(self, self.list,session = session)
		self.createSetup()

	def createSetup(self):
		self.list = []
		self.inputpanelpassword = getConfigListEntry(_("Input name for MQB macro : "), self.macroname)
		self.list.append(self.inputpanelpassword)
		self["config"].list = self.list
		self["config"].l.setList(self.list)

	def keyCancel(self):
		ret = None
		self.close((ret, self.listidx))

	def keyGo(self):
		ret = self.macroname.value
		self.close((ret, self.listidx))
