

class Node:
  def __init__(self,examples):
    self.attribute = None
    self.children = {} #dict of value + rows
  #   self.isLeaf=False
  #   self.examples=[]
  #
  # def makeLeaf(self):
  #   self.isLeaf = True
  # def isLeaf(self):
  #   if self.isLeaf==True:
  #       return True
  def addChild(self, Node):
     self.children.update(Node)
	# you may want to add additional fields here...
