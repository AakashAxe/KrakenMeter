
from .models import MPANCore, Meter, Reading, ProcessedFiles
from django.utils import timezone


class FlowRepository:
    """DB access helpers for MPAN/Meter/Reading and processed-files."""

    def get_mpan(self, mpan_core: str) -> Optional[MPANCore]:
        return MPANCore.objects.filter(mpan_core=mpan_core).first()

    def get_or_create_mpan(self, mpan_core: str, bcs_validation_status: str) -> Tuple[MPANCore, bool]:
        return MPANCore.objects.get_or_create(mpan_core=mpan_core, defaults={"bcs_validation_status": bcs_validation_status})     

    def get_meter(self, mpan_core: str, meter_id: str) -> Optional[Meter]:
        return Meter.objects.filter(mpan_core__mpan_core=mpan_core, meter_id=meter_id).select_related("mpan_core").first()

    def get_meter_by_id(self, meter_id: str) -> Optional[Meter]:
        return Meter.objects.filter(meter_id=meter_id).select_related("mpan_core").first()

    def get_or_create_meter(self, mpan_core_obj: MPANCore, meter_id: str, meter_type: Optional[str] = None) -> Tuple[Meter, bool]:
        return Meter.objects.get_or_create(mpan_core=mpan_core_obj, meter_id=meter_id, defaults={"meter_type": meter_type or ""})

    def get_meters_for_mpan(self, mpan_core: str) -> List[Meter]:
        return list(Meter.objects.filter(mpan_core__mpan_core=mpan_core).select_related("mpan_core"))
    
    def get_readings(self, meter_id: str) -> List[Reading]:
        return list(Reading.objects.filter(meter__meter_id=meter_id).select_related("meter"))

    def get_reading(self, meter_id: str, meter_register_id: str, reading_date_time: str) -> Optional[Reading]:
        return Reading.objects.filter(meter__meter_id=meter_id, meter_register_id=meter_register_id, reading_date_time=reading_date_time).select_related("meter").first()

    def get_or_create_reading(self, meter_obj: Meter, meter_register_id: str, reading_date_time: str, register_reading: float,
                              reset_date_time: Optional[str] = None, md_reset_count: Optional[int] = None,
                              reading_flag: Optional[str] = None, reading_method: Optional[str] = None) -> Tuple[Reading, bool]:
        return Reading.objects.get_or_create(
            meter=meter_obj,
            meter_register_id=meter_register_id,
            reading_date_time=reading_date_time,
            reading_method=reading_method,
            register_reading=register_reading,
            defaults={
                "reset_date_time": reset_date_time,
                "md_reset_count": md_reset_count,
                "reading_flag": reading_flag,
            }
        )

    def add_processed_file(self, file_name: str) -> ProcessedFiles:
        return ProcessedFiles.objects.create(file_name=file_name, processed_at=timezone.now())

    def get_processed_file(self, file_name: str) -> Optional[ProcessedFiles]:
        return ProcessedFiles.objects.filter(file_name=file_name).first()