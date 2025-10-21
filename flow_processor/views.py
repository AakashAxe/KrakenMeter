from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .import_service import check_path, read_file, read_files_from_directory


# Create your views here.
def read(request):
    """
    View to handle file import requests.
    """
    testPath = "sample_data/DTC5259515123502080915D0010.uff"
    checked_path = check_path(testPath)
    print(checked_path)
    if checked_path == "directory":
        read_files_from_directory(testPath)
        return HttpResponse({"status": "Path not found"}, status=400)
    elif checked_path == "file":
        read_file(testPath)
        return HttpResponse({"status": "Path not found"}, status=400)
    else:
        return HttpResponse({"status": "Path not found"}, status=404)
    



    