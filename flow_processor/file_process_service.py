from .meter_reading_codes import MeterReadingsCodes as Codes
from .repository import FlowRepository
from datetime import datetime, timezone

def process_file(file_path: str):
    if FlowRepository().get_processed_file(file_name=file_path) is not None:
        return f"File {file_path} has already been processed. Skipping."
    try:
        with open(file_path, 'r') as file:
            current_mpan_core_obj = None
            current_meter_obj = None
            for line in file:
                current_mpan_core_obj, current_meter_obj = read_line(line.strip(), current_mpan_core_obj, current_meter_obj)   

        #File processed add it to ProcessedFiles table
        FlowRepository().add_processed_file(file_name=file_path)
        return "File processed successfully."
    except Exception as e:
        return f"An error occurred while processing the file {file_path}: {str(e)}"

def read_line(line: str, current_mpan_core_obj: Optional[str], current_meter_obj: Optional[str]):
    data = line.split("|")
    if not data or len(data) == 0:
        raise Exception("Empty line encountered.")

    code = data[0]
    if code == Codes.MPAN_CORE.value:
        # Process MPAN core line
        return process_mpan_core(data)
    elif code == Codes.METER_READING_TYPE.value:
        # Process meter reading line
        return process_meter_reading(data, current_mpan_core_obj)
    elif code == Codes.REGISTER_READINGS.value:
        # Process register readings line
        process_register_reading(data, current_meter_obj)
        return None, None
    else:
        print(f"Unknown code {code} in line: {line}")
        return None, None


def process_mpan_core(data: [str]):
    if len(data) < 3 or not data[1] or not data[2]:
        print("Error: Incomplete MPAN core data.")
        raise Exception("Incomplete MPAN core data.")

    core = data[1]
    status = data[2]
    # Check if MPAN core already exists
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
    if len(data) < 3 or not data[1] or not data[2]:
        print("Error: Incomplete Meter reading data.")
        raise Exception("Incomplete Meter reading data.")
    
    meter_id = data[1]
    print(f"Meter ID: {meter_id}")
    reading_type = data[2]
    # Check if meter already exists
    if FlowRepository().get_meter_by_id(meter_id) is None:
        meter_obj, created =FlowRepository().get_or_create_meter(mpan_core_obj=current_mpan_core, meter_id=meter_id, meter_type=reading_type)
        return current_mpan_core, meter_obj
    else:
        print(f"Meter ID {meter_id} already exists in the database.")
        return current_mpan_core, FlowRepository().get_meter_by_id(meter_id)

def process_register_reading(data: [str], current_meter_obj: Optional[str]):
    if current_meter_obj is None:
        print("Error: No current Meter set for register reading.")
        return
    if len(data) < 8 or not data[1] or not data[2] or not data[3] or not data[7]:
        print("Error: Incomplete Register reading data.")
        raise Exception("Incomplete Register reading data.")

    register_id = data[1]
    reading_date_time = convert_to_datetime(data[2])
    register_reading = float(data[3])
    reset_date_time =  convert_to_datetime(data[4]) if data[4] else None 
    md_reset_count = int(data[5]) if data[5] else None
    reading_flag = data[6] if data[6] else None
    reading_method = data[7]
    # Check if reading already exists
    if FlowRepository().get_reading(current_meter_obj, register_id, reading_date_time) is None:
        FlowRepository().get_or_create_reading(
            meter_obj=current_meter_obj,
            meter_register_id=register_id,
            reading_date_time=reading_date_time,
            register_reading=register_reading,
            reset_date_time=reset_date_time,
            md_reset_count=md_reset_count,
            reading_flag=reading_flag,
            reading_method=reading_method
        )
        return None, None
    else:
        print(f"Reading for Register ID {register_id} at {reading_date_time} already exists in the database.")
        return None, None

        
def convert_to_datetime(date_str: str) -> datetime:
    print(f"Converting date string: {date_str}")
    return datetime.strptime(date_str, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)