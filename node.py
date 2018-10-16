

class Node:
  def __init__(self,examples,attribute=None):
    self.examples=examples
    self.attribute = attribute
    self.children = [] #dict of value + rows
  #   self.isLeaf=False
  #   self.examples=[]
  #
  # def makeLeaf(self):
  #   self.isLeaf = True
  # def isLeaf(self):
  #   if self.isLeaf==True:
  #       return True
  def addChild(self, Node):
     self.children.append(Node)
  def getAttribute(self):
    return self.attribute
  def getChildren(self):
    return self.children
  def getExamples(self):
    return self.examples
	# you may want to add additional fields here...
