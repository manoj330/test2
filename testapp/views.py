from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps
# Create your views here.

# class GetProfiles(APIView):
#     def get(self,request):
#         if self.request.query_params.get('uname'):
#             objs=Profile.objects.filter(username__contains=self.request.query_params.get('uname'))
#         elif self.request.query_params.get('id'):
#             objs=Profile.objects.get(id=self.request.query_params.get('id'))
#         else:
#             objs=Profile.objects.all()
#         serializer=ProfileSerializer(objs,many=True)  
      
#         return Response(serializer.data)
#     def post(self,request):
#         data=json.loads(self.request.body)
#         mdata=self.modify_data(data)
#         try:
#             obj=Profile(**data)
#             obj.save()
#             return Response({"sucess":"data created"})
#         except Exception as exc:
#             return Response({"error":str(exc)})
            
#     def delete(self,request):
#         id=self.request.query_params.get("id")
#         if id :
#             try:
#                obj=Profile.objects.get(id=id)
#                obj.delete()
#                return Response("data deleted")
#             except Exception as exec:
#                return Response({"error":str(exec)})
                
#     def put(self,request):
#         try:
#             data=json.loads(self.request.body)
#             obj=Profile.objects.get(id=data['id'])
#             mdata=self.modify_data(data)
#             obj.__dict__.update(mdata)
#             obj.save()
#             return Response("data updated")
#         except Exception as exec:
#             return Response({"error":str(exec)}) 
        
#     def modify_data(self,data):
#         skilldata=data.get('skills')
#         obj=Skill.objects.filter(skill=skilldata)
#         if len(obj)!=0:
#             data['skills']=obj[0]
#         else:
#             Skill.objects.create(skill=data.get('skills'),experience=0)
#             obj=Skill.objects.filter(skill=skilldata)[0]
#             data['skills']=obj
#         return data
            
            
            
            
        
# class SkillA(APIView):
#     def get(self,request):
#         objs=Skill.objects.all()
#         serializer=SkillSerializer(objs,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         try:
#             data=json.loads(self.request.body)
#             obj=Skill(**data)
#             obj.save()
#             return Response("posted sucecessfully")
#         except Exception as exec:
#             return Response({"error":str(exec)})
def convert(objs,many):
    """ coverts any model object to dictionary"""
    data=[]
    if many:
        for obj in objs:
            dic={}
            for field in obj._meta.fields:
                key = field.name
                value = getattr(obj, key)
                if field.is_relation:
                  value.__dict__.pop('_state')
                  
                  dic[key]=value.__dict__
                else:
                    dic[key]=value
            data.append(dic)

    else:
            
            for field in objs._meta.fields:
                key = field.name
                value = getattr(objs, key)
                if field.is_relation:
                      value.__dict__.pop('_state')
                      value.__dict__.pop('id')
                      data[key]=value.__dict__
                else:
                    data[key]=value
    
    return data
       

def modify_data(data):
        skilldata=data.get('skills')
        obj=Skill.objects.filter(skill=skilldata)
        if len(obj)!=0:
            data['skills']=obj[0]
        else:
            Skill.objects.create(skill=data.get('skills'),experience=0)
            obj=Skill.objects.filter(skill=skilldata)[0]
            data['skills']=obj
        return data          
""" function based"""  
@csrf_exempt  
def Profile_crud(request):
    if request.method=='GET':   
        if request.GET.get('uname'):
            objs=Profile.objects.filter(username__contains=request.query_params.get('uname'))
            data=convert(objs,many=True)
        elif request.GET.get('id'):
            objs=Profile.objects.get(id=request.GET.get('id'))
            data=convert(objs,many=False)
        else:
            objs=Profile.objects.all()
            data=convert(objs,many=True)

        
      
        return JsonResponse(data,safe=False)
    elif request.method=='POST':
        data=json.loads(request.body)
        mdata=modify_data(data)
        try:
            obj=Profile(**data)
            obj.save()
            return JsonResponse({"sucess":"data created"})
        except Exception as exc:
            return JsonResponse({"error":str(exc)})
            
    elif request.method=='DELETE':
        id=json.loads(request.body)['id']
        if id :
            try:
               obj=Profile.objects.get(id=id)
               obj.delete()
               return JsonResponse({"status":"data deleted"})
            except Exception as exec:
               return JsonResponse({"error":str(exec)})
                
    elif request.method=='PUT':
        try:
            data=json.loads(request.body)
            obj=Profile.objects.get(id=data['id'])
            mdata=modify_data(data)
            obj.__dict__.update(mdata)
            obj.save()
            return JsonResponse("data updated",safe=False)
        except Exception as exec:
            return JsonResponse({"error":str(exec)}) 
      
@csrf_exempt       
def SkillA(request):
    if request.method=='GET':
        objs=Skill.objects.all()
        data=convert(objs,many=True)
        return JsonResponse(data,safe=False)
    
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            obj=Skill(**data)
            obj.save()
            return JsonResponse("posted sucecessfully",safe=False)
        except Exception as exec:
            return JsonResponse({"error":str(exec)})
            
                    
        
        
            
            