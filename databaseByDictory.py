'''
1.在添加操作之前需要检验是否有建表
2.需要检查添加操作字段和值个数是否一一对应
3.需要检验输入的sql语句是否符合规范，语句前不能有空格，属性没有引号，字段的值如果是字符要用引号...

4.支持动态添加表格字段
5.支持建多张表进行操作
6.执行用sql语句进行操作
7.支持自动算出带score的分数列表和带weight的权重列表的加权平均，若新添加的列也带score和weight也会自动算入加权平均
8.支持按照用户输入的列来进行升序还是降序的排序

sql语句事例:
建表:create table (属性1,属性2,属性3, ...)
eg:create table (name,guowen_score,guowen_weight,math_score,math_weight)

插入数据:insert table (属性1,属性2,属性3 ...) values (属性值1,属性值2 ,属性值3 ...)
eg:insert table (name,guowen_score,guowen_weight,math_score,math_weight) values ('zhangshang',94 ,2,84,3)
   insert table (name,guowen_score,guowen_weight,math_score,math_weight) values ('lisi',89 ,2,96,3)

查询所有:select * from table

条件查询:select * from table sortby 排序依据的列名 升降序
eg:select * from table sortby average des

删除数据:delete table where 属性 = 属性值
eg:delete table where id = 2

更新数据:update table set (属性1 = 属性值1 , 属性2 = 属性值2,  属性3 = 属性值3 ...) where 属性 = 属性值
eg:update table set (name = 'haschange', guowen_score = 60, math_score = 70) where id = 1

添加变量:alter table add 属性 （一次只支持添加一个属性）
eg:alter table add English_score
   alter table add English_weight
'''
from StackListUtils import *
import re
class databaseByDictory(object):
    def __init__(self):
        self.__tables = StackListUtils()
        self.__tables.push({})
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
        return dict(sorted(self.getPeekTable().items(), key=lambda x: x[1][referColumn], reverse=isreverse))

    '''
    创建表
    '''
    def create_table(self, fields):#给数据库中创建以传入参数作为字段的表
        self.addTable({})
        self.setId(0)
        self.setFields(fields)
        return '创建表的属性:' + str(self.getFields())

    def add_recode(self, values):
        fields = self.getFields()
        recode = dict(self.getPeekTable())#获得数据库中正在操作的表对象
        recode.setdefault(self.plusId())#id自增,{id:content} content:{'':'','':''...}
        field_value = zip(fields,list(values))#将表的字段和值以键值对的形式打包在一起,需要字段和值严格一一对应
        content = {}
        for (field,value) in field_value:
            content.setdefault(field,value)
        recode[self.getId()] = content
        self.setPeekTable(recode)
        return '增加一条记录'

    '''
        传入表的列名列表(字符),分数列表，权重列表，将加权放置给加权列表
    '''
    def calAverage(self, scoreColumn, weightColumn, averageColumn):
        if not averageColumn in self.getFields():
            print('自动',self.alter_table(averageColumn),'average')
        for key, value in dict(self.getPeekTable()).items():
            totalscore = 0
            totalweight = 0
            score_weightLists = zip(scoreColumn, weightColumn)
            for (tempscore, tempweight) in score_weightLists:
                if not self.getPeekTable()[key][tempscore] == None and not self.getPeekTable()[key][tempweight] == None:
                    totalscore = totalscore + int(self.getPeekTable()[key][tempscore]) * int(self.getPeekTable()[key][tempweight])
                    totalweight = totalweight + int(self.getPeekTable()[key][tempweight])
            average = round(totalscore / totalweight,2)
            self.getPeekTable()[key][averageColumn] = average
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
            keys = self.getFields()
            fields = []
            fields.append('id')
            for key in keys:
                fields.append(key)
            header = (formatStr) % (tuple(fields))
            print(header_wrap)
            print(header)
            print(header_wrap)
            for key, value in dict(table).items():#遍历每一条记录
                recodeCount = recodeCount + 1
                recodesValue = []
                recodesValue.append(int(key))
                for i in range(1,fields_num + 1):#遍历每条记录的每个属性
                    recodeValue = table[key][(fields[i])]
                    recodesValue.append(recodeValue)
                result = (formatStr) % (tuple(recodesValue))
                print(result)
            print(header_wrap)
        print("{} rows in table".format(recodeCount))

    def selectById(self):
        pass

    def del_recode(self, id):
        self.getTables().peekDelDicById(id)
        return '一条记录被删除'

    def update_recode(self, id, field, value):
        self.getTables().peekUpdateDicById(id, field, value)

    ''' 
        增加单个数据库字段
        需要将之前的记录该字段置为None
    '''
    def alter_table(self, field):
        fields_num = self.getFields().__len__()  # 获取原来属性个数
        self.getFields().append(field)
        for key, value in dict(self.getPeekTable()).items():  # 遍历每一条记录
            if isinstance(self.getPeekTable()[key],dict):
                self.getPeekTable()[key][(self.getFields()[fields_num])] = None
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
                    print(userinputre)
                    sortbyField = userinputre.group(2).replace(' ', '')
                    db.selectAll(self.sortBy(False, sortbyField))
                elif (userinput[-3:] == 'des'):
                    userinputre = re.search(r'select (.*) from table sortby (.*) des', userinput, re.M | re.I)
                    sortbyField = userinputre.group(2).replace(' ', '')
                    db.selectAll(self.sortBy(True, 'average'))

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
            #alter database add average
            elif (userinput[0:5] == 'alter'):
                userinputre = re.search(r'alter table add (.*)', userinput, re.M | re.I)
                addField = userinputre.group(1).replace(' ', '')
                print(self.alter_table(addField))
            elif (userinput == 'exit()'):
                flag = True

db = databaseByDictory()
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
# insert table (name1,guowen_score1,guowen_weight1,math_score1,math_weight1) values ('wanglaowu_1',94,4 ,84,7)
#alter table add English_score
#alter table add English_weight
# insert table (name1,guowen_score1,guowen_weight1,math_score1,math_weight1,English_score,English_weight) values ('zhangshang_1',92,4 ,74,7,79,2)
# select * from table

#create table (username,password)
#insert table (username,password) values ('xiaoming',123456)
#update table set (username = 'xiaohong', password = 135790) where id = 1
#select * from table
# select * from table