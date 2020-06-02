"""
Widgets used to initialize a given machine type, machines declare their intentions in the config spec and announce it over the network
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider, QVBoxLayout
from aenum import Enum
from pydantic.dataclasses import dataclass
from typing import Union, List, Dict, Any


class MachineInitVHolder(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout()
        # TODO BETTER COPY
        self.layout.addWidget(QLabel("This will be populated once you've selected your machine template"))
        self.setLayout(self.layout)


class MachineInitWidgetContainer(QWidget):
    def __init__(self, machine_spec_config: "MachineSpecConfig", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel(machine_spec_config.title))
        self.layout.addWidget(QLabel(machine_spec_config.desc))
        if machine_spec_config.comp == MachineSpecComponentEnum.SliderComponent:
            if machine_spec_config.cls.name == "IntegerConfig":
                print("wewlad")
                self.layout.addWidget(
                    MachineInitInputSlider(
                        label="fff",
                        val_min=machine_spec_config.cls.field_validation['min'],
                        val_max=machine_spec_config.cls.field_validation['max'],
                        val_default=machine_spec_config.cls.field_default
                    )
                )

        # self.layout.addWidget()
        self.setLayout(self.layout)


class MachineInitInputSlider(QWidget):
    xlabel = None

    def __init__(self, label, val_min, val_max, val_default, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slider = QSlider(Qt.Horizontal)

        self.slider.setRange(val_min, val_max)
        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.slider_value_changed)
        self.xlabel = QLabel("-")

        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        layout.addWidget(self.slider)
        layout.addWidget(self.xlabel)


        self.setLayout(layout)

        if val_default:
            self.slider.setValue(int(val_default))
        else:
            self.slider.setValue(0)

    def slider_value_changed(self, value):
        self.xlabel.setText(str(value))


class MachineInitInputTupleSlider(QWidget):
    # A layout for initializing a machine that contains a tuple of sliders with various limits and parameters
    def __init__(self, label, val_min, val_max, val_default, fields, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MachineInitInputToggle(QWidget):
    pass


class MachineInitInputSelector(QWidget):
    pass


class MachineInitInputMultiSelector(QWidget):
    pass


class MachineInitKeyValueTuple(QWidget):
    pass


# widget that allows arrays of subwidgets to be added,
# should _technically_ be able to nest into self for stuff like mmcc which is a list of RGB values
class MachineInitArrayWidget(QWidget):
    def __init__(self, widget, initial_count=1, *args, **kwargs):
        pass


class MachineSpecConfigClsNameEnum(Enum):
    TupleConfig = "TupleConfig"
    IntegerConfig = "IntegerConfig"

class MachineSpecComponentEnum(Enum, init="title cls"):
    SliderComponent = ("SliderComponent", MachineInitInputTupleSlider)

    def _missing_value_(key):
        for entry in list(MachineSpecComponentEnum):
            if entry.title == key:
                return entry


@dataclass
class MachineSpecConfigCls:
    field_default: Union[List[Union[str, int]], Union[str, int]]
    field_titles: List[str]
    field_validation: Dict[str, Any]
    name: str

    field_type: str = "Int"
    field_cnt: int = 1


@dataclass
class MachineSpecConfig:
    cls: MachineSpecConfigCls
    comp: MachineSpecComponentEnum
    desc: str = None
    title: str = None

    class Config:
        arbitrary_types_allowed = True

    def widget(self):
        return MachineInitWidgetContainer(self)


@dataclass
class MachineSpec:
    desc: str
    cls: str
    grp: List[str]
    conf: Dict[str, MachineSpecConfig]

    class Config:
        arbitrary_types_allowed = True