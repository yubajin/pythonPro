
from StackListUtils import *
import re
import operator

class databaseByList(object):
    def __init__(self):
        self.__tables = StackListUtils()
        self.__tables.push([])#数据用列表存储
        self.__fields = []
        self.scoreColumn = []
        self.weightColumn = []
        self.__id = 0

    def getTables(self):
        return self.__tables

    def setPeekTable(self, table):
        self.__tables.updateLastNode(table)

    def getPeekTable(self):
        return  self.getTables().peek()

    def addTable(self, table):
        self.__tables.push(table)

    def getFields(self):
        return self.__fields

    def setFields(self, fields):
        self.__fields = fields

    def getScoreColumn(self):
        return self.scoreColumn

    def setScoreColumn(self):
        self.scoreColumn = []
        for field in self.getFields():
            if 'score' in field:
                self.scoreColumn.append(field)

    def getWeightColumn(self):
        return self.weightColumn

    def setWeightColumn(self):
        self.weightColumn  = []
        for field in self.getFields():
            if 'weight' in field:
                self.weightColumn.append(field)

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id = id

    def plusId(self):
        self.__id = self.__id + 1
        return self.__id

    def sortBy(self, isreverse, referColumn):
        self.setScoreColumn()#扫描带score的列
        self.setWeightColumn()#扫描带weight的列
        if not self.getScoreColumn().__len__() == 0 and not self.getWeightColumn().__len__() == 0:
            self.calAverage(self.getScoreColumn(),self.getWeightColumn(),'average')
        return list(sorted(self.getPeekTable(), key=operator.itemgetter(self.getListIndexFromField(referColumn)+1),reverse=isreverse))

    def getListIndexFromField(self, field):#获取该字段在字段列表中的引序
        fieldIndex = -1
        for i in self.getFields():
            if field == i:
                fieldIndex = self.getFields().index(i)
        return fieldIndex
    '''
    创建表
    '''
    def create_table(self, fields):#给数据库中创建以传入参数作为字段的表
        self.addTable([])
        self.setId(0)
        self.setFields(fields)
        return '创建表的属性:' + str(self.getFields())

    def add_recode(self, values):
        fields = self.getFields()
        recode = list(self.getPeekTable())#获得数据库中正在操作的表对象
        self.plusId()#id自增
        fields_values = zip(fields,list(values))#将表的字段和值以键值对的形式打包在一起,需要字段和值严格一一对应

        content = []
        content.append(self.getId())
        for (field,value) in fields_values:
            content.append(value)
        recode.append(content)
        self.setPeekTable(recode)

        return '增加一条记录'

    '''
        传入表的列名列表(字符),分数列表，权重列表，将加权放置给加权列表
    '''
    def calAverage(self, scoreColumn, weightColumn, averageColumn):
        if not averageColumn in self.getFields():
            print('自动',self.alter_table(averageColumn),averageColumn)
        for indexTable in list(self.getPeekTable()):#计算加权平均值
            totalscore = 0
            totalweight = 0
            score_weightLists = zip(scoreColumn, weightColumn)
            for (tempscore, tempweight) in score_weightLists:
                if not indexTable[self.getListIndexFromField(tempscore)+1] == None and not indexTable[self.getListIndexFromField(tempweight)+1] == None:
                    totalscore = totalscore + int(indexTable[self.getListIndexFromField(tempscore)+1]) * int(indexTable[self.getListIndexFromField(tempweight)+1])
                    totalweight = totalweight + int(indexTable[self.getListIndexFromField(tempweight)+1])
            average = round(totalscore / totalweight,2)
            if self.getFields().__len__() + 1 > list(indexTable).__len__():
                indexTable_len = list(indexTable).__len__()
                self.getPeekTable()[list(self.getPeekTable()).index(indexTable)][indexTable_len:] = [None]
            self.getPeekTable()[list(self.getPeekTable()).index(indexTable)][self.getListIndexFromField(averageColumn)+1] = average
        self.getPeekTable()

    def selectAll(self, table):
        self.setScoreColumn()#扫描带score的列
        self.setWeightColumn()#扫描带weight的列
        if not self.getScoreColumn().__len__() == 0 and not self.getWeightColumn().__len__() == 0:
            self.calAverage(self.getScoreColumn(),self.getWeightColumn(),'average')
        fields_num = self.getFields().__len__()#获取属性个数
        recodeCount = 0#数记录总共条数
        if not fields_num == 0:
            header_wrap = '+---------------' * fields_num + '+---------------+'
            formatStr = '|%-15s' * fields_num + '|%-15s|'
            indexs = self.getFields()
            fields = []
            fields.append('id')
            for index in indexs:
                fields.append(index)
            header = (formatStr) % (tuple(fields))#打印第一行
            print(header_wrap)
            print(header)
            print(header_wrap)
            for indexrecode in list(table):#遍历每一条记录
                recodeCount = recodeCount + 1
                recodesValue = []
                for i in list(indexrecode):#遍历每条记录的每个属性
                    recodeValue = i
                    recodesValue.append(recodeValue)
                result = (formatStr) % (tuple(recodesValue))
                print(result)
            print(header_wrap)
        print("{} rows in table".format(recodeCount))

    def selectById(self):
        pass

    def del_recode(self, id):
        return self.getTables().peekDelListById(id)

    def update_recode(self, id, field, value):
        fieldIndex = self.getListIndexFromField(field)
        self.getTables().peekUpdateListById(id, fieldIndex, value)

    ''' 
        增加单个数据库字段
        需要将之前的记录该字段置为None
    '''
    def alter_table(self, field):
        self.getFields().append(field)
        for indexTable in list(self.getPeekTable()):  # 遍历每一条记录,置新加列位None
            if isinstance(indexTable,list):
                indexTable_len = list(indexTable).__len__()
                self.getPeekTable()[list(self.getPeekTable()).index(indexTable)][indexTable_len:] = [None]
        return '增加了一个字段'

    def run(self):
        flag = False
        while not flag:
            userinput = input('bajinsql>')
            if(userinput[0:6] == 'create'):
                userinputre = re.search(r'create table (.*)', userinput, re.M | re.I)
                fieldArr = userinputre.group(1).lstrip('(').rstrip(')').replace(' ', '').split(',')
                print(self.create_table(fieldArr))
            if (userinput[0:6] == 'insert'):
                userinputre = re.search(r'insert table (.*) values (.*)', userinput, re.M | re.I)
                fieldArr = userinputre.group(1).lstrip('(').rstrip(')').replace(' ', '').split(',')
                valueArr = userinputre.group(2).lstrip('(').rstrip(')').replace(' ', '').split(',')
                index = 0
                for value in valueArr:
                    tempvalue = eval(value)
                    valueArr[index] = tempvalue
                    index = index + 1

                sentenceMatch = True
                index = 0
                for field in self.getFields():#判断增加记录是用户输入的属性是否和表的属性一致
                    if not field == fieldArr[index]:
                        sentenceMatch = False
                    index = index + 1

                print('用户输入的属性是否和表的属性一致:' ,sentenceMatch)
                if(sentenceMatch):
                    print(self.add_recode(valueArr))

            elif (userinput[0:6] == 'select'):
                if (userinput == 'select * from table'):
                    self.selectAll(self.getPeekTable())
                elif (userinput[-3:] == 'asc'):
                    userinputre = re.search(r'select (.*) from table sortby (.*) asc', userinput, re.M | re.I)
                    sortbyField = userinputre.group(2).replace(' ', '')
                    self.selectAll(self.sortBy(False, sortbyField))
                elif (userinput[-3:] == 'des'):
                    userinputre = re.search(r'select (.*) from table sortby (.*) des', userinput, re.M | re.I)
                    sortbyField = userinputre.group(2).replace(' ', '')
                    self.selectAll(self.sortBy(True, 'average'))

            elif (userinput[0:6] == 'delete'):
                userinputre = re.search(r'delete (.*) where (.*)', userinput, re.M | re.I)
                delId = int(userinputre.group(2).replace(' ', '').split('=')[1])
                print(self.del_recode(delId))

            elif (userinput[0:6] == 'update'):
                userinputre = re.search(r'update table set (.*) where (.*)', userinput, re.M | re.I)
                keys_values = userinputre.group(1).lstrip('(').rstrip(')').replace(' ', '').split(',')
                keys = []
                values = []
                for key_value in keys_values:#获取用户输入的属性和属性的值
                    keys.append(key_value.split('=')[0])#属性
                    values.append(key_value.split('=')[1])#属性的值
                tempkeys_values = zip(keys,values)
                updateId = int(userinputre.group(2).replace(' ', '').split('=')[1])
                countField = 0
                for key,value in tempkeys_values:
                    self.update_recode(updateId,key,eval(value))
                    countField = countField + 1
                print('一条记录的' + str(countField) + '个属性值已经更改')
            elif (userinput[0:5] == 'alter'):
                userinputre = re.search(r'alter table add (.*)', userinput, re.M | re.I)
                addField = userinputre.group(1).replace(' ', '')
                print(self.alter_table(addField))
            elif (userinput == 'exit()'):
                flag = True

db = databaseByList()
# print(db.create_table(['name','guowen_score','guowen_weight','math_score','math_weight']))
# print(db.add_recode(['zhangshang',89,2,94,3]))#需要检查创建表的属性要与增加记录的值的个数一一对应
# print(db.add_recode(['lisi',87,2,98,3]))#需要检查创建表的属性要与增加记录的值的个数一一对应
# print(db.alter_table('pe_score'))
# print(db.alter_table('pe_weight'))
# print(db.del_recode(1))
# db.update_recode(2,'name','changed')#需要检查要更改的属性是否在表里存在
#
#
# db.selectAll(db.sortBy(False, 'average'))
# print(db.add_recode(['zhangshang',89,2,94,3,99,2]))
# db.selectAll(db.getPeekTable())
# db.selectAll(db.sortBy(True, 'average'))
# db.add_recode(['wangwu',78,3,90,2,85.8])
db.run()

#操作语句:可以按照顺序复制到控制台从上往下执行
# create table (name,guowen_score,guowen_weight,math_score,math_weight)
# insert table (name,guowen_score,guowen_weight,math_score,math_weight) values ('zhangshagn',94 ,2,84,3)
# insert table (name,guowen_score,guowen_weight,math_score,math_weight) values ('lisi',89 ,2,96,3)
# select * from table
# select * from table sortby average asc
#select * from table sortby average des
#delete table where id = 2
#select * from table
#update table set (name = 'haschange', guowen_score = 60, math_score = 70) where id = 1
# select * from table

#create table (name1,guowen_score1,guowen_weight1,math_score1,math_weight1)
#insert table (name1,guowen_score1,guowen_weight1,math_score1,math_weight1) values ('wanglaowu_1',94,4 ,84,7)
#alter table add English_score
#alter table add English_weight
#insert table (name1,guowen_score1,guowen_weight1,math_score1,math_weight1,English_score,English_weight) values ('zhangshang_1',92,4 ,74,7,79,2)
# select * from table

#create table (username,password)
#insert table (username,password) values ('xiaoming',123456)
#update table set (username = 'xiaohong', password = 135790) where id = 1
#select * from table
# select * from table