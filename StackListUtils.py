
class StackListUtils(object):

    class Node(object):
        def __init__(self, val):
            self.__val = val
            self.__next = None
        def get_val(self):
            return self.__val
        def set_val(self, val):
            self.__val = val
        def get_next(self):
            return self.__next
        def set_next(self, next):
            self.__next = next

    header = Node(None)

    def push(self,val):
        pushNode = self.Node(val)
        pushNode.set_next(StackListUtils.header)
        StackListUtils.header = pushNode

    def pop(self):
        popNode = StackListUtils.header
        if popNode.get_next() == None:
            return
        else:
            StackListUtils.header = StackListUtils.header.get_next()
            return popNode.get_val()

    def peek(self):
        popNode = StackListUtils.header
        if popNode.get_next() == None:
            return
        else:
            return popNode.get_val()

    #delete
    '''
        如果最后一个元素是一个字典，删除字典里面的某条数据
    '''
    def peekDelDicById(self, id):
        if isinstance(StackListUtils.header.get_val(),dict):
            StackListUtils.header.get_val().pop(int(id))
        else:
            print('栈的最后一个元素不是字典')
        return  StackListUtils.header.get_val()

    '''
        如果最后一个元素是一个列表，删除列表里面的某条数据
    '''
    def peekDelListById(self, id):
        returnStr = ''
        find = False
        if isinstance(StackListUtils.header.get_val(),list):
            for indextable in StackListUtils.header.get_val():
                if not list(indextable).__len__() == 0:
                    if indextable[0] == id:
                        find = True
                        StackListUtils.header.get_val().remove(indextable)
                        returnStr = '一条记录被删除'
            if find == False:
                returnStr = 'id不存在'
        else:
            returnStr = '栈的最后一个元素不是列表'
        return  returnStr

    #updata
    def updateLastNode(self, val):
        tempNode = StackListUtils.header
        if tempNode.get_next() == None:
            return
        StackListUtils.header.set_val(val)

    '''
        如果最后一个元素是一个字典，更改字典里面的某条数据
    '''
    def peekUpdateDicById(self, id, field, value):
        if isinstance(StackListUtils.header.get_val()[int(id)], dict):
            tempdict = {field:value}
            StackListUtils.header.get_val()[int(id)].update(tempdict)

    '''
        如果最后一个元素是一个列表，更改列表里面的某条数据
    '''
    def peekUpdateListById(self, id, fieldIndex, value):
        returnStr = ''
        find = False
        if isinstance(StackListUtils.header.get_val(), list):
            for indextable in StackListUtils.header.get_val():
                if not list(indextable).__len__() == 0:
                    if indextable[0] == id:
                        find = True
                        indexOfIndextable = list(StackListUtils.header.get_val()).index(list(indextable))
                        StackListUtils.header.get_val()[indexOfIndextable][fieldIndex+1] = value
                        returnStr = '一条记录'
            if find == False:
                returnStr = 'id不存在'
        else:
            returnStr = '栈的最后一个元素不是列表'
        return returnStr

    def isEmpty(self):
        if(StackListUtils.header.get_next() == None):
            return True
        else:
            return False

    def clear(self):
        StackListUtils.header = StackListUtils.Node(None)

    def getAllNode(self):
        pass

