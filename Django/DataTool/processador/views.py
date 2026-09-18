from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.datastructures import MultiValueDictKeyError
from .models import Field, InputSettings, OutputSettings

# Create your views here.
class Default(View):
    
    template_name = 'form.html'
    
    def get (self, *args, **kwargs): 

        contexto = {
            'Dados': '',
        }
        
        return render (self.request, template_name=self.template_name, context=contexto)
    
    def post (self, *args, **kwargs):
        
        input = InputSettings(True, 'T', None, []) 
        output = OutputSettings('I', 'oracle', [], None)
        contexto = {
            'InputSetttings': input,
            'OutputSettings': output,
            'dataText': None,
            'resultText': None
        }
        
        return render (self.request, template_name=self.template_name, context=contexto)
    

class Formatar(View):
    
    template_name = 'form.html'
    
    def post (self, *args, **kwargs):   

        header = None        
        try:
            header = self.request.POST['HasHeader']
        except MultiValueDictKeyError as e:
            header = None
            
        hasHeader = True if header != None else False
        delimiter = self.request.POST['rdDelimiter']
        otherDelimiter = self.request.POST['txtOther']
        columns = self.request.POST['listFields']
        tableName = self.request.POST['txtTargetTableName']
        textData = self.request.POST['textData']
         
        listFields = []
        fieldSetting = []
        
        for col in columns.split('\n'):
            fieldSetting = col.split(' ')
            field = Field(fieldSetting[0], fieldSetting[1], fieldSetting[2])
            listFields.append(field)
        
        input = InputSettings(hasHeader, delimiter, otherDelimiter, listFields) 

        tableName = self.request.POST['txtTargetTableName']
        resultType = self.request.POST['rdResultAs']
        columns = self.request.POST['listKeys']
        listKeys = []
        
        for col in columns.split('\n'):
            fieldSetting = col.split(' ')
            field = Field(fieldSetting[0], fieldSetting[1], fieldSetting[2])
            listKeys.append(field)
        
        selDBProvider = self.request.POST['selDBProvider']
        print ('selDBProvider: ', selDBProvider)
        output = OutputSettings(resultType, selDBProvider, listKeys, tableName)
        
        contexto = {
            'InputSettings': input,
            'OutputSettings': output,
            'textData': textData,
            'result': '',
        }
        
        return render (self.request, template_name=self.template_name, context=contexto)
