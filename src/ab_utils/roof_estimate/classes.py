import math
from pathlib import Path
import pandas as pd

from .models import CostItem, MaterialBreakdown, Pitch, RoofEstimateOptions, RoofMeasurements, MaterialCatalog, LaborCatalog
from .constants import PITCH_PATTERN


class Materials:
    def __init__(self, measurements: RoofMeasurements, material_catalog: MaterialCatalog):
        self.measurements = measurements
        self.material_catalog = material_catalog

    def update_measurements(self, **updates) -> RoofMeasurements:
        for key, value in updates.items():
            setattr(self.measurements, key, value)

        return self.measurements

    def get_landmark(self, waste=1.12):
        charge_item = self.material_catalog.landmark
        quantity = round(self.measurements.total_pitched_area /
                         charge_item.unit_size * waste * 3) / 3

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_cap(self, waste=1.25):
        charge_item = self.material_catalog.cap_shingle
        quantity = math.ceil(
            (self.measurements.hips + self.measurements.ridges) / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_starter(self, waste=1.1):
        charge_item = self.material_catalog.starter
        quantity = math.ceil((self.measurements.valleys * 2 + self.measurements.eaves +
                             self.measurements.rakes) / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_ice_guard(self, waste=1.33):
        charge_item = self.material_catalog.ice_shield
        quantity = math.ceil((self.measurements.eaves * 2 +
                             self.measurements.valleys) / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_synthetic(self, waste=1.1):
        charge_item = self.material_catalog.synthetic
        ice_shield_coverage = (self.measurements.eaves * 2 +
                               self.measurements.valleys) / self.material_catalog.ice_shield.unit_size

        quantity = math.ceil(
            (self.measurements.total_pitched_area - ice_shield_coverage) * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_ridge_vent(self, waste=1):
        charge_item = self.material_catalog.ridge_vent
        quantity = math.ceil(self.measurements.ridges /
                             charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_drip_edge(self, waste=1.15):
        charge_item = self.material_catalog.drip_edge
        quantity = math.ceil(
            (self.measurements.eaves + self.measurements.rakes) /
            charge_item.unit_size * waste
        )

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_valley(self, waste=1.1):
        charge_item = self.material_catalog.valley
        quantity = math.ceil(self.measurements.valleys /
                             charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_cap_nail(self, extra=0):
        charge_item = self.material_catalog.cap_nail
        quantity = math.ceil(
            self.measurements.total_roof_area / charge_item.unit_size) + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_coil_nail(self, extra=0):
        charge_item = self.material_catalog.coil_nail
        quantity = math.ceil(
            self.measurements.total_roof_area / charge_item.unit_size) + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_coil(self, extra=0):
        charge_item = self.material_catalog.coil
        quantity = (max(1, math.ceil(self.measurements.chimneys))
                    if self.measurements.chimneys > 0 else 0) + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_step_flashing(self, waste=1.05):
        charge_item = self.material_catalog.step_flashing
        quantity = math.ceil(
            self.measurements.step_flashing / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_sanitary_boots(self, extra=0):
        charge_item = self.material_catalog.sanitary_boots
        quantity = self.measurements.vent_pipes + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_rvk1as(self, extra=0):
        charge_item = self.material_catalog.rvk1a
        quantity = self.measurements.rvk1as + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_caulk(self, extra=0):
        charge_item = self.material_catalog.caulk

        skylight_caulk = self.measurements.skylights
        chimney_caulk = self.measurements.chimneys
        vent_pipe_caulk = math.ceil(self.measurements.vent_pipes / 4)
        flashing_caulk = math.ceil(math.ceil(
            self.measurements.wall_flashing + self.measurements.step_flashing) / 150)

        quantity = skylight_caulk + chimney_caulk + \
            vent_pipe_caulk + flashing_caulk + extra

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_sa_top(self, waste=1.2):
        charge_item = self.material_catalog.sa_top
        quantity = math.ceil(
            self.measurements.total_flat_area / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_sa_base(self, waste=1.2):
        charge_item = self.material_catalog.sa_base
        quantity = math.ceil(
            self.measurements.total_flat_area / charge_item.unit_size * waste)

        return CostItem(**charge_item.model_dump(), quantity=quantity)

    def get_fuel(self):
        charge_item = self.material_catalog.fuel
        return CostItem(**charge_item.model_dump(), quantity=1)

    def get_delivery_fee(self):
        charge_item = self.material_catalog.delivery_fee
        return CostItem(**charge_item.model_dump(), quantity=1)

    def get_materials(self) -> MaterialBreakdown:
        return MaterialBreakdown(
            landmark=self.get_landmark(),
            cap_shingle=self.get_cap(),
            starter=self.get_starter(),
            ice_shield=self.get_ice_guard(),
            synthetic=self.get_synthetic(),
            ridge_vent=self.get_ridge_vent(),
            hip_vent=None,
            box_vent=None,
            edge_vent=None,
            drip_edge=self.get_drip_edge(),
            valley=self.get_valley(),
            cap_nail=self.get_cap_nail(),
            coil_nail=self.get_coil_nail(),
            coil=self.get_coil(),
            step_flashing=self.get_step_flashing(),
            sanitary_boots=self.get_sanitary_boots(),
            rvk1a=self.get_rvk1as(),
            caulk=self.get_caulk(),
            sa_top=self.get_sa_top(),
            sa_base=self.get_sa_base(),
            skylights=None,
            wood=None,
            fuel=self.get_fuel(),
            delivery_fee=self.get_delivery_fee(),
        )


class Labor:
    def __init__(self, measurements: RoofMeasurements, labor_catalog: LaborCatalog):
        self.measurements = measurements
        self.labor_catalog = labor_catalog

    def get_labor(self):
        return {
            "cost": 0, "labor": []
        }


class RoofEstimate:
    def __init__(self, options: RoofEstimateOptions):
        self.customer = options.customer
        self.measurements = options.measurements
        self.material_catalog = options.material_catalog
        self.labor_catalog = options.labor_catalog
        self.materials = Materials(
            measurements=options.measurements, material_catalog=options.material_catalog)
        self.labor = Labor(
            measurements=options.measurements, labor_catalog=options.labor_catalog)

    def get_materials(self):
        return self.materials.get_materials()

    def get_labor(self):
        return self.labor.get_labor()


class RoofrReport:
    def __init__(self, report: Path):
        self.report = report

    def extract_address(self):
        row = pd.read_csv(self.report).iloc[0]
        return str(row["Address"])

    def extract_measurements(self):
        if self.report.suffix.lower() != ".csv":
            raise ValueError("Roofr report file file must be a CSV file.")

        row = pd.read_csv(self.report).iloc[0]
        data = row.to_dict()

        pitch_breakdown = []
        for column, area in row.items():
            match = PITCH_PATTERN.match(str(column))
            if match and pd.notna(area) and area > 0:
                pitch_breakdown.append(
                    Pitch(pitch=int(match.group(1)), area=float(area)))

        data["Pitch breakdown"] = pitch_breakdown

        return RoofMeasurements.model_validate(data)

    def extract(self):
        return self.extract_address(), self.extract_measurements()
