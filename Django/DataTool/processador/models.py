from django.db import models

# Create your models here.

class Field:
    def __init__(self, name, type, size):
        self.Name = name
        self.Type = type
        self.Size = size
        
class InputSettings:
    
    def __init__(self, containsHeader, delimiter, otherDelimiter, fieldList):
        self.ContainsHeader = containsHeader
        self.Delimiter = delimiter
        self.OtherDelimiter = otherDelimiter
        self.FieldDelimiter = otherDelimiter
        
        if delimiter == 'tab':
            self.FieldDelimiter = '\t'
        elif delimiter == 'semicolon':
            self.FieldDelimiter = ';'
        elif delimiter == 'fixed':
            self.FieldDelimiter = None # o delimitaador será pela largura fixa de cada campo 
            
        self.Fields = fieldList
        
class OutputSettings:
    
    def __init__(self, resultType, dbProvider, fieldKeyList, targetTableName):
        self.ResultType = resultType
        self.DBProvider = dbProvider
        self.Keys = fieldKeyList
        self.TargetTableName = targetTableName