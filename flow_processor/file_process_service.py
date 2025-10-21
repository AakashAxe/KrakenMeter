from .meter_reading_codes import MeterReadingsCodes as Codes
from .repository import FlowRepository

# TODO : Read each line check Enum

def read_line(line: str):
    data = line.split("|")
    code = data[0]
    if code == Codes.MPAN_CORE.value:
        # Process MPAN core line
        print(f"Processing MPAN Core Line: {line}")
        process_mpan_core(data)
    elif code == Codes.METER_READING_TYPE.value:
        # Process meter reading line
        #print(f"Processing Meter Reading Line: {line}")
        pass
    elif code == Codes.REGISTER_READINGS.value:
        # Process register readings line
        #print(f"Processing Register Readings Line: {line}")
        pass
    else:
        print(f"Unknown code {code} in line: {line}")


def process_mpan_core(data: [str]):
    core = data[1]
    status = data[2]
    print(f"MPAN Core: {core}, BCS Validation Status: {status}")
    if FlowRepository().get_mpan(core) is None:
        FlowRepository().create_mpan(mpan_core=core, bcs_validation_status=status)
    else:
        print(f"MPAN Core {core} already exists in the database.")


def process_meter_reading(line: str):
    # Placeholder for processing meter reading lines
    pass

def process_register_reading(line: str):
    # Placeholder for processing register reading lines
    pass
    