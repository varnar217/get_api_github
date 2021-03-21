#from django.shortcuts import render
#from django.http import HttpResponse

#def homePageView(request):
    #return HttpResponse('Hello worlds')
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from github import Github
from .forms import UserForm
from pprint import pprint
import json
import requests
import os

def poluchenie_pull(username,i):
    out2=requests.get('https://api.github.com/search/issues?q=state%3Aopen+author%3A{}+type%3Apr'.format(username)) .json()
    k=0
    html_url=''
    for dann in out2['items']:

        if i == k:
            html_url=str(dann['pull_request']['html_url'])
            url_html=str(dann['pull_request']['url'])


        k=k+1


    return html_url,url_html

def get_commits(html_url):
    out2=requests.get(html_url) .json()

    number_commits=out2['commits']
    return number_commits

def index(request):
    if request.method == "POST":
        username = request.POST.get("name")

        out=(requests.get('https://api.github.com/users/{}/repos'.format(username) ).json())

        nume_proejct=[]
        k_bufer=0
        zagolovok=['name','stargazers_count','repos_url','pull_html','number_commits']
        for repo in out:
            nume_xx=[]

            if not repo['private']:
                a=repo['name']


                a1=str(repo['name'])
                nume_xx.append(a1)
                nume_xx.append(repo['stargazers_count'])
                nume_xx.append(repo['html_url'])

                html_url1,urll=(poluchenie_pull(username,k_bufer))
                #print(urll)
                nume_xx.append(html_url1)
                number_commits=get_commits(urll)
                nume_xx.append(number_commits)


                nume_proejct.append(nume_xx)
                k_bufer=k_bufer+1



        return render(request,"ers.html",context={"langes":nume_proejct,'nazvanie':zagolovok})
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})
