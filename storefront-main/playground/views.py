from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import requests
import re
# Create your views here.

base_url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/"

user_name = "sandboxTokenizedUser02"	
password = "sandboxTokenizedUser02@12345"
app_key = "4f6o0cjiki2rfm34kfdadl1eqq"
app_secret = "2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b"
grant_response = None
create_response = None
create_agreement_response= None
id_token = None
agreementID=None
agreementStatus=None
exec
def homepage(request):
    if agreementID == None:
        return render(request, 'index.html', {'name':'mosh'})
    else:
        return render(request, 'index  agreement.html', {'name':'mosh'})
def payment(request):
    if agreementID == None:
        return render(request, 'homepage.html', {'name':'mosh'})
    else:
        return render(request, 'agreement_homepage.html', {'name':'mosh'})
def grant(request):
    global base_url,user_name,password,app_key,app_secret,grant_response,id_token
    grant_URL = f"{base_url}/tokenized/checkout/token/grant"
    
    grant_request_head = {
        'Content-Type' : "application/json",
        'Accept' :"application/json",
        'username' : user_name,
        'password' :password
    }
    
    grant_request_parameter = {
        'app_key' : app_key,
        'app_secret' : app_secret
    }
    
    response = requests.post(grant_URL,headers=grant_request_head,json=grant_request_parameter)
    grant_response = response.json()
    id_token = grant_response.get("id_token")
    
    create_url = f'{base_url}/tokenized/checkout/create'
    print(grant_response.get('id_token'))
    create_request_head = {
        'Content-Type' : "application/json",
        'Accept' :"application/json",
        'Authorization' : grant_response.get("id_token"),
        'X-App-Key' : app_key
    }
    create_request_parameter = {
        'mode' : "0011",
        'payerReference' : "01619777283",
        'callbackURL' : 'http://127.0.0.1:8000/playground/execute',
        'amount' : '10',
        'currency' : 'BDT',
        'intent' : 'sale',
        'merchantInvoiceNumber' : '01992939478',
        'merchantAssociationInfo' : 'MI05MID54RF09123456789'
    }
    try:
        response = requests.post(create_url,headers=create_request_head,json=create_request_parameter,timeout=30)
        create_response = response.json()
    except requests.exceptions.Timeout:
        return render(response, 'popup without agreement.html',{'message':"Payment failed!"})
    return HttpResponseRedirect(create_response.get('bkashURL'))

def execute(response):
    global base_url,user_name,password,app_key,app_secret,grant_response,id_token
    create_response_id = response.get_full_path()
    payment_id = re.search(r'paymentID=(.*?)&',create_response_id).group(1)
    status =  re.search(r'status=(.*?)&', create_response_id).group(1)
    
    if status == 'success':
        print("ggwp")
        execute_url = f'{base_url}/tokenized/checkout/execute'
        execute_request_head = {
            'Accept' :"application/json",
            'Authorization' : id_token,
            'X-App-Key' : app_key
        }
        execute_request_parameter = {
            'paymentID' : str(payment_id)
        }
        try:
            execute_response = requests.post(execute_url,headers=execute_request_head,json=execute_request_parameter,timeout=30)
            execute_response = execute_response.json()
            print("------------------------------------------------")
            print(execute_response)
            print("------------------------------------------------")
            final_reponse = execute_response.get('statusMessage')
            if final_reponse == 'Successful':
                if agreementID==None:
                    return render(response, 'popup without agreement.html',{'message':"Payment Successful!"})
                else:
                    return render(response, 'popup with agreement.html',{'message':"Payment Successful!"})
            elif final_reponse == 'Duplicate for All Transactions':
                if agreementID==None:
                    return render(response, 'popup without agreement.html',{'message':"Duplicate Transaction, Please try again after 2 minutes"})
                else:
                    return render(response, 'popup with agreement.html',{'message':"Duplicate Transaction, Please try again after 2 minutes"})
            else:
                if agreementID==None:
                    return render(response, 'popup without agreement.html',{'message':'Payment failed! ,'+final_reponse})
                else:
                    return render(response, 'popup with agreement.html',{'message':'Payment failed! ,'+final_reponse})
        except requests.exceptions.Timeout:
            query_url =  f'{base_url}/tokenized/checkout/payment/status'
            query_request_head = {
                'Content-Type' : "application/json",
                'Accept' :"application/json",
                'Authorization' : id_token,
                'X-App-Key' : app_key
            }
            query_request_parameter = {
                'paymentID' : str(payment_id),
            }
            query_response = requests.post(query_url,headers=query_request_head,json=query_request_parameter,timeout=30)
    elif status == 'cancel':
        if agreementID==None:
            return render(response, 'popup without agreement.html',{'message':"Payment cancelled"})
        else:
            return render(response, 'popup with agreement.html',{'message':"Payment cancelled"})
    else:
        if agreementID==None:
            return render(response, 'popup without agreement.html',{'message':"Payment failed,Wallet locked"})
        else:
            return render(response, 'popup with agreement.html',{'message':"Payment failed, Wallet Locked"})
def create_agreement(response):
    global base_url,user_name,password,app_key,app_secret,grant_response,id_token
    grant_URL = f"{base_url}/tokenized/checkout/token/grant"
    
    grant_request_head = {
        'Content-Type' : "application/json",
        'Accept' :"application/json",
        'username' : user_name,
        'password' :password
    }
    
    grant_request_parameter = {
        'app_key' : app_key,
        'app_secret' : app_secret
    }
    
    response = requests.post(grant_URL,headers=grant_request_head,json=grant_request_parameter)
    grant_response = response.json()
    id_token = grant_response.get("id_token")
    create_agg_url = f'{base_url}/tokenized/checkout/create'
    create_request_head = {
        'Content-Type' : "application/json",
        'Accept' :"application/json",
        'Authorization' : grant_response.get("id_token"),
        'X-App-Key' : app_key
    }
    create_request_parameter = {
        'mode' : "0000",
        'payerReference' : "01619777283",
        'callbackURL' : 'http://127.0.0.1:8000/playground/execute_agreement',
        'amount' : '10',
        'currency' : 'BDT',
        'intent' : 'sale',
        'merchantInvoiceNumber' : '01992939478',
    }
    try:
        response = requests.post(create_agg_url,headers=create_request_head,json=create_request_parameter,timeout=30)
        create_agreement_response = response.json()
    except requests.exceptions.Timeout:
        return render(response, 'popup without agreement.html',{'message':"Payment failed"})
    create_response = response.json()
    return HttpResponseRedirect(create_response.get('bkashURL'))
def execute_agreement(response):
    global base_url,user_name,password,app_key,app_secret,grant_response,id_token,create_agreement_response,agreementID, agreementStatus
    create_agreement_id = response.get_full_path()
    payment_id = re.search(r'paymentID=(.*?)&',create_agreement_id).group(1)
    status =  re.search(r'status=(.*?)&', create_agreement_id).group(1)
    if status == 'success':
        execute_url = f'{base_url}/tokenized/checkout/execute'
        execute_request_head = {
            'Accept' :"application/json",
            'Authorization' : id_token,
            'X-App-Key' : app_key
        }
        execute_request_parameter = {
            'paymentID' : str(payment_id)
        }
        try:
            execute_response = requests.post(execute_url,headers=execute_request_head,json=execute_request_parameter,timeout=30)
            execute_response = execute_response.json()
            agreementID=execute_response.get('agreementID')
            agreementStatus= execute_response.get('agreementStatus')
            pay_agg_url = f'{base_url}/tokenized/checkout/create'
            create_request_head = {
                'Content-Type' : "application/json",
                'Accept' :"application/json",
                'Authorization' : id_token,
                'X-App-Key' : app_key
            }
            create_request_parameter = {
                'mode' : "0001",
                'payerReference' : "01619777283",
                'callbackURL' : 'http://127.0.0.1:8000/playground/execute',
                'agreementID' : agreementID,
                'amount' : '10',
                'currency' : 'BDT',
                'intent' : 'sale',
                'merchantInvoiceNumber' : '01992939478',
                'merchantAssociationInfo' :'MI05MID54RF09123456789'
            }
            try:
                response = requests.post(pay_agg_url,headers=create_request_head,json=create_request_parameter,timeout=30)
                create_agreement_response = response.json()
            except requests.exceptions.Timeout:
                return render(response, 'popup with agreement.html',{'message':"Payment Failed!"})  
            create_response = response.json()
            return HttpResponseRedirect(create_agreement_response.get('bkashURL'))              
            return render(response, 'popup with agreement.html',{'message':"Agreement Successful"})
        except requests.exceptions.Timeout:
            query_agree__url =  f'{base_url}/tokenized/checkout/agreement/status'
            query_request_head = {
                'Accept' :"application/json",
                'Authorization' : id_token,
                'X-App-Key' : app_key
            }
            query_request_parameter = {
                'agreementID' : agreementID
            }
            query_response = requests.post(query_agree__url,headers=query_request_head,json=query_request_parameter,timeout=30)
    elif status == 'cancel':
        return render(response, 'popup without agreement.html',{'message':"Agreement cancelled"})
    else:
        return render(response, 'popup without agreement.html',{'message':"Aggreement failed"}) 
# def execute_agreement(response):
#     global base_url,user_name,password,app_key,app_secret,grant_response,id_token,create_agreement_response,agreementID, agreementStatus
#     create_agreement_id = response.get_full_path()
#     payment_id = re.search(r'paymentID=(.*?)&',create_agreement_id).group(1)
#     status =  re.search(r'status=(.*?)&', create_agreement_id).group(1)
#     if status == 'success':
#         execute_url = f'{base_url}/tokenized/checkout/execute'
#         execute_request_head = {
#             'Accept' :"application/json",
#             'Authorization' : id_token,
#             'X-App-Key' : app_key
#         }
#         execute_request_parameter = {
#             'paymentID' : str(payment_id)
#         }
#         try:
#             execute_response = requests.post(execute_url,headers=execute_request_head,json=execute_request_parameter,timeout=30)
#             execute_response = execute_response.json()
#             agreementID=execute_response.get('agreementID')
#             agreementStatus= execute_response.get('agreementStatus')
#             return render(response, 'popup with agreement.html',{'message':"Agreement Successful"})
#         except requests.exceptions.Timeout:
#             query_agree__url =  f'{base_url}/tokenized/checkout/agreement/status'
#             query_request_head = {
#                 'Accept' :"application/json",
#                 'Authorization' : id_token,
#                 'X-App-Key' : app_key
#             }
#             query_request_parameter = {
#                 'agreementID' : agreementID
#             }
#             query_response = requests.post(query_agree__url,headers=query_request_head,json=query_request_parameter,timeout=30)
#     elif status == 'cancel':
#         return render(response, 'popup without agreement.html',{'message':"Agreement cancelled"})
#     else:
#         return render(response, 'popup without agreement.html',{'message':"Aggreement failed"})   
def pay_with_agreement(request):
    global base_url,user_name,password,app_key,app_secret,grant_response,id_token,agreementID, agreementStatus
    pay_agg_url = f'{base_url}/tokenized/checkout/create'
    create_request_head = {
        'Content-Type' : "application/json",
        'Accept' :"application/json",
        'Authorization' : id_token,
        'X-App-Key' : app_key
    }
    create_request_parameter = {
        'mode' : "0001",
        'payerReference' : "01619777283",
        'callbackURL' : 'http://127.0.0.1:8000/playground/execute',
        'agreementID' : agreementID,
        'amount' : '10',
        'currency' : 'BDT',
        'intent' : 'sale',
        'merchantInvoiceNumber' : '01992939478',
        'merchantAssociationInfo' :'MI05MID54RF09123456789'
    }
    try:
        response = requests.post(pay_agg_url,headers=create_request_head,json=create_request_parameter,timeout=30)
        create_agreement_response = response.json()
    except requests.exceptions.Timeout:
        return render(response, 'popup with agreement.html',{'message':"Payment Failed!"})  
    create_response = response.json()
    return HttpResponseRedirect(create_agreement_response.get('bkashURL'))    
    
def cancel_agreement(response):
    global agreementID,agreementStatus
    agreementID = None
    agreementStatus = None
    return render(response, 'popup without agreement.html',{'message':"Aggreement cancelled"})  