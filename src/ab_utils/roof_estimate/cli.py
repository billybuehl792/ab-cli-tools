import argparse
import json
from pathlib import Path
import subprocess

from ab_utils.utils import json_to_csv

from .classes import RoofEstimate, RoofrReport
from .models import Customer, LaborCatalog, MaterialCatalog, RoofEstimateOptions, RoofMeasurements
from .constants import APP_NAME, DEFAULT_LABOR_CATALOG, DEFAULT_MATERIAL_CATALOG


def add_parser(subparsers):
    parser: argparse.ArgumentParser = subparsers.add_parser(APP_NAME, help="Create roof estimate", description=(
        "Create a roof estimate from measurements, material prices, ""and labor prices."))

    # Input options
    parser.add_argument(
        "measurements", help=f"Path to roof measurements JSON.")
    parser.add_argument("--name",
                        default="", help=f"Customer Name (default: '')")
    parser.add_argument("--address",
                        default="", help=f"Customer Address (default: '')")
    parser.add_argument("--email",
                        default="", help=f"Customer Email (default: '')")
    parser.add_argument("--phone",
                        default="", help=f"Customer Phone (default: '')")
    parser.add_argument("--extract-measurements", action="store_true",
                        help="extract measurements from the input file.")
    parser.add_argument("-labor", "--labor-catalog",
                        default=DEFAULT_LABOR_CATALOG, help=f"Labor catalog JSON file (default: {DEFAULT_LABOR_CATALOG})")
    parser.add_argument("-material", "--material-catalog",
                        default=DEFAULT_MATERIAL_CATALOG, help=f"Material catalog JSON file (default: {DEFAULT_MATERIAL_CATALOG})")

    # Output options
    parser.add_argument("--csv", action="store_true", help="output as CSV")
    parser.add_argument("-o", "--output", default=None, help="Output file")
    parser.add_argument("-c", "--copy", action="store_true",
                        help="copy to clipboard.")

    parser.set_defaults(func=run)


def run(args: argparse.Namespace):
    is_extract_measurements = args.extract_measurements
    print("Extracting measurements..." if is_extract_measurements else "Creating roof estimate...")

    measurements_path = Path(args.measurements)
    address = args.address
    customer = Customer(name=args.name, address=address,
                        phone=args.phone, email=args.email)
    output_file_path = Path(args.output) if args.output else None
    output_file_path_type = output_file_path.suffix.lower().lstrip(
        ".") if output_file_path else None

    if output_file_path is not None:
        if output_file_path_type not in ["json", "csv"]:
            raise ValueError(
                f"Unsupported output file type: {output_file_path_type}")
        if args.csv and output_file_path_type != "csv":
            raise ValueError(
                f"CSV output requested but output file type is {output_file_path_type}")

    if measurements_path.suffix.lower() == ".csv":
        address, measurements = RoofrReport(measurements_path).extract()
    else:
        measurements = RoofMeasurements.model_validate_json(
            measurements_path.read_text(), by_name=True)

    if is_extract_measurements:
        json_output = measurements.model_dump_json(indent=2)
        csv_output = measurements.get_formatted_csv()
    else:
        labor_catalog = LaborCatalog.model_validate_json(
            Path(args.labor_catalog).read_text())
        material_catalog = MaterialCatalog.model_validate_json(
            Path(args.material_catalog).read_text())

        roof_estimate = RoofEstimate(
            RoofEstimateOptions(
                customer=customer,
                measurements=measurements,
                material_catalog=material_catalog,
                labor_catalog=labor_catalog)
        )

        json_output = roof_estimate.get_json()
        csv_output = roof_estimate.get_csv()

    # Output
    if args.copy:
        subprocess.run(
            ["pbcopy"], input=csv_output if args.csv else json_output, text=True)
        print(f"{'CSV' if args.csv else 'JSON'} copied to clipboard.")

    if output_file_path:
        output_file_path.write_text(
            csv_output if output_file_path_type == "csv" else json_output)
        print(f"Output written to {output_file_path.name}")
    else:
        print(csv_output if args.csv else json_output)
