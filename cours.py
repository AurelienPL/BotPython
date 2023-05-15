class node:
  def __init__(self,data):
    self.data = data
    self.next_node = None

class queue:
  def __init__(self, data):
    self.first_node = node(data)

  def pop(self):
    if self.first_node == None:
      return

    data = self.first_node.data
    self.first_node = self.first_node.next_node
    return data

  def append(self,data):
    current_node = self.first_node
    while current_node.next_node != None:
      current_node = current_node.next_node
    current_node.next_node = node(data)

########################################################
class node:
  def __init__(self, answer, question):
    self.answer = answer
    self.questio = question
    self.next_node = []

  def size(self):
    count = 1
    for node in self.next_node:
      count += node.size
    return count
  
  def deepth(self):
    Max = 0 
    for node in self.next_nodes:
      if node.deepth() > Max:
        Max = node.deepth()
    return Max + 1
  
  def append(self,question, reponses, question_precedante):
    if question_precedante == self.question:
      self.next_nodes.append(node(question, reponses))
    for n in self.next_nodes:
      n.append(question, reponses, question_precedante)

class tree:
  def __init__(self, question):
    self.first_node = node("", question)
    self.current_node = self.first_node

  def size(self):
    return self.first_node.size()
  
  def deepth(self):
    return self.first_node.deepth()
  
  def append(self, question, reponses, question_precedente):
   self.first_node.append( question, reponses, question_precedente)

  def get_question(self):
    return self.current_node.question

  def choice(self, message):
    pass


#####################################################

class node : 
  def __init__(self,data):
    self.data = data
    self.right_node = None
    self.left_node = None

  def append(self,data):
    if data < self.data :
      if self.left_node == None:
        self.left_node = node(data)
      else:
        self.left_node.append(data)
    elif data > self.data:
      if self.right_node == None:
        self.right_node = node(data)
      else:
        self.right_node.append(data)

  def search(self, data):
    if data == self.data:
      return True
    elif data < self.data:
      if self.left_node == None:
        return False
      else:
        return self.left_node.search(data)
    else:
      if self.right_node == None:
        return False
      else:
        return self.right_node.search(data)
      
  def __str__(self):
    txt = str(self.data)
    if self.left_node != None:
      txt += "-" +str(self.left_node)
    if self.right_node != None:
      txt += "-" +str(self.right_node)
    return txt


class binary_tree:
  def __init__(self,data):
    self.first_node = node(data)

  def append(self,data):
    self.first_node.append(data)

  def search(self,data):
    return self.first_node.search(data)

  def __str__(self):
    return str(self.first_node)
  


  ###########################################################

  class hashmap:
    def __init__(self, length):
      self.datas = []
      for i in range(length):
        self.datas.append([])

    def append(self,key,value):
      hashed_key = hash(key)
      indice = hashed_key % len(self.datas)
      self.datas[indice].append ((key, value))

    def get(self, key):
      hashed_key = hash(key)
      indice = hashed_key % len(self.datas)
      for key_datas, value_datas in self.datas[indice]:
        if key == key_datas:
          return value_datas
        return None
      


#####################################################################


person = {
    "name" : "Aurelien",
    "age" : 20
}

import json


jsonFile = open("C:\Users\aured\OneDrive\Bureau\bot discords.py, "w")
jsonFile.write(jsonString)
jsonFile.close()


jsonFile2 = open("C:\Users\aured\OneDrive\Bureau\bot discords.py/data.json")
data = json.load(jsonFile2)

print(json.dumps(person))
      
