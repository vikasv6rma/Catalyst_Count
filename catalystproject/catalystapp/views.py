from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
# Python program to read JSON
import json
from django.core.files.storage import FileSystemStorage
import os
import pandas as pd
import mysql.connector


cwd = os.getcwd().replace("\\", "/") 
print("cwd--->",cwd)

# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import *

baseUrl = 'http://127.0.0.1:8000/'




@csrf_exempt
def uploadData(request):
    return render(request, "uploadData.html", {'baseUrl': baseUrl})


@csrf_exempt
def queryBuilder(request):
    distinctIndustryValues = CatalystCount.objects.values_list('industry', flat=True).distinct().order_by('industry')
    industryList = []
    for industry in distinctIndustryValues:
        industryList.append(industry.strip())
    # print("industryList ---->",industryList)

    yearFoundedList = list(CatalystCount.objects.values_list('year_founded', flat=True).distinct().order_by('year_founded'))
    print("yearFoundedList ---->",yearFoundedList)

    distinctLocalityValues = CatalystCount.objects.values_list('locality', flat=True).distinct()
    # print("distinctLocalityValues ---->",distinctLocalityValues)

    cityList = []
    stateList = []

    for locality in distinctLocalityValues:
        if locality.lower().strip() != "nan":
            # if locality not in cityList and 
            locality = locality.strip().split(",")
            if locality[0].strip() not in cityList:
                cityList.append(locality[0].strip())
            if locality[1].strip() not in stateList:
                stateList.append(locality[1].strip())

    cityList.sort()
    stateList.sort()
    # print("cityList ---->",cityList)
    print("stateList ---->",stateList)

    distinctCountryValues = CatalystCount.objects.values_list('country', flat=True).distinct().order_by('country')
    countryList = []
    for country in distinctCountryValues:
        if country.lower().strip() != "nan":
            countryList.append(country.strip())
    # print("countryList ---->",countryList)


    distinctCurrentEmpValues = CatalystCount.objects.values_list('current_emp_estimate', flat=True).distinct()
    currentEmpList = []
    for currentEmp in distinctCurrentEmpValues:
        currentEmpList.append(currentEmp.strip())
    # print("currentEmpList ---->",currentEmpList)


    distinctTotalEmpValues = CatalystCount.objects.values_list('total_emp_estimate', flat=True).distinct()
    currentTotalEmpList = []
    for currentTotalEmp in distinctTotalEmpValues:
        currentTotalEmpList.append(currentTotalEmp.strip())
    # print("currentTotalEmpList ---->",currentTotalEmpList)

    return render(request, "queryBuilder.html", {'baseUrl': baseUrl, 'industryList':industryList, 'yearFoundedList':yearFoundedList,'cityList':cityList,'stateList':stateList ,'countryList':countryList, 'currentEmpList':currentEmpList, 'currentTotalEmpList':currentTotalEmpList})





@csrf_exempt
def users(request):
    userDetails = Users.objects.all().values().order_by('-id')
    print("userDetails ---->",userDetails)
    return render(request, "users.html", {'baseUrl': baseUrl, 'userDetails':userDetails})



@csrf_exempt
def addUser(request):
    print("***************** addUser() ******************")
    if request.method == 'POST':
        response = {}
        jsonData = request.POST.get('payload')
        parsedData = json.loads(jsonData)
        print("parsedData ---->",parsedData)

        userName= parsedData.get('userName')
        print("userName ----->",userName)

        emailId= parsedData.get('emailId')
        print("emailId ----->",emailId)

        isActive= parsedData.get('isActive')
        print("isActive ----->",isActive)

        try:
            Users.objects.create(name = userName, email_id = emailId.lower(), is_active = isActive).save()
            response["status"]=True
            response["message"]= "New user added successfully!"
            return JsonResponse(response)

        except Exception as e :
            print("error ----->",str(e))
            response["status"]=False
            response['message'] = 'Something went wrong'
            return JsonResponse(response)


from django.db import connection

def queryExecuter(query):
    print("******** queryExecuter() *********")
    try:
        # print("--------- try_queryExecuted ---------")
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        # print("--------- except_exceptionError ---------")
        print("error ---->",e)

    finally:
        # print("--------- finally_connectionClosed() ---------")
        cursor.close()







@csrf_exempt
def uploadCSVFile(request):
    print(f"[{datetime.now()}]: -------uploadCSVFile()----------------->")
    response = {}
    try:
        if request.method=='POST':
            csvFile = request.FILES.get('csvFile')
            print("csvFile --->",csvFile)

            if csvFile is not None:
                UPLOAD_FOLDER= f"{cwd}/media/files"
                print("UPLOAD_FOLDER --->",UPLOAD_FOLDER)
                fs = FileSystemStorage(location=UPLOAD_FOLDER)
                isExist = os.path.exists(UPLOAD_FOLDER)
                print("isExist ---->",isExist)

                print("csvFile name ---->",csvFile.name)
                    
                if not isExist:
                    print("********** if ************")
                    os.makedirs(UPLOAD_FOLDER)
                    print("The new directory is created!")
                    file = fs.save(csvFile.name, csvFile)
                    print("file --->",file)
                    fileurl = fs.url(file)

                else:
                    print("********** else ************")
                    filePathExist = f"{UPLOAD_FOLDER}/{csvFile.name}"
                    isfilePathExist = os.path.exists(filePathExist)
                    print("isfilePathExist ---->",isfilePathExist)
                    
                    if isfilePathExist:
                        os.remove(filePathExist)

                    file = fs.save(csvFile.name, csvFile)
                    fileurl = fs.url(file)

                # MySQL database connection settings
                db_config = {
                    'host': '127.0.0.1',
                    'user': 'root',
                    'password': '',
                    'database': 'Catalyst'
                }

                # CSV file path and chunk size
                csv_file_path = f'{cwd}/media/files/{file}'
                chunk_size = 1000

                # Establish database connection
                db_connection = mysql.connector.connect(**db_config)
                cursor = db_connection.cursor()

                # Read CSV data in chunks and insert into the database
                csv_file = open(csv_file_path, 'r', newline='' ,encoding='latin-1') 

                for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                    # Preparing SQL Insert Query for this chunk
                    #-------------------------- Columns Name --------------------------
                    columns = ','.join(chunk.columns)
                    print("columns ---->",columns)
                    noOfColumns = list(chunk.columns)[-1].split(":")[1]
                    intNoOfColumns = int(noOfColumns)
                    tupleColumns = tuple(chunk.columns[:intNoOfColumns])
                    print("tupleColumns ---->",tupleColumns)
                    
                    listColumns = []
                    for data in tupleColumns:
                        listColumns.append("`" + data + "`")
                    print("listColumns ----->",listColumns)

                    backTickColumn  = ','.join(listColumns)
                    print("backTickColumn --->",backTickColumn)

                    #-------------------------- Injection Values --------------------------
                    values = ','.join(['%s'] * len(chunk.columns))
                    # print("values ---->",values)
                    valuesList = values.split(",")[:intNoOfColumns]
                    # print("valuesList ---->",valuesList)

                    valuesPlaneTxt = ','.join(valuesList)
                    print("valuesPlaneTxt ---->",valuesPlaneTxt)

                    insertQuery = f"INSERT INTO `catalyst_count` ({backTickColumn}) VALUES ({valuesPlaneTxt})"
                    print("insertQuery --->",insertQuery)
                    
                    for index, row in chunk.iterrows():
                        print("row ---->",row)
                        valuesTuple = tuple(row)
                        print("valuesTuple ---->",valuesTuple)
                        valuesList = []
                        for i in valuesTuple:
                            valuesList.append(str(i).strip())
        
                        finalValuesTuple = tuple(valuesList[0:intNoOfColumns])
                        print("finalValuesTuple ---->",finalValuesTuple)
                        cursor.execute(insertQuery, finalValuesTuple)
                    
                    db_connection.commit()  # Commit after each chunk (Per chunk 1000 data exist)
                    print("************* First (1000 data) Chunk Inserted *********************")

                cursor.close()
                db_connection.close()

                print("************* Data insertion completed ********************")
                response['status'] = True
                response['message'] = 'File uploaded successfully!'
                response['fileName'] = csvFile
                print("RESPONSE --->",response)
                return HttpResponse(json.dumps(response,default=str))

            else: 
                response['status'] = False
                response['message'] = 'No file found!'
                response['fileName'] = ""
                print("RESPONSE --->",response)
                return HttpResponse(json.dumps(response,default=str))

    except Exception as e:
        print("error ---->",e)
        response['status'] = False
        response['message'] = 'Something went wrong'
        print("RESPONSE --->",response)
        return HttpResponse(json.dumps(response,default=str))
    

##################################################################################################

@csrf_exempt
def queryDateFilter(request):
    try:
        if request.method=='POST':
            response= {}
            # cursor = connection.cursor()

            parsedData = json.loads(request.POST.get('payload'))
            print("parsedData ---->",parsedData)

            industry = parsedData.get('industry')
            print("industry---->", industry)

            yearFounded = parsedData.get("yearFounded")
            print("yearFounded---->", yearFounded)

            city = parsedData.get("city")
            print("city---->", city)

            state = parsedData.get("state")
            print("state---->", state)

            country = parsedData.get("country")
            print("country---->", country)

            if city=="":
                city= None
            if state=="":
                state= None

        
            query = "SELECT count(*) FROM `catalyst_count`"
            where = ""
            orText = "or"
            paramCount = 0
            # orderbyDescQuery = " order by userTransactions_id desc"

            if len(industry.strip()) != 0 or len(yearFounded.strip()) != 0 or city != None or state != None or len(country.strip()) != 0:
                where = "where"
                query = query + " " + where + " "

                if len(industry) != 0:
                    query = query + " " + f"INDUSTRY= '{industry.strip()}'"
                    paramCount = paramCount + 1

                if len(yearFounded) != 0:
                    if paramCount > 0:
                        query = query + " " + orText + " "
                    query = query + " " + f"YEAR_FOUNDED= '{yearFounded.strip()}'"
                    paramCount = paramCount + 1

                if city != None or state != None:
                    if paramCount > 0:
                        query = query + " " + orText + " "
                    query = query + " " + f"(LOCALITY LIKE '%{city}%' or LOCALITY LIKE '%{state}%')"
                    paramCount = paramCount + 1
                

                if len(country) != 0:
                    if paramCount > 0:
                        query = query + " " + orText + " "
                    query = query + " " + f"COUNTRY= '{country.strip()}'"
                    paramCount = paramCount + 1


                print("QUERY--->", query)

                result = queryExecuter(query)
                
                countResult = result[0][0]
                print("countResult --->", countResult)

                response["status"]=True
                response["message"]= f"{countResult} records found for the query"
                return JsonResponse(response)
        
    
    except Exception as e:
        print("error ---->",e)
        response['status'] = False
        response['message'] = 'Something went wrong'
        print("RESPONSE --->",response)
        return JsonResponse(response)







   

