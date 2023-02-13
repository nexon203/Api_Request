from django.shortcuts import render
from rest_framework import permissions
from apitest.models import TestModel, UserRequest
from apitest.serializers import TestModelSerializer
from rest_framework.views import APIView, Response
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests
import pandas as pd
import numpy as np
import hashlib
import logging


logging.basicConfig(filename="logs.log", level=logging.INFO)


# Make the API request
def index(request):
    return render(request, "index.html")


class DATAView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer = TestModelSerializer

    def get(self, request):
        data = TestModel.objects.all()
        datalist = list(data.values())
        return Response(datalist)


@csrf_exempt
def api_request(request, *ags, **kwargs):
    inputvalue = request.POST.get('inputapi')
    url = "http://localhost:8000/testdata/api/"
    context = {}
    time = timezone.now()
    
    try:
        response = requests.get(inputvalue)
        print("trying...")
        logging.info("API Request made to URL: %s", inputvalue)
        logging.info("API Request made on time: %s", time)
        logging.info("API Response Status code: %s", response.status_code)
        logging.info("API Response Content: %s", response.content)
        if response.status_code == 200:
            pd.options.display.float_format = '{:,.0f}'.format

            # Convert the response data to a pandas dataframe
            data = response.json()

            hash = hashlib.sha256(response.text.encode("utf-8")).hexdigest()

            headers = str(response.headers)

            df = pd.DataFrame(data)

            df = df.applymap(lambda x: str(int(x)) if type(x) == float and not np.isnan(x) else x)

            # Count the number of non-null values in each column
            non_null_counts = df.count()
            not_null_columns = dict()
            for column_name, value in non_null_counts.items():
                not_null_columns[column_name] = value

            # Count the number of null values in each column
            null_counts = df.isnull().sum()
            null_columns = dict()

            for column_name, value in null_counts.items():
                null_columns[column_name] = value

            objj = UserRequest(requests={'not_null_values': not_null_columns, 'null_values': null_columns, 'hash_value': hash, 'headers': headers})
            objj.save()

            # Print the results
            print("Columns    Total Values:\n", non_null_counts)
            print("\nColumns    Null Values:\n", null_counts)

            # Print the HTTP status code
            print("HTTP Status Code:", response.status_code)

            # Print the headers of the response
            print("Headers:", response.headers)

            # Print the body of the response
            print("Body:", response.text)

            # Print the hash value
            print("Hash Value:", hash)

            return render(request, 'data.html', {'df': df.to_dict('records')})

    except:
        logging.error("API Request made to URL: %s", inputvalue)
        logging.info("API Request made on time: %s", time)
        logging.error("API Response Status code: %s", "404")
        logging.error("API Response Content: %s", "Invalid API")
        context['message'] = 'Please Provide a Valid API'
        return render(request, 'index.html', context)
        
