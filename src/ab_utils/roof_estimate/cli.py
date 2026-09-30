import argparse
from pathlib import Path

from .classes import RoofEstimate, RoofrReport
from .models import Customer, LaborCatalog, MaterialCatalog, RoofEstimateOptions, RoofMeasurements
from .constants import APP_NAME, DEFAULT_LABOR_CATALOG, DEFAULT_MATERIAL_CATALOG


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Create roof estimate", description=(
        "Create a roof estimate from measurements, material prices, ""and labor prices."))

    # Measurements
    parser.add_argument(
        "measurements", help=f"Path to roof measurements JSON.")

    # Customer Information
    parser.add_argument("--name",
                        default="", help=f"Customer Name (default: '')")
    parser.add_argument("--address",
                        default="", help=f"Customer Address (default: '')")
    parser.add_argument("--email",
                        default="", help=f"Customer Email (default: '')")
    parser.add_argument("--phone",
                        default="", help=f"Customer Phone (default: '')")

    # Prices
    parser.add_argument("-labor", "--labor-catalog",
                        default=DEFAULT_LABOR_CATALOG, help=f"Labor catalog JSON file (default: {DEFAULT_LABOR_CATALOG})")
    parser.add_argument("-material", "--material-catalog",
                        default=DEFAULT_MATERIAL_CATALOG, help=f"Material catalog JSON file (default: {DEFAULT_MATERIAL_CATALOG})")
    parser.add_argument("-o", "--output", default=None,
                        help="Output JSON file")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    measurements_path = Path(args.measurements)
    address = str(args.address)

    if measurements_path.suffix.lower() == ".csv":
        address, measurements = RoofrReport(measurements_path).extract()
    else:
        measurements = RoofMeasurements.model_validate_json(
            measurements_path.read_text(), by_name=True)

    customer = Customer(name=args.name, address=address,
                        phone=args.phone, email=args.email)

    labor_catalog = LaborCatalog.model_validate_json(
        Path(args.labor_catalog).read_text())
    material_catalog = MaterialCatalog.model_validate_json(
        Path(args.material_catalog).read_text())

    # print(labor_catalog.model_dump_json(indent=2))
    # print(material_catalog.model_dump_json(indent=2))
    # print(measurements.model_dump_json(indent=2))

    roof_estimate = RoofEstimate(
        RoofEstimateOptions(
            customer=customer,
            measurements=measurements,
            material_catalog=material_catalog,
            labor_catalog=labor_catalog)
    )

    print(roof_estimate.get_materials().model_dump_json(indent=2))

    # if args.output:
    #     output_file = Path(args.output)
    #     output_file.write_text(output)
    #     print(f"Output written to {output_file.name}")
    # else:
    #     print(output)
