from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .import_service import check_path, read_file, read_files_from_directory


# Create your views here.
def read(request, path: str):
    """
    View to handle file import requests.
    """

    path = "sample_data/DTC5259515123502080915D0010.uff"
    checked_path = check_path(path)
    print(checked_path)
    if checked_path == "directory":
        read_files_from_directory(path)
        return HttpResponse({"Success": "File Ingested"}, status=200)
    elif checked_path == "file":
        read_file(path)
        return HttpResponse({"Success": "File Ingested"}, status=200)
    else:
        return HttpResponse({"status": "Path not found"}, status=404)
    



    