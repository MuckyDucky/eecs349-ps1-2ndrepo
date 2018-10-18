from node import Node
import math
import copy
import random



def ID3(examples, default):
  print("ID3")
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  default = 0
  attr_to_split, gain = find_best_split(examples) #find best attribute to split on
  print('attr_to_split : ' + str(attr_to_split))
  root = Node(examples, attr_to_split)

  #todo: eval is not pointing to same node. -> solved
  if gain == 0:

    return Node(examples)
  else:
    part_list = partition(examples,attr_to_split)
    for p in part_list:
      for instance in p:
        if '?' in instance.values():
          qkey=find_key(instance, '?')
          instance[qkey]=nodemode(p,qkey)
      root.addChild(ID3(p,0))
  return root

def nodemode(examples,attr):
  tracker = {}
  assigners = ['y','n']
  for instance in examples:
    if instance[attr] not in tracker:
      tracker[instance[attr]] = 1
    else:
      tracker[instance[attr]] += 1
  mode = max(tracker, key=tracker.get)
  if mode is '?':
    return assigners[random.uniform(0,1)]
  return mode



def ID3_real(filled_examples, default):
  pass



def find_key(dict,v):
  for k,v in dict.items():
    if dict[k]==v:
      return k

def prune(node, examples):
  print("prune function")
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if hasGC(node): #if node has children of children
    for child in node.getChildren():
      themode=mode_class(child.getExamples())
      print('themode is : ' + str(themode))
      subset = getSubset(examples, node.getAttribute(), themode)
      print('subset is ' + str(subset))
      prune(child,subset)
  else:
    preprune_acc = test(node,examples)
    if preprune_acc == None:
      return 0
    temp_children=node.getChildren()
    temp_attr = node.getAttribute()
    node.removeAllChildren()
    node.attribute=None
    postprune_acc = test(node,examples)
    if preprune_acc > postprune_acc: #no prune
      node.children = temp_children
      node.attribute=temp_attr
    else: #prune
      print('pruned ')

def getSubset(examples,attr,val):
  subset = []
  for example in examples:
    if example[attr] == val:
      subset.append(example)
  return subset

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  orig_ex = copy.deepcopy(examples)
  test_data = copy.deepcopy(examples)

  if len(test_data)==0:
    return None

  tree = ID3(node.getExamples(), 0)

  correct_cnt=0

  for i in range(len(test_data)):
    test_data[i].pop('Class')
    print(test_data[i])
    res = evaluate(tree, test_data[i])
    if res == orig_ex[i]['Class']:
      correct_cnt+=1

  print("accuracy is : " + str(correct_cnt/len(test_data)))
  return correct_cnt/len(test_data)

def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if node.isLeaf():

    class_count = count_classes(node.getExamples())
    return max(class_count, key=class_count.get)

  #print(node.getAttribute())
  #print(node.getExamples())
  if example[node.getAttribute()] is not '?':
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
  yorn =['y','n']
  listofpartitions = [] #listoflists
  for v in values:
    #print(v)
    listtoappend =[]
    for row in dataset:
      if row[attr] == v:
        listtoappend.append(row)


    listofpartitions.append(listtoappend)


  return listofpartitions

def get_values_of_attr(dataset, attr): #returns set of values of attr
  list_of_values=[]
  for row in dataset: #each row is a dict
    list_of_values.append(row[attr])
  return set(list_of_values)

def find_best_split(dataset): #return attribute, gain with best split in the current example portion
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
  attr_list=[]
  for attr in dataset[0]:
    if attr != 'Class':
      attr_list.append(attr)
  return attr_list

def count_classes(dataset): #returns a dictionary that keeps count of the possible outputs.
  count_dict={}
  for row in dataset:
    theclass = row['Class']
    if theclass in count_dict:
      count_dict[theclass] +=1
    else:
      count_dict[theclass] = 1
  return count_dict


def print_tree(node, margin=''):
  print(margin +  str(node.getExamples()))
  if node.isLeaf() == True:
    print('----->leaf.') #parent is ' + str(node.parent.getExamples()))
    return 0
  margin+='-'
  for child in node.getChildren():
    print_tree(child,margin)

def isSameRow(dict1, dict2):
  for k,v in dict1.items():
    if k is 'Class':
      continue
    if v != dict2[k]:
      return False
  return True

def mode_class(examples): #returns the mode Class among examples.
  class_count = count_classes(examples)
  return max(class_count, key=class_count.get)

def pruneworthy(node, examples): #todo: dsf
  if len(examples)==0:
    return True

  correct = 0
  for row in examples:
    if row['Class'] == mode_class(examples):
      correct += 1

  if float(correct)/len(examples) >= test(node,examples):
      return True
  return False

def hasGC(node):
  for child in node.getChildren():
    if len(child.getChildren()) > 0:
      return True
  return False
def subset(examples, label):
  subsets = {}

  for row in examples:
    if not row[label] in subsets.keys():
      subsets[row[label]] = [row]
    else:
      subsets[row[label]].append(row)
  return subsets