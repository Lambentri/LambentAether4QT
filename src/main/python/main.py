from argparse import ArgumentParser
from datetime import datetime
from sys import argv
from functools import partial
from typing import Dict, List, Callable

from PyQt5 import QtCore, QtWidgets
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner
from autobahn.wamp import ApplicationError
from autobahn.wamp.types import PublishOptions
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QPainter, QColor, QIcon
from PyQt5.QtWidgets import qApp, QLabel, QHBoxLayout, QWidget, QSlider, QSpacerItem, QLineEdit, QPushButton, QDialog, \
    QDialogButtonBox, QVBoxLayout, QComboBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
import qt5reactor
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import task

from src.main.python.config_ui import Ui_Dialog
from src.main.python.main_ui import Ui_MainWindow

from dataclasses import dataclass, asdict
from aenum import Enum
import configparser
import os


class TickEnum(Enum):
    HUNDREDTHS = .01
    FHUNDREDTHS = .05
    TENTHS = .1
    FTENTHS = .5
    ONES = 1
    TWOS = 2
    FIVES = 5
    TENS = 10
    TWENTYS = 20
    THIRTHYS = 30
    MINS = 60


class RunningEnum(Enum):
    RUNNING = "RUNNING"
    NOTRUNNING = "NOTRUNNING"


class BrightnessSliderEnum(Enum, init="slider enumv string"):
    FULL = (5, 1, "100%")
    HALF = (4, 2, "50%")
    QUARTER = (3, 4, "25%")
    PCT_TEN = (2, 10, "10%")
    PCT_FIVE = (1, 20, "5%")
    OFF = (0, 0, "0%")

    def _missing_value_(key):
        for entry in list(BrightnessSliderEnum):
            if entry.slider == key:
                return entry


@dataclass
class Machine:
    name: str
    speed: TickEnum
    running: RunningEnum
    id: str
    desc: str

    iname: str = None


@dataclass
class Device:
    iname: str
    id: str
    name: str
    updated: datetime = datetime.now()

    def update(self):
        self.updated = datetime.now()


@dataclass
class LinkSpecSrc:
    listname: str
    ttl: str
    id: str
    cls: str


@dataclass
class LinkSpecTgt:
    listname: str
    grp: str
    iname: str
    id: str
    name: str


@dataclass
class LinkSpec:
    source: LinkSpecSrc
    target: LinkSpecTgt


@dataclass
class Link:
    name: str
    active: bool
    list_name: bool
    full_spec: LinkSpec


@dataclass
class LinkSrc:
    listname: str
    ttl: str
    id: str
    cls: str


@dataclass
class LinkSink:
    listname: str
    grp: str
    iname: str
    id: str
    name: str

    def dict(self):
        return {}


class GenericComboBoxForm(QWidget):
    def __init__(self, label: str, items: List, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.items = items
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        self.box = QComboBox(self)
        self.box.addItems(items)
        layout.addWidget(self.box)

        self.setLayout(layout)


class GenericTextEntryWithButton(QWidget):
    def __init__(self, label: str, button_icon: QIcon, button_tt: str, button_callable: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_callable = button_callable

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        self.button = QPushButton()
        self.button.setToolTip(button_tt)
        self.button.setIcon(button_icon)
        self.button.clicked.connect(self.do_button_callable)
        layout.addWidget(self.button)

        self.setLayout(layout)

    @inlineCallbacks
    def do_button_callable(self, event):
        res = yield self.button_callable()
        self.line_edit.setText(res)


class DeviceListHeader(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label_row_layout = QHBoxLayout()

        label_row_layout.addWidget(QLabel("IP"))
        label_row_layout.addWidget(QLabel("Name"))
        label_row_layout.addWidget(QLabel(""))
        self.setLayout(label_row_layout)


class DeviceListControls(QWidget):
    device: Device

    def __init__(self, device: Device, session: ApplicationSession, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = device
        self.session = session

        layout = QHBoxLayout()

        pm_rename = QPixmap('imgs/rename-box.png')
        pic_rename = QLabel()
        pic_rename.setToolTip("Rename")
        pic_rename.setPixmap(pm_rename)
        pic_rename.mousePressEvent = self.on_rename
        layout.addWidget(pic_rename)

        pm_poke = QPixmap("imgs/flash-alert.png")
        pic_poke = QLabel()
        pic_poke.setToolTip("Poke")
        pic_poke.setPixmap(pm_poke)
        pic_poke.mousePressEvent = self.on_poke
        layout.addWidget(pic_poke)

        self.setLayout(layout)

    def on_rename(self, event):
        dialog = DeviceNameDialog(self.device, session=self.session)
        dialog.exec()

    @inlineCallbacks
    def _on_poke(self):
        yield self.session.call(
            "com.lambentri.edge.la4.device.82667777.poke",
            shortname=self.device.iname
        )

    def on_poke(self, event):
        print("poke")
        self._on_poke()
        print("qqq")
        return


class DeviceListLayout(QWidget):
    device: Device

    def __init__(self, device: Device, session: ApplicationSession, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = device
        self.session = session

        layout = QHBoxLayout()
        layout.addWidget(QLabel(device.iname))
        layout.addWidget(QLabel(device.name))
        layout.addWidget(DeviceListControls(device, session))

        self.setLayout(layout)


class DeviceNameDialog(QDialog):
    def __init__(self, device: Device, session: 'LambentSessionWindow', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = device
        self.session = session

        self.setWindowTitle("Name It")

        self.layout = QHBoxLayout()

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    @inlineCallbacks
    def accept(self):
        if self.line_edit.text() == "":
            return

        yield self.session.call(
            "com.lambentri.edge.la4.device.82667777.name",
            shortname=self.device.iname,
            nicename=self.line_edit.text()
        )
        self.session.device_list[self.device.id].name = self.line_edit.text()
        super().accept()


class MachineListHeader(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Type"))
        layout.addWidget(QLabel("Ticks"))
        layout.addWidget(QLabel("Status"))
        layout.addWidget(QLabel("Name"))
        layout.addWidget(QLabel())
        self.setLayout(layout)


class MachineControlSpeedLayout(QWidget):
    machine_plus = pyqtSignal(str)
    machine_minus = pyqtSignal(str)

    machine: Machine

    def __init__(self, machine: Machine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine = machine

        pm_plus = QPixmap('imgs/plus.png')
        pm_minus = QPixmap('imgs/minus.png')

        pic_plus = QLabel()
        pic_plus.setPixmap(pm_plus)
        pic_plus.mousePressEvent = self.on_plus
        pic_plus.setAlignment(QtCore.Qt.AlignRight)
        pic_minus = QLabel()
        pic_minus.setAlignment(QtCore.Qt.AlignLeft)
        pic_minus.setPixmap(pm_minus)
        pic_minus.mousePressEvent = self.on_minus

        layout = QHBoxLayout()
        layout.addWidget(pic_minus)
        layout.addWidget(QLabel(machine.speed))
        layout.addWidget(pic_plus)
        self.setLayout(layout)

    def on_plus(self, event):
        print("plus_a")
        self.machine_plus.emit(self.machine.id)

    def on_minus(self, event):
        print("minus_a")
        self.machine_minus.emit(self.machine.id)


class MachineListControls(QWidget):
    bslider: QSlider
    blabel: QLabel

    machine_brightness_set = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QHBoxLayout()
        # layout.addWidget(QSpacerItem())

        ## New Button
        pm_plus = QIcon('imgs/plus.png')
        self.newButton = QPushButton()
        self.newButton.setToolTip("New Machine")
        self.newButton.setIcon(pm_plus)
        self.newButton.clicked.connect(self.new_button_clicked)
        layout.addWidget(self.newButton)

        ## Search Box
        self.slabel = QLabel("Search")
        layout.addWidget(self.slabel)
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.search_value_changed)
        layout.addWidget(self.searchbar)

        ## Brightness Slider
        layout.addWidget(QLabel("Global Brightness"))
        self.bslider = QSlider(QtCore.Qt.Horizontal, self)
        self.bslider.setRange(0, 5)
        self.bslider.setSingleStep(1)
        self.bslider.setValue(5)
        self.bslider.valueChanged[int].connect(self.slider_value_changed)
        layout.addWidget(self.bslider)

        self.blabel = QLabel("100%")
        layout.addWidget(self.blabel)

        self.setLayout(layout)

    def slider_value_changed(self, value):
        enum_val = BrightnessSliderEnum(value)
        self.blabel.setText(enum_val.string)
        self.machine_brightness_set.emit(enum_val.enumv)

    def search_value_changed(self, value):
        print(value)

    def new_button_clicked(self):
        print("new_button_clicked")


class MachineListLayout(QWidget):
    layout_speed: MachineControlSpeedLayout
    machine: Machine

    machine_play_pause = pyqtSignal(str)
    machine_rm = pyqtSignal(str)

    def __init__(self, machine: Machine, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.machine = machine

        pm_play = QPixmap('imgs/play.png')
        pm_play_painter = QPainter(pm_play)
        pm_play_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        pm_play_painter.fillRect(pm_play.rect(), QColor(0, 192, 0))
        pm_play_painter.end()

        pm_pause = QPixmap('imgs/pause.png')
        pm_pause_painter = QPainter(pm_pause)
        pm_pause_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        pm_pause_painter.fillRect(pm_pause.rect(), QColor(255, 64, 0))
        pm_pause_painter.end()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        w_name = QLabel(machine.name)
        w_name.setToolTip(machine.desc)
        layout.addWidget(w_name)
        self.layout_speed = MachineControlSpeedLayout(machine)
        layout.addWidget(self.layout_speed)

        pic_running = QLabel()
        pic_running.mousePressEvent = self.on_running
        if machine.running == RunningEnum.NOTRUNNING.value:
            pic_running.setPixmap(pm_pause)
        else:
            pic_running.setPixmap(pm_play)

        layout.addWidget(pic_running)
        # layout.addWidget(QLabel(machine.id))
        # layout.addWidget(QLabel(machine.desc))
        iname = QLabel(machine.iname)
        iname.setToolTip(machine.id)
        layout.addWidget(iname)


        pm_remove = QPixmap('imgs/close-thick.png')
        pm_remove_painter = QPainter(pm_remove)
        pm_remove_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        pm_remove_painter.fillRect(pm_remove.rect(), QColor(0, 102, 202))
        pm_remove_painter.end()

        pic_remove = QLabel()
        pic_remove.mousePressEvent = self.on_remove
        pic_remove.setPixmap(pm_remove)
        layout.addWidget(pic_remove)

        self.setLayout(layout)

    def on_running(self, event):
        print("running_a")
        self.machine_play_pause.emit(self.machine.id)

    def on_remove(self, event):
        self.machine_rm.emit(self.machine.id)

class LinkListHeader(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Name"))
        layout.addWidget(QLabel("Source"))
        layout.addWidget(QLabel("Target"))
        layout.addWidget(QLabel())
        self.setLayout(layout)

class LinkControlToggleLayout(QWidget):
    link_toggle = pyqtSignal(str)
    link_disable = pyqtSignal(str)
    link_rm = pyqtSignal(str)

    link: Link

    def __init__(self, link: Link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.link = link

        layout = QHBoxLayout()

        pm_remove = QPixmap('imgs/close-thick.png')
        pm_remove_painter = QPainter(pm_remove)
        pm_remove_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        pm_remove_painter.fillRect(pm_remove.rect(), QColor(0, 102, 202))
        pm_remove_painter.end()
        pic_remove = QLabel()
        pic_remove.mousePressEvent = self.on_remove
        pic_remove.setPixmap(pm_remove)

        layout.addWidget(pic_remove)

        if link.active:
            pm_switch = QPixmap('imgs/toggle-switch.png')
        else:
            pm_switch = QPixmap('imgs/toggle-switch-off.png')
        pm_switch_painter = QPainter(pm_switch)
        pm_switch_painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if link.active:
            pm_switch_painter.fillRect(pm_switch.rect(), QColor(0, 192, 0))
        else:
            pm_switch_painter.fillRect(pm_switch.rect(), QColor(255, 64, 0))
        pm_switch_painter.end()
        pic_switch = QLabel()
        pic_switch.mousePressEvent = self.on_switch
        pic_switch.setPixmap(pm_switch)

        layout.addWidget(pic_switch)
        




        self.setLayout(layout)

    def on_remove(self, event):
        self.link_rm.emit(self.link.name)

    def on_switch(self, event):
        if self.link.active:
            self.link_disable.emit(self.link.name)
        else:
            self.link_toggle.emit(self.link.name)


class LinkListControls(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QHBoxLayout()
        # layout.addWidget(QSpacerItem())

        ## New Button
        pm_plus = QIcon('imgs/plus.png')
        self.newButton = QPushButton()
        self.newButton.setToolTip("New Link")
        self.newButton.setIcon(pm_plus)
        self.newButton.clicked.connect(self.new_button_clicked)
        layout.addWidget(self.newButton)
        layout.addSpacerItem(QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum))

        self.setLayout(layout)

    def new_button_clicked(self):
        print("new_button_clicked")


class LinkListLayout(QWidget):
    link: Link

    def __init__(self, link: Link, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.link = link

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel(link.name))
        layout.addWidget(QLabel(link.full_spec['source']['listname']))
        layout.addWidget(QLabel(link.full_spec['target']['listname']))
        self.layout_controls = LinkControlToggleLayout(link)
        layout.addWidget(self.layout_controls)

        self.setLayout(layout)


class LinkCreateDialog(QDialog):
    def __init__(self, callable: Callable, session: ApplicationSession, *args, **kwargs):
        super(LinkCreateDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("New Link")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        self.session = session

        self.available_sources = session.link_src_list
        self.available_sources_map = {i.listname: i.id for i in self.available_sources.values()}

        self.available_targets = session.link_sink_list
        self.available_targets_map = {i.listname: i.id for i in self.available_targets.values()}

        # target pair
        self.box_src = GenericComboBoxForm("Source", [i.listname for i in self.available_sources.values()])
        self.layout.addWidget(self.box_src)

        self.box_tgt = GenericComboBoxForm("Target", [i.listname for i in self.available_targets.values()])
        self.layout.addWidget(self.box_tgt)

        self.name_box = GenericTextEntryWithButton("Name", QIcon("imgs/refresh.png"), "Generate", callable)
        self.layout.addWidget(self.name_box)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    @inlineCallbacks
    def accept(self):
        selected_src = self.box_src.box.currentText()
        selected_src_spec = self.available_sources[self.available_sources_map[selected_src]]

        selected_tgt = self.box_tgt.box.currentText()
        selected_tgt_spec = self.available_targets[self.available_targets_map[selected_tgt]]
        yield self.session.call("com.lambentri.edge.la4.links.save",
                                link_name=self.name_box.line_edit.text(),
                                link_spec={
                                    "source": asdict(selected_src_spec),
                                    "target": asdict(selected_tgt_spec)
                                }
                                )

        return super().accept()


class LambentSessionWindow(QMainWindow, Ui_MainWindow, ApplicationSession):
    machine_list: Dict[str, Machine] = dict()
    device_list: Dict[str, Device] = dict()
    link_list: Dict[str, Link] = dict()
    link_src_list: Dict[str, LinkSrc] = dict()
    link_sink_list: Dict[str, LinkSink] = dict()

    controls_machine: MachineListControls

    def __init__(self, config=None):
        QMainWindow.__init__(self)
        ApplicationSession.__init__(self, config)

        self.setupUi(self)

        # self._channel = config.extra['channel']
        self._subscriptions_ = []
        self._controls = [
            # (self.bigFellaDial, self.bigFellaSlider),
            # (self.smallBuddyDial, self.smallBuddySlider),
            # (self.tinyLadDial, self.tinyLadSlider),
            # (self.littlePalDial, self.littlePalSlider),
        ]
        for i, (_, slider) in enumerate(self._controls):
            slider.valueChanged.connect(partial(self.changeValue, i))

        # self.channelEdit.setValidator(QRegularExpressionValidator(CHANNEL_REGEXP))
        # self.channelEdit.setText(self._channel)

        self.actionQuit.triggered.connect(qApp.quit)
        self.tabWidget.setCurrentIndex(0)
        self.statusbar.showMessage("LAMBENT 4")
        self.deviceHolderLayout.addWidget(DeviceListHeader())
        self.machineHolderLayout.addWidget(MachineListHeader())
        self.linkHolderLayout.addWidget(LinkListHeader())

        self.controls_machine = MachineListControls()
        self.controls_machine.machine_brightness_set.connect(self.on_machine_brightness_set)
        self.machineControls.addWidget(self.controls_machine)

        self.controls_link = LinkListControls()
        self.controls_link.newButton.mousePressEvent = self.pressed_new_link_dialog
        self.linkControls.addWidget(self.controls_link)
        self.linkControls
        # self.machineHolderLayout.addWidget(MachineListHeader())

    # @inlineCallbacks
    def onJoin(self, details):
        self.setEnabled(True)
        # yield self.switchChannel(self._channel)
        self.statusbar.showMessage("LAMBENT 4 - Connected")

        self.loop_machine_check = task.LoopingCall(self.machine_check)
        self.loop_machine_check.start(15)

        self.write_machine_list = task.LoopingCall(self.machine_write)
        self.write_machine_list.start(2)

        self.subscribe(self.device_listener, "com.lambentri.edge.la4.machine.sink.8266-7777")
        self.subscribe(self.link_listener, "com.lambentri.edge.la4.links")

    def onDisconnect(self):
        self.statusbar.showMessage("LAMBENT 4 - Disconnected")

    def onLeave(self, details):
        from twisted.internet import reactor
        if reactor.threadpool is not None:
            reactor.threadpool.stop()
        qApp.quit()

    def closeEvent(self, event):
        self.leave()
        event.accept()

    @inlineCallbacks
    def machine_check(self):
        print("machine_check")
        try:
            machine_list_and_enums = yield self.call("com.lambentri.edge.la4.machine.list")  # type: Dict[str, Dict]
            machine_list = machine_list_and_enums['machines']
            for machine_id, spec in machine_list.items():
                self.machine_list[machine_id] = Machine(**spec)
        except ApplicationError:
            print("missing remote machine component")

        return

    def machine_write(self):
        print("machine_write")
        # clear widget
        for item in range(1, self.machineHolderLayout.count()):
            self.machineHolderLayout.itemAt(item).widget().deleteLater()
        # redraw
        for item in list(self.machine_list.values()):
            this_item = MachineListLayout(item)
            this_item.layout_speed.machine_plus.connect(self.on_machine_plus)
            this_item.layout_speed.machine_minus.connect(self.on_machine_minus)
            this_item.machine_play_pause.connect(self.on_machine_play_pause)
            this_item.machine_rm.connect(self.on_machine_remove)
            self.machineHolderLayout.addWidget(this_item)

    def device_listener(self, res: List[Dict[str, str]]):
        # print(res)
        for item in res:
            item_id = item['id']
            if item_id in self.device_list:
                self.device_list[item_id].update()
            else:
                self.device_list[item_id] = Device(**item)

        # clear widget
        for item in range(1, self.deviceHolderLayout.count()):
            self.deviceHolderLayout.itemAt(item).widget().deleteLater()
        # redraw
        for item in self.device_list.values():
            this_item = DeviceListLayout(item, self)
            self.deviceHolderLayout.addWidget(this_item)

    def link_listener(self, links: Dict[str, str], sinks: List, srcs: List):
        # print(sinks)
        # print(srcs)
        for key, item in links.items():
            self.link_list[key] = Link(**item)

        for item in srcs:
            self.link_src_list[item['id']] = LinkSrc(**item)

        for item in sinks:
            self.link_sink_list[item['id']] = LinkSink(**item)

        # clear widget
        for item in range(1, self.linkHolderLayout.count()):
            self.linkHolderLayout.itemAt(item).widget().deleteLater()
        # redraw
        for item in self.link_list.values():
            this_item = LinkListLayout(item)
            this_item.layout_controls.link_rm.connect(self.on_link_rm)
            this_item.layout_controls.link_disable.connect(self.on_link_disable)
            this_item.layout_controls.link_toggle.connect(self.on_link_toggle)
            self.linkHolderLayout.addWidget(this_item)

    def pressed_new_link_dialog(self, event):
        print("clicky-new-link")
        dialog = LinkCreateDialog(self.generate_name_callable, session=self)
        dialog.exec()

    @inlineCallbacks
    def generate_name_callable(self):
        print("refresh")

        res = yield self.call("com.lambentri.edge.la4.helpers.namegen")
        returnValue(res['name'])

    # def on_channelEdit_textChanged(self, text):
    #     backgroundFormat = 'QLineEdit {{ background-color: {}; }}'
    #     if self.channelEdit.hasAcceptableInput():
    #         self.channelEdit.setStyleSheet(backgroundFormat.format('#efe'))
    #         self.channelSwitchButton.setEnabled(text != self._channel)
    #     else:
    #         self.channelEdit.setStyleSheet(backgroundFormat.format('#fee'))
    #         self.channelSwitchButton.setEnabled(False)
    #     self.channelCancelButton.setEnabled(text != self._channel)

    # @pyqtSlot()
    # def on_channelCancelButton_clicked(self):
    #     self.channelEdit.setText(self._channel)
    #
    # @pyqtSlot()
    # def on_channelSwitchButton_clicked(self):
    #     self.switchChannel(self.channelEdit.text())

    @pyqtSlot()
    def on_actionQuit_clicked(self):
        print("clicky")
        self.qApp.quit()

    @inlineCallbacks
    def changeValue(self, index, value):
        yield self.publish(
            # self.topic(self._channel, index), value,
            options=PublishOptions(exclude_me=False))

    @inlineCallbacks
    def on_machine_plus(self, machine_id: str):
        yield self.call("com.lambentri.edge.la4.machine.tick_dn", machine_id)
        yield self.machine_check()
        self.machine_write()

    @inlineCallbacks
    def on_machine_minus(self, machine_id: str):
        yield self.call("com.lambentri.edge.la4.machine.tick_up", machine_id)
        yield self.machine_check()
        self.machine_write()

    @inlineCallbacks
    def on_machine_play_pause(self, machine_id: str):
        print("plpaus")
        yield self.call("com.lambentri.edge.la4.machine.pause", machine_id)
        yield self.machine_check()
        self.machine_write()

    @inlineCallbacks
    def on_machine_remove(self, machine_id: str):
        print("mach_rm")
        yield self.call("com.lambentri.edge.la4.machine.rm", machine_id)
        yield self.machine_check()
        try:
            del self.machine_list[machine_id]
        except:
            pass
        self.machine_write()

    @inlineCallbacks
    def on_machine_brightness_set(self, value: int):
        yield self.call("com.lambentri.edge.la4.machine.gb.set", value)

    @inlineCallbacks
    def on_link_toggle(self, link_id: str):
        yield self.call("com.lambentri.edge.la4.links.toggle", link_id)

    @inlineCallbacks
    def on_link_disable(self, link_id: str):
        yield self.call("com.lambentri.edge.la4.links.disable", link_id)
        self.link_list[link_id].active = False

    @inlineCallbacks
    def on_link_rm(self, link_id: str):
        yield self.call("com.lambentri.edge.la4.links.destroy", link_id)
        try:
            del self.link_list[link_id]
        except:
            raise

class LambentConfigWindow(QMainWindow, Ui_Dialog):
    def __init__(self, config=None):
        QMainWindow.__init__(self)
        ApplicationSession.__init__(self, config)

        self.setupUi(self)


def make(config):
    session = LambentSessionWindow(config)
    session.show()
    return session


def parse_args():
    parser = ArgumentParser(description='PyQt version of Lambent4')
    parser.add_argument('--url',
                        type=str,
                        default=u'ws://127.0.0.1:8083/ws',
                        metavar='<url>',
                        help='WAMP router URL (default: ws://127.0.0.1:8083/ws).')

    return parser.parse_args()


def main():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~/.la4.config.ini"))

    args = parse_args()
    app = QApplication(argv)
    qt5reactor.install()

    if not args.url or not "url" in config.options("gui"):
        print("missing config file/parmas")
        return
    elif "url" in "url" in config.options("gui"):
        print("found config")
        runner = ApplicationRunner(config.get("gui", "url"), u'realm1', extra=vars(args))
        runner.run(make)
    else:
        runner = ApplicationRunner(args.url, u'realm1', extra=vars(args))
        runner.run(make)


if __name__ == '__main__':
    main()
