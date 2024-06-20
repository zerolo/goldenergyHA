from dataclasses import dataclass
import datetime
from .meter import Meter
from ..const import GAS, ELECTRICITY


@dataclass(init=True, repr=True)
class Consumption:
    date: datetime.datetime
    meter: Meter
    realM3: int
    estimatedM3: int
    realKWh: int
    estimatedKWH: int
    energy_type: str

    @classmethod
    def from_dict(cls, data):
        energies = data.get("energies")
        consumptions = {}
        for energy in energies:
            energy_type = GAS if energy.get("energyType") == 0 else ELECTRICITY
            consumption = cls(
                date=data.get("date"),
                meter=Meter.from_dict(energy.get("meters")[0].get("meter")),
                realM3=energy.get("meters")[0].get("realM3"),
                estimatedM3=energy.get("meters")[0].get("estimatedM3"),
                realKWh=energy.get("meters")[0].get("realKWh"),
                estimatedKWH=energy.get("meters")[0].get("estimatedKWH"),
                energy_type=energy_type
            )
            consumptions[energy_type] = consumption

        return consumptions

