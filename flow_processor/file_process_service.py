from .meter_reading_codes import MeterReadingsCodes as Codes
from .repository import FlowRepository

# TODO : Read each line check Enum

def process_file(file_path: str):
    with open(file_path, 'r') as file:
        current_mpan_core_obj = None
        current_meter_obj = None
        for line in file:
            current_mpan_core_obj, current_meter_obj = read_line(line.strip(), current_mpan_core_obj, current_meter_obj)
            print(current_mpan_core_obj, current_meter_obj)

            

def read_line(line: str, current_mpan_core_obj: Optional[str], current_meter_obj: Optional[str]):
    data = line.split("|")
    code = data[0]
    if code == Codes.MPAN_CORE.value:
        # Process MPAN core line
        #print(f"Processing MPAN Core Line: {line}")
        return process_mpan_core(data)
    elif code == Codes.METER_READING_TYPE.value:
        # Process meter reading line
        print(f"Processing Meter Reading Line: {line}")
        return process_meter_reading(data, current_mpan_core_obj)
    elif code == Codes.REGISTER_READINGS.value:
        # Process register readings line
        print(f"Processing Register Readings Line: {line}")
        return None, None
    else:
        print(f"Unknown code {code} in line: {line}")
        return None, None


def process_mpan_core(data: [str]):
    core = data[1]
    status = data[2]
    print(f"MPAN Core: {core}, BCS Validation Status: {status}")
    if FlowRepository().get_mpan(core) is None:
        MPANCoreObj, created = FlowRepository().get_or_create_mpan(mpan_core=core, bcs_validation_status=status)
        return MPANCoreObj, None
    else:
        print(f"MPAN Core {core} already exists in the database.")
        return FlowRepository().get_mpan(core), None


def process_meter_reading(data: [str], current_mpan_core: Optional[str]):
    if current_mpan_core is None:
        print("Error: No current MPAN core set for meter reading.")
        return
    meter_id = data[1]
    print(f"Meter ID: {meter_id}")
    reading_type = data[2]
    if FlowRepository().get_meter_by_id(meter_id) is None:
        FlowRepository().get_or_create_meter(mpan_core_obj=current_mpan_core, meter_id=meter_id, meter_type=reading_type)
        return current_mpan_core, meter_id
    else:
        print(f"Meter ID {meter_id} already exists in the database.")
        return current_mpan_core, meter_id

def process_register_reading(line: str):
    # Placeholder for processing register reading lines
    pass
    