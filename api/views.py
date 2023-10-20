
import os
import time
from django.shortcuts import render, HttpResponse, redirect
from .models import uploadFileModel
from .forms import uploadFileForms

from .main import *
from .config import public_key,secret_key


def performTask(request):
    if request.method == "POST":
        form = uploadFileForms(request.POST,request.FILES)
        files = request.FILES.getlist('file')
        opertion = request.POST['operations']

        # if str(files[0]).split(".")[1] != "pdf":
        #     return HttpResponse("invalid file type , please select pdf")
        # else:
        serveFileName = []
        ## get authentication and server to proces files...............
        access_token = getAuthenticationToken(public_key, secret_key)
        headers = {'Authorization': f'Bearer {access_token}'}
        server, taskID = getServerTaskID(headers, opertion)

        for file in files:
            upload = uploadFileModel.objects.create(myfile=file)
            upload.save()
            file_path = "G:\\MyCodeprojects\\Django\\iLovePdfAPI\\media\\"+str(file)
            server_filename = uploadFileToServer(headers, file_path, server, taskID)
            serveFileName.append(server_filename)

        print("All file uploaded......")
        fileProcessing(headers, server, taskID, serveFileName, opertion)
        downloadProcessFile(headers, taskID, server, str(file), opertion)

        for file in files:
            file_path = "G:\\MyCodeprojects\\Django\\iLovePdfAPI\\media\\" + str(file)
            os.remove(file_path)
        return HttpResponse("Output file saved in Output folder.....\nThank You For using...")
    else:
        form = uploadFileForms()
    return render(request,"uploadFile.html",{'form':form})

