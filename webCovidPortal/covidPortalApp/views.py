from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

from rest_framework.authentication import get_authorization_header, BaseAuthentication, TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.core.mail import send_mail

from operator import itemgetter
import hashlib
import pandas as pd
import shutil
import io
import os
import sys
import json
import traceback
import numpy as np
import seaborn as sns
import gzip
import nibabel as nib
import subprocess
from django import forms
from PIL import Image
import datetime
import base64
from glob import glob
import jwt
import datetime
from rest_framework.authentication import get_authorization_header
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
import json
import glob
import matplotlib.pyplot as plt

from covidPortalApp.models import *
from covidPortalApp.covidPortalAppObjs import *
from covidPortalApp.covidPortalAppConstants import *
from django.contrib.auth import authenticate
import time
import paramiko

from conf import *
import asyncio, asyncssh, sys

from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk)+str(timestamp);
        # return (
        #     six.text_type(user.pk) + six.text_type(timestamp) +
        #     six.text_type(user.profile.email_confirmed)
        # )

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

def monitorJobs(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        userName = data["userName"]
        users = User.objects.filter(username = userName)
        if len(users) > 0:
            user = users[0]
            uploadFolders = uploadFolder.objects.filter(user = user)
            uploadFolders = [x for x in uploadFolders if x.status != 'Uploaded' and s.status != 'Analysis Completed']
            uploadFolderJSON = [{'name':x.name,'chksum':x.chksum,'user':str(x.user),
            'description':x.description, 'id':x.id,'status':x.status,
            'fileName':x.fileName,'uploadedDate':x.uploadedDate.strftime('%Y-%m-%d'),
            'analysisProtocol':x.analysisProtocol,
            'fileType':uploadFolder.fileType,
            'analysisSubmittedDate':x.analysisSubmittedDate.strftime('%Y-%m-%d') if x.analysisSubmittedDate else '',
            'rowColor':statusColorMap[x.status], "resultsAvailable":"no"} for x in uploadFolders]
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps(uploadFolderJSON), content_type="application/json")

def getUserProfile(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter (username = username)
        if len(users) > 0:
            user = users[0]
            covidUser = CovidUser.objects.filter(user = user)[0]
            userJSON = {"username":covidUser.user.username, "addressLine1":covidUser.addressLine1, "addressLine2":covidUser.addressLine2, "city":covidUser.city, "state":covidUser.state, "zipCode":covidUser.zipCode, "phoneNumber":covidUser.phoneNumber, "email":covidUser.user.email}
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps(userJSON), content_type="application/json")

def updateUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter (username = username)
        if len(users) > 0:
            user = users[0]
            covidUser = CovidUser.objects.filter(user = user)[0]

            covidUser.addressLine1 = data["addressLine1"]
            covidUser.addressLine2 = data["addressLine1"]
            covidUser.city = data["city"]
            covidUser.state = data["state"]
            covidUser.zipCode = data["zipCode"]
            covidUser.phoneNumber = data["phoneNumber"]

            covidUser.save()

            userJSON = {"username":covidUser.user.username, "addressLine1":covidUser.addressLine1, "addressLine2":covidUser.addressLine2, "city":covidUser.city, "state":covidUser.state, "zipCode":covidUser.zipCode, "phoneNumber":covidUser.phoneNumber, "email":covidUser.user.email}
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed to update profile.", "user":{} } ), content_type="application/json")
    return HttpResponse(json.dumps({"message":"User profile updated.", "user":userJSON}), content_type="application/json")

def signupUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        email = data["email"]

        addressLine1 = data["addressLine1"]
        addressLine2 = data["addressLine2"]
        city = data["city"]
        state = data["state"]
        zipCode = data["zipCode"]
        phoneNumber = data["phoneNumber"]
        print(" username " + username + " password " + password + " email " + email)
        users = User.objects.filter(username = username)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
        else:
            user = User.objects.create_user(username, email, password)

            covidUser = CovidUser ()
            covidUser.user = user
            covidUser.addressLine1 = addressLine1
            covidUser.addressLine2 = addressLine2
            covidUser.city = city
            covidUser.state = state
            covidUser.zipCode = zipCode
            covidUser.phoneNumber = phoneNumber

            covidUser.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def checkUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        users = User.objects.filter(username = username)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def emailPasswordLink(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data["email"]
        print ( " email = " + email )
        account_activation_token = AccountActivationTokenGenerator()
        users = User.objects.filter(email = email)
        if len(users) > 0:
            send_mail(
                'Reset password ' + str(account_activation_token),
                'Please enter password',
                'mitra.siddhartha@gmail.com',
                [email],
                fail_silently=False,
            )
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"An error occured."}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Password resert link emailed."}), content_type="application/json")

def resetPassword(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]

        users = User.objects.filter(username = username)
        if len(users) > 0:
            user = users[0]
            user.set_password(password)
            user.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"An error occured."}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Password resert link emailed."}), content_type="application/json")

def checkEmail(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data["email"]
        users = User.objects.filter(email = email)
        if len(users) > 0:
            return HttpResponse(json.dumps({"message":"Exists"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

def checkLogin(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data["username"]
        password = data["password"]
        print('username='+str(username)+" password="+str(password))
        userString =""
        user = authenticate(request, username=username, password=password)
        if user is None:
            return HttpResponse(json.dumps({"message":"Invalid"}), content_type="application/json")
    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Invalid"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Valid"}), content_type="application/json")

def logoutUser(request):
    try:

        username = request.POST.get("logoutUser","")
        print('username='+str(username))

        logout(request, user)
        userString=json.dumps({"id":"0","firstName":"","lastName":"","email":""})
        print ( "userString =  " + str(userString))

    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(userString), content_type="application/json")

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def submitUploadFile(request):
    try:
        print("begin upload")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])
        #jwt.decode(encoded_jwt
        print(auth)
        md5 = hashlib.md5()
        print ( " items = " + str([(k,f) for k, f in request.FILES.items()]))
        # f = request.FILES["name"]
        f = request.FILES['file']

        print(" start upload ")

        with open(settings.UPLOAD_FOLDER + str(f.name) , 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
                    md5.update(chunk)

        print(" end upload ")

        chksum = md5.hexdigest()
        print (chksum)

        if f.name.find("nii.gz") != -1:
            shutil.move(settings.UPLOAD_FOLDER + str(f.name), settings.UPLOAD_FOLDER + str(chksum) + ".nii.gz")
        elif f.name.find("tar.gz") != -1:
            shutil.move(settings.UPLOAD_FOLDER + str(f.name), settings.UPLOAD_FOLDER + str(chksum) + ".tar.gz")
        elif f.name.find("zip") != -1:
            shutil.move(settings.UPLOAD_FOLDER + str(f.name), settings.UPLOAD_FOLDER + str(chksum) + ".zip")
        else:
            shutil.move(settings.UPLOAD_FOLDER + str(f.name), settings.UPLOAD_FOLDER + str(chksum) )

        print(" moved file ")

        adminUser = User.objects.get(id=user_id)
        uploadFolder = UploadFolder(name=str(f.name), description = str(f.name), chksum=chksum, user= adminUser, status = "Uploaded", uploadedDate=datetime.datetime.now())
        uploadFolder.save()
        outf = open(settings.UPLOAD_FOLDER + str(chksum) + ".user", "w")
        outf.write(adminUser.username)
        outf.close()

        print(" created user file ")

        uploadFolderJson = {'id':uploadFolder.id, 'name':uploadFolder.name,'chksum':uploadFolder.chksum,'user':str(uploadFolder.user),'description':uploadFolder.description,
        'status':uploadFolder.status,
        'fileName':uploadFolder.fileName,'uploadedDate':uploadFolder.uploadedDate.strftime('%Y-%m-%d'),
        'analysisProtocol':uploadFolder.analysisProtocol,
        'fileType':uploadFolder.fileType,
        'analysisSubmittedDate':uploadFolder.analysisSubmittedDate.strftime('%Y-%m-%d') if uploadFolder.analysisSubmittedDate else '',
        'rowColor':statusColorMap[uploadFolder.status]}

    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({ }), content_type="application/json")
    return HttpResponse(json.dumps(uploadFolderJson), content_type="application/json")

def updateDatafileName(request):
    try:
        print("update data file name")
        data = json.loads(request.body.decode('utf-8'))

        datafileName = data["datafileName"]
        uploadFolderId = int(data["uploadFolderId"])

        uploadFolder = UploadFolder.objects.get(pk = uploadFolderId)
        uploadFolder.fileName = datafileName
        uploadFolder.save()

    except:
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"message":"Failed"}), content_type="application/json")
    return HttpResponse(json.dumps({"message":"Success"}), content_type="application/json")

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def searchUploadedFolders(request):
    try:
        searchString = request.GET.get("searchString","0")
        print(searchString)
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        userId = int(tokendata['user_id'])
        print(userId)
        user = User.objects.get(pk = userId)
        fileList = UploadFolder.objects.filter(user = user)
        print(" search = " + searchString)
        if searchString != '':
            fileList = [{'name':x.name,'chksum':x.chksum,'user':str(x.user),'description':x.description, 'id':x.id,'status':x.status, 'rowColor':statusColorMap[x.status]} for x in fileList if x.name.find(searchString) != -1]
        else:
            fileList = [{'name':x.name,'chksum':x.chksum,'user':str(x.user),'description':x.description, 'id':x.id,'status':x.status, 'rowColor':statusColorMap[x.status]} for x in fileList]

        print(fileList)
    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(fileList), content_type="application/json")

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def listUploadedFiles(request):
    try:
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        userId = int(tokendata['user_id'])
        print(userId)
        user = User.objects.get(pk = userId)
        fileList = UploadFolder.objects.filter(user = user)
        fileObjList = fileList
        fileList = [{'name':x.name,'chksum':x.chksum,'user':str(x.user),'description':x.description, 'id':x.id,'status':x.status, 'rowColor':statusColorMap[x.status], "resultsAvailable":"no"} for x in fileList]
        for index, fileObj in enumerate(fileList):
            if os.path.exists("/data/Synology_Scans/Processing/Ants/" + user.username + "/" + fileObj['chksum'] + "/T1/Completed/Brain_Extraction.completed") and os.path.exists("/data/Synology_Scans/Processing/Ants/" + user.username + "/" + fileObj['chksum'] + "/T1/Completed/Prediction.completed"):
              fileObj["resultsAvailable"] = "yes"
              fileObj["rowColor"] = statusColorMap["Score Calculated"]
              fileObjList[index].status = "Score Calculated"
              if os.path.exists("/data/Synology_Scans/Processing/Ants/" + user.username + "/" + fileObj['chksum'] + "/T1/Completed/ROI.completed"):
                fileObj["rowColor"] = statusColorMap["Analysis Completed"]
                fileObjList[index].status = "Analysis Completed"
              fileObjList[index].save()
    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(fileList), content_type="application/json")

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def getRunningJobs(request):
    try:
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        userId = int(tokendata['user_id'])
        print(userId)
        user = User.objects.get(pk = userId)

    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(fileList), content_type="application/json")


# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def deleteDatafile(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        datafileId = data["datafileId"]
        print(" datafileId " + datafileId)
        uploadFolder = UploadFolder.objects.get(pk = int(datafileId) )
        if os.path.exists("/data/Synology_Scans/Processing/Ants/" + uploadFolder.user.username + "/" + uploadFolder.chksum ):
            shutil.rmtree("/data/Synology_Scans/Processing/Ants/" + uploadFolder.user.username + "/" + uploadFolder.chksum)
        uploadFolder.delete()
    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"File delete failed."})

    return JsonResponse({"message":"File deleted."})

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def getDatafile(request):
    try:
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])

        submitUser = User.objects.get(id=user_id)

    except:
        traceback.print_exc(file=sys.stdout)
    return JsonResponse(uploadFolderJSON)

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def fetchAllComments(request):
    try:

        print(" ******* in fetch comments ")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])

        submitUser = User.objects.get(id=user_id)

        data = json.loads(request.body.decode('utf-8'))

        uploadFolderId = data["uploadFolderId"]
        uploadFolder = UploadFolder.objects.get(pk = int(uploadFolderId) )

        comments = Comment.objects.filter(uploadFolder= uploadFolder)

    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in fetching comment."})

    return JsonResponse(commentsJSON, safe=False)

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def fetchCommentsByLocation(request):
    try:

        print(" ******* in fetch comments ")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])

        submitUser = User.objects.get(id=user_id)

        data = json.loads(request.body.decode('utf-8'))

    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in fetching comment."})

    return JsonResponse(commentsJSON)

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def saveComment(request):
    try:

        print(" ******* in save comment ")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])

        submitUser = User.objects.get(id=user_id)

        data = json.loads(request.body.decode('utf-8'))

        uploadFolderId = data["uploadFolderId"]
        uploadFolder = UploadFolder.objects.get(pk = int(uploadFolderId) )

    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in saving comment."})

    return JsonResponse({"message":"Comment saved."})

def terminateJob(request):
    try:

        print(" ******* in submit analysis 0000000000000000 ")
        print("begin upload")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])

        submitUser = User.objects.get(id=user_id)

        data = json.loads(request.body.decode('utf-8'))
        datafileId = data["datafileId"]

        outf = open(settings.UPLOAD_FOLDER + uploadFolder.chksum + ".analysis", "w")
        outf.write(analysisProtocol)
        outf.close()

        uploadFolder.status = "Analysis Terminated"
        # uploadFolder.analysisSubmittedDate = datetime.datetime.now()

        uploadFolder.save()
    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in job termination.", "uploadFolder":{}})

    return JsonResponse({"message":"Job successfully terminated.", "uploadFolder":uploadFolderJSON})

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
def submitAnalysis(request):
    try:

        print(" ******* in submit analysis 0000000000000000 ")
        print("begin upload")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")
        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])
    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in job submission.", "uploadFolder":{}})

    return JsonResponse({"message":"Job successfully submitted.", "uploadFolder":uploadFolderJSON})

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication ])
# @permission_classes([IsAuthenticated])
def getMutationData(request):
    mutationData = {}
    try:
        print (" in overlay ")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")

        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])
        df = pf.from_csv()
    except:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({"message":"Error in job submission.", "uploadFolder":{}})

    return JsonResponse({"message":"Job successfully submitted.", "uploadFolder":uploadFolderJSON})

def getOverlayData(request):
    brainViewerData = {}
    try:
        print (" in overlay ")
    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(brainViewerData), content_type='application/json')

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication ])
# @permission_classes([IsAuthenticated])

def getFullScreenOverlayData(request):
    brainViewerData = {}
    try:
        print (" in full screen overlay ")
        auth = get_authorization_header(request).split()
        tokendata = auth[1].decode("utf-8")

        print(tokendata)
        tokendata = jwt.decode(auth[1].decode("utf-8"),settings.SECRET_KEY, algorithms=['HS256'])
        user_id = int(tokendata['user_id'])
    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(brainViewerData), content_type='application/json')

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication ])
# @permission_classes([IsAuthenticated])
def listSequences(request):
    sequenceObjList = {}
    sequenceResultObj = {}
    try:
        # /home/siddhartha/Downloads/sequence.csv
        # /home/siddhartha/Downloads/sequencerecord.csv
        df = pd.read_csv('data/db_inserts/sequencerecord.csv', index_col=None, na_filter=False)
        # df = df[:6]
        print(df.columns)
        # df.fillna(" ").replace(":"," ")
        # accession	organism	collection_date	country	host	isolation_source	coded_by	protein_id	taxon_id	isolate

        sequenceObjList = [
        {"id":row["id"], "accession":row["accession"],
         "organism":row["organism"], "collection_date":row["collection_date"], "country":row["country"], "host":row["host"], "isolation_source":row["isolation_source"], "coded_by":row["coded_by"],
         "protein_id":row["protein_id"],"taxon_id":row["taxon_id"],"isolate":row["isolate"] }
          for index, row in df.iterrows()]

        sequenceResultObj = {"sequenceTableColumns":list(df.columns), "sequenceObjList":sequenceObjList}

    except:
        traceback.print_exc(file=sys.stdout)
    return HttpResponse(json.dumps(sequenceResultObj), content_type='application/json')

# @api_view([ "GET", "POST"])
# @permission_classes((IsAuthenticated, ))
# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication ])
# @permission_classes([IsAuthenticated])
def showAlignment(request):
    alignment = {}
    alignmentObjList = []
    try:

        print (" alignment ")

        residueColorMap = {
                        "A":"#00FF00",
                        "G":"#00FF00",
                        "C":"#98FFB3",
                        "D":"#00FA6D",
                        "E":"#00FA6D",
                        "N":"#00FA6D",
                        "Q":"#00FA6D",
                        "I":"#0000FF",
                        "L":"#0000FF",
                        "M":"#0000FF",
                        "V":"#0000FF",
                        "F":"#FF6575",
                        "W":"#FF6575",
                        "Y":"#FF6575",
                        "H":"#AFD7FF",
                        "K":"#FFA500",
                        "R":"#FFA500",
                        "P":"#FF0065",
                        "S":"#FF0000",
                        "T":"#FF0000",
                        "-":"#FFFFFF"
                        }

        alignmentMap = {
                 "first": "--------MFVFLVLLP--------------LVSSQCVNLT---------TRTQ-------LPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFH--AIHVSGTNG-------------TKRFDNPVLPFNDGVYFASTEKSNI-------------------IRGWIFGTTLDSKTQSLLI--VN--------------------NATNVVIKVCE---------FQFCNDPFLGVYYHKN-NKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGN-F--KNLREFVFKNIDGYFKIYSKHTPINLV----RDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTP----GDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRF-PNITN-LCPFGEVF--NATRFASVYAWNRKRISNCVADYSVLYNS-ASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKV---------------------------GGNYNYLYRLFRKSNLKPFERDISTEIYQ-------------------AGSTPCNGVEGFNCYF---------------------------PLQSY--------------------------GFQ-----------------------------------P-----TNGVGYQPYRVVVLSFELLHAPATVCGPK-K-----STNLVKNKCVNFNFNGLTGTGVLTE-SNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYST-----GSNVFQTRAGCLIGAEHVNN----SYECDIPIGAGICASYQTQTNSPRRA-RSVA-----SQSIIAYTMSLG-AENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIY--KTPPIK----DFGGFNFSQILPDPS-----------KPSKRSFIEDLLFNKVTLADAGFIKQYGDCLG---DIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHD---GKAHFPREGVFVSNGT----------",
                 "second": "MKIL---IFAFLANLAK---------------AQEGCGIIS---------RKPQ-------PKMAQVSSSRRGVYYNDDIFRSDVLHLTQDYFLPFDSNLTQYF--SLNVD-SDR-------------YTYFDNPILDFGDGVYFAATEKSNV-------------------IRGWIFGSSFDNTTQSAVI--VN--------------------NSTHIIIRVCN---------FNLCKEPMYTVSRG---TQ----QNAWVYQSAFNCTYDRVEKSFQLDTTP-KTGNF--KDLREYVFKNRDGFLSVYQTYTAVNLP----RGLPTGFSVLKPILKLPFGINITSYRVVMAMFSQ----------TTSNFLPESAAYYVGNLKYSTFMLRFNENGTITDAVDCSQNPLAELKCTIKNFNVDKGIYQTSNFRVSPTQEVIRF-PNITN-RCPFDKVF--NATRFPNVYAWERTKISDCVADYTVLYNS-TSFSTFKCYGVSPSKLIDLCFTSVYADTFLIRSSEVRQVAPGETGVIADYNYKLPDDFTGCVIAWNTAKHDT--------------------------------GNYYYRSHRKTKLKPFERDLSSDD--------------------------------GNGVY---------------------------TLSTY--------------------------DFN-----------------------------------P-----NVPVAYQATRVVVLSFELLNAPATVCGPK-L-----STELVKNQCVNFNFNGLKGTGVLTS-SSKRFQSFQQFGRDTSDFTDSVRDPQTLEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVPTAIRADQLTPAWRVYST-----GVNVFQTQAGCLIGAEHVNA----SYECDIPIGAGICASYHTASV----L-RSTG-----QKSIVAYTMSLG-AENSIAYANNSIAIPTNFSISVTTEVMPVSMAKTAVDCTMYICGDSLECSNLLLQYGSFCTQLNRALTGIAIEQDKNTQEVFAQVKQMY--KTPAIK----DFGGFNFSQILPDPS-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGDCLG---DVSARDLICAQKFNGLTVLPPLLTDDMVAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQESLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPSQEKNFTTAPAICHE---GKAYFPREGVFVSNGT----------",
                 'third': "----MFIFLLFLTLTSG--------------SDLDRCTTFD---------DVQA-------PNYTQHTSSMRGVYYPDEIFRSDTLYLTQDLFLPFYSNVTGFH--TINH--------------------TFGNPVIPFKDGIYFAATEKSNV-------------------VRGWVFGSTMNNKSQSVII--IN--------------------NSTNVVIRACN---------FELCDNPFFAVSKP-M-GT---QTHTMIFDNAFNCTFEYISDAFSLDVSE-KSGNF--KHLREFVFKNKDGFLYVYKGYQPIDVV----RDLPSGFNTLKPIFKLPLGINITNFRAILTAFSP----------AQDIWGTSAAAYFVGYLKPTTFMLKYDENGTITDAVDCSQNPLAELKCSVKSFEIDKGIYQTSNFRVVPSGDVVRF-PNITN-LCPFGEVF--NATKFPSVYAWERKKISNCVADYSVLYNS-TFFSTFKCYGVSATKLNDLCFSNVYADSFVVKGDDVRQIAPGQTGVIADYNYKLPDDFMGCVLAWNTRNIDATS---------------------------TGNYNYKYRYLRHGKLRPFERDISNVPFS-------------------PDGKPCT-PPALNCYW---------------------------PLNDY--------------------------GFY-----------------------------------T-----TTGIGYQPYRVVVLSFELLNAPATVCGPK-L-----STDLIKNQCVNFNFNGLTGTGVLTP-SSKRFQPFQQFGRDVSDFTDSVRDPKTSEILDISPCSFGGVSVITPGTNASSEVAVLYQDVNCTDVSTAIHADQLTPAWRIYST-----GNNVFQTQAGCLIGAEHVDT----SYECDIPIGAGICASYHTVSL----L-RSTS-----QKSIVAYTMSLG-ADSSIAYSNNTIAIPTNFSISITTEVMPVSMAKTSVDCNMYICGDSTECANLLLQYGSFCTQLNRALSGIAAEQDRNTREVFAQVKQMY--KTPTLK----YFGGFNFSQILPDPL-----------KPTKRSFIEDLLFNKVTLADAGFMKQYGECLG---DINARDLICAQKFNGLTVLPPLLTDDMIAAYTAALVSGTATAGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKQIANQFNKAISQIQESLTTTSTALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDKVEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQAAPHGVVFLHVTYVPSQERNFTTAPAICHE---GKAYFPREGVFVFNGT----------",
                }
        for k,v in alignmentMap.items():

            residueObjList = [{"residueValue":x,"residueColor":residueColorMap[x], "residuePosition":i} for i,x in enumerate(v)]
            alignmentObj = {"label":k,"residueObjList":residueObjList}
            alignmentObjList.append(alignmentObj)
            print (alignmentObjList)


    except:
        traceback.print_exc(file=sys.stdout)

    return HttpResponse(json.dumps(alignmentObjList), content_type='application/json')
