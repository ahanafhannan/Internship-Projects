from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import requests
import re
def redirect(request):
    return HttpResponseRedirect('http://127.0.0.1:8000/playground/')