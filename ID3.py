from node import Node
import math


def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''


  attr_to_split, gain = find_best_split(examples) #find best attribute to split on
  root = Node(examples,attr_to_split)
  if gain == 0:
    return Node(examples)
  else:
    part_list = partition(examples,attr_to_split)
    for p in part_list:
      root.addChild(Node(p))
    for child in root.getChildren():
      ID3(child.examples,0)
  for child in root.getChildren():
    print(child.getExamples())

  return root


def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  #if len(node.getChildren())==0: #a no-split case. return the class of the example set
  if node.isLeaf() == True:
    print(node.getExamples()[0]['Class'])
    return node.getExamples()[0]['Class'] ###Todo:fix!! check accuracy. needs testing

  if example[node.getAttribute()] is not '?':
    print("node examples : " + str(node.getExamples()))
    for child in node.getChildren():
      #print("iterating on child that has : " +  str(child.getExamples()))
      #print("child.getExamples()[0] = " + str(child.getExamples()[0]))
      if child.getExamples()[0][node.getAttribute()] == example[node.getAttribute()]:
      #check if value of splitted attribute matches
        #if it matches,

        #for item in child:
        return evaluate(child,example)


def partition(dataset,attr): #partitions data according to attr. returns list of partitioned dataset(list of lists)

  values = get_values_of_attr(dataset,attr)

  listofpartitions = [] #listoflists
  for v in values:
    #print(v)
    listtoappend =[]
    for row in dataset:
      if row[attr] == v:
        listtoappend.append(row)
    listofpartitions.append(listtoappend)


  # partitioned=dict.fromkeys(values,[])
  #
  # for v,l in partitioned.items():
  #   for row in dataset:
  #     if row[attr]==v:
  #       l.append(row)
  # for row in dataset:
  #   #if row[attr] in partitioned:
  #   print(row[attr])
  #   partitioned[1].append('match')
  #   #partitioned[row[attr]].append('match')

  return listofpartitions

def get_values_of_attr(dataset, attr): #returns set of values of attr
  list_of_values=[]
  for row in dataset: #each row is a dict
    list_of_values.append(row[attr])
  return set(list_of_values)

def find_best_split(dataset): #return attribute, gain with best split in the current example portion
  #return best_gain, best_attribute
  #try attributes, find the one with the best gain
  best_gain  = 0
  best_attribute = None
  H_prior = entropy(dataset)
  attr_list=get_attr_list(dataset)

  for attr in attr_list:
    attr_IG=IG(partition(dataset, attr), H_prior)
    if attr_IG >= best_gain:
      best_attribute,best_gain=attr,attr_IG

  return best_attribute,best_gain


def IG(listofparts,H_prior): #Todo: attributes should be in list/dict/set form
  currIG=H_prior
  total_length=0
  for l in listofparts:
    total_length+=len(l)
  #print("H_prior is " + str(H_prior))
  #print("listofparts is " + str(listofparts))
  for l in listofparts:
    p=float(len(l))/total_length
    #print("p is " + str(p))
    currIG-=p*entropy(l)
  #print("currIG is " + str(currIG))
  return currIG

def entropy(dataset): #Todo: parameter type
  counts = class_counts(dataset)
  entropy = 0
  for label in counts:
    prob_lbl = counts[label] / float(len(dataset))
    entropy += -prob_lbl * math.log(prob_lbl, 2)
  return entropy

def class_counts(dataset):
  # returns dictionary that contains total count of each attribute
  counts = {}
  for row in dataset:
      label = row['Class']
      if label not in counts:
        counts[label] = 1
      else:
        counts[label] +=1
  return counts

def count_attributes(dataset):
  count = 0
  for attr in dataset[0]:
    if attr is not 'Class':
      count +=1
  return count

def get_attr_list(dataset):
  return [ attr for attr in dataset[0] if attr is not 'Class']


