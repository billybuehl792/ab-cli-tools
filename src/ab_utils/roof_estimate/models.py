from typing import Literal
from pydantic import BaseModel, Field


class ChargeItem(BaseModel):
    label: str
    description: str = ''
    uom: Literal["sqft", "lf", "unit"]
    unit_size: float
    unit_price: float


class CostItem(ChargeItem):
    quantity: float


class LaborCatalog(BaseModel):
    re_roof_comp: ChargeItem
    re_deck: ChargeItem
    re_roof_shake: ChargeItem
    flat_roofing: ChargeItem

    steep_8_12: ChargeItem
    steep_9_12: ChargeItem
    steep_10_12: ChargeItem
    steep_11_12: ChargeItem
    steep_12_12: ChargeItem
    mansard: ChargeItem

    second_story: ChargeItem
    second_layer: ChargeItem
    third_layer: ChargeItem

    decking_4x8: ChargeItem
    decking_lf: ChargeItem

    chimney_flashing: ChargeItem
    skylight_flashing_reflash: ChargeItem
    skylight_flashing_new: ChargeItem
    replace_skylight: ChargeItem

    cut_in_box_vent: ChargeItem
    cut_in_hip_vent: ChargeItem
    cut_in_ridge_vent: ChargeItem

    slate_tear_off: ChargeItem
    cricket_install: ChargeItem
    emergency_service_tarps: ChargeItem
    dump_fee: ChargeItem


class MaterialCatalog(BaseModel):
    landmark: ChargeItem
    cap_shingle: ChargeItem
    starter: ChargeItem
    ice_shield: ChargeItem
    synthetic: ChargeItem
    ridge_vent: ChargeItem
    hip_vent: ChargeItem
    box_vent: ChargeItem
    edge_vent: ChargeItem
    drip_edge: ChargeItem
    valley: ChargeItem
    cap_nail: ChargeItem
    coil_nail: ChargeItem
    coil: ChargeItem
    step_flashing: ChargeItem
    sanitary_boots: ChargeItem
    rvk1a: ChargeItem
    caulk: ChargeItem
    sa_top: ChargeItem
    sa_base: ChargeItem
    skylights: ChargeItem
    wood: ChargeItem
    fuel: ChargeItem
    delivery_fee: ChargeItem


class Pitch(BaseModel):
    pitch: int = Field(ge=0, le=100)
    area: float = Field(ge=0, json_schema_extra={"unit": "sqft"})


class Customer(BaseModel):
    name: str
    address: str
    phone: str
    email: str


class RoofMeasurements(BaseModel):
    total_roof_area: float = Field(
        alias="Total roof area (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    total_flat_area: float = Field(
        alias="Total flat area (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    total_pitched_area: float = Field(
        alias="Total pitched area (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    two_story: float = Field(alias="Two Story (Sqft)",
                             ge=0, json_schema_extra={"unit": "sqft"})
    two_layer: float = Field(alias="Two Layer (Sqft)",
                             ge=0, json_schema_extra={"unit": "sqft"})
    eaves: float = Field(alias="Eaves (LF)", ge=0,
                         json_schema_extra={"unit": "lf"})
    valleys: float = Field(alias="Valleys (LF)", ge=0,
                           json_schema_extra={"unit": "lf"})
    hips: float = Field(alias="Hips (LF)", ge=0,
                        json_schema_extra={"unit": "lf"})
    ridges: float = Field(alias="Ridges (LF)", ge=0,
                          json_schema_extra={"unit": "lf"})
    rakes: float = Field(alias="Rakes (LF)", ge=0,
                         json_schema_extra={"unit": "lf"})
    wall_flashing: float = Field(
        alias="Wall Flashing (LF)", ge=0, json_schema_extra={"unit": "lf"})
    step_flashing: float = Field(
        alias="Step Flashing (LF)", ge=0, json_schema_extra={"unit": "lf"})
    transitions: float = Field(
        alias="Transitions (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    parapet_wall: float = Field(
        alias="Parapet Wall (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    unspecified: float = Field(
        alias="Unspecified (Sqft)", ge=0, json_schema_extra={"unit": "sqft"})
    chimneys: int = Field(default=0, alias="Chimneys", ge=0)
    skylights: int = Field(default=0, alias="Skylights", ge=0)
    vent_pipes: int = Field(default=0, alias="Vent Pipes", ge=0)
    rvk1as: int = Field(default=0, alias="RVK1As", ge=0)

    pitch_breakdown: list[Pitch] = Field(
        default_factory=list, alias="Pitch breakdown")


class RoofEstimateOptions(BaseModel):
    customer: Customer
    measurements: RoofMeasurements
    material_catalog: MaterialCatalog
    labor_catalog: LaborCatalog


class MaterialBreakdown(BaseModel):
    landmark: CostItem
    cap_shingle: CostItem
    starter: CostItem
    ice_shield: CostItem
    synthetic: CostItem
    ridge_vent: CostItem
    hip_vent: CostItem | None = None
    box_vent: CostItem | None = None
    edge_vent: CostItem | None = None
    drip_edge: CostItem
    valley: CostItem
    cap_nail: CostItem
    coil_nail: CostItem
    coil: CostItem
    step_flashing: CostItem
    sanitary_boots: CostItem
    rvk1a: CostItem
    caulk: CostItem
    sa_top: CostItem
    sa_base: CostItem
    skylights: CostItem | None = None
    wood: CostItem | None = None
    fuel: CostItem
    delivery_fee: CostItem


class LaborBreakdown(BaseModel):
    re_roof_comp: CostItem
    re_deck: CostItem
    re_roof_shake: CostItem
    flat_roofing: CostItem

    steep_8_12: CostItem
    steep_9_12: CostItem
    steep_10_12: CostItem
    steep_11_12: CostItem
    steep_12_12: CostItem
    mansard: CostItem

    second_story: CostItem
    second_layer: CostItem
    third_layer: CostItem

    decking_4x8: CostItem
    decking_lf: CostItem

    chimney_flashing: CostItem
    skylight_flashing_reflash: CostItem
    skylight_flashing_new: CostItem
    replace_skylight: CostItem

    cut_in_box_vent: CostItem
    cut_in_hip_vent: CostItem
    cut_in_ridge_vent: CostItem

    slate_tear_off: CostItem
    cricket_install: CostItem
    emergency_service_tarps: CostItem
    dump_fee: CostItem
