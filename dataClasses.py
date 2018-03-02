#!/usr/bin/python
#coding: UTF-8

class inwardTransactionProcessedData:
    
    def __init__(self):
        self.dataToReport = {}
        self.dataToManual = {}


class outwardTransactionProcessedData:
    
    def __init__(self):
        self.dataToReport = {}
        self.dataToManual = {}

class exchangeRate:

    def __init__(self):
        self.exchangeRate = ''


class customerInfoData:
    
    def __init__(self):
        self.customerInfoData = ''

        
class accountInfoData:
    
    def __init__(self):
        self.accountInfoData = ''



class taxStatisticData:
    
    def __init__(self):
        self.inwardData  = '' 
        self.outwardData = ''

        #self.inwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'From(662)', 'AMOUNT', 'Currency(664)', 'Customer', 'Rate', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address', 'Tax Code']

        #self.outwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'To(662)', 'AMOUNT(660)', 'Currency(664)', 'Reasons(661)', 'Customer(671)', 'Beneficiary', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address', 'Tax Code']

        self.exchangeRateData = exchangeRate()
        self.customerInfoData = customerInfoData()
        self.accountInfoData = accountInfoData()


class sheetTitleInward:
    
    def __init__(self):
        self.toReport = 'Inward Remittance Report'
        self.toManual = 'Inward Remittance Manually Confirm'

class sheetTitleOutward:
    
    def __init__(self):
        self.toReport = 'Outward Remittance Report'
        self.toManual = 'Outward Remittance Manually Confirm'



class excelHeader:

    def __init__(self):
        self.inwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'From(662)', 'AMOUNT', 'Currency(664)',\
                             'Customer', 'Rate', 'SEK', 'Origanisation Number/ID', 'Personal Number', 'Address',\
                             'Tax Code']

        self.outwardHeader = ['Transaction Value Date(663)', 'Ref. NO.', 'To(662)', 'AMOUNT(660)', 'Currency(664)',\
                              'Reasons(661)', 'Customer(671)', 'Beneficiary', 'EX RATE', 'SEK', 'Origanisation Number/ID',\
                              'Personal Number', 'Address', 'Tax Code']

        self.inwardSheetTitle = sheetTitleInward()
        self.outwardSheetTitle = sheetTitleOutward()



class processedTransactionData:

    def __init__(self):

        self.inwardData = inwardTransactionProcessedData()
        self.outwardData = outwardTransactionProcessedData()

