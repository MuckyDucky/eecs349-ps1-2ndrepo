from node import Node
import math
import copy


def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  print("=======ID3 phase start")
  print('current Node examples : ' + str(examples))
  attr_to_split, gain = find_best_split(examples) #find best attribute to split on
  print('attr_to_split : ' + str(attr_to_split))
  print('gain : ' + str(gain))
  root = Node(examples, attr_to_split)
  #print(root.getExamples())

  #todo: eval is not pointing to same node.
  if gain == 0:
    print('children of this node : ' + str(root.getChildren()))

    return Node(examples)
  else:
    print('node number : ' + str(root))
    part_list = partition(examples,attr_to_split)
    print(part_list)
    for p in part_list:
      print('p is ' + str(p))
      print('adding child for ' + str(p))
      #root.addChild(Node(p))
      root.addChild(ID3(p,0))
    print('children of this node : ' + str(root.getChildren()))
    #for child in root.getChildren():
      #ID3(child.getExamples(),0)
  #for child in root.getChildren():
    #print(child.getExamples())

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
  orig_ex = copy.deepcopy(examples)
  test_data = copy.deepcopy(examples)

  tree = ID3(node.getExamples(), 0)

  #test_data[0].pop('Class')

  correct_cnt=0
  #print("test_data test : " + str(test_data[1]))
  #print(evaluate(tree, test_data[0]))
  #test_data[1].pop('Class')
  #print(evaluate(tree,test_data[1]))
  #evaluate(tree, dict(a=0,b=0,c=0) )
  for i in range(len(test_data)):
    test_data[i].pop('Class')
    #print_tree(tree)
    #print("testing example : " + str(test_data[i]))
    res = evaluate(tree, test_data[i])
    #res = evaluate(tree, dict(a=0,b=0,c=0))
    if res == orig_ex[i]['Class']:
      print('---->accurate!')
      correct_cnt+=1
    else:
      print("---->not accurate!")
  print("accuracy is : " + str(correct_cnt/len(test_data)))
  return correct_cnt/len(test_data)

  #evaluate examples without class and see if they match with its actual class



def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  #if len(node.getChildren())==0: #a no-split case. return the class of the example set
  if len(node.getChildren()) == 0: #get the mode class #and if attribute value matches
    #print("leaf:" + str(node.getExamples()))
    #search if there is an exact match first
    for item in node.getExamples():
      if isSameRow(item,example):
        print('fell at example : ' + str(example))

        print('children : ' + str(node.getChildren()))
        print('evaluate result : ' + str(item['Class']))
        return item['Class']
    # if not,
    class_count = count_classes(node.getExamples())
    print('fell at example : ' + str(node.getExamples()))
    print('node : ' + str(node))
    print('children : ' + str(node.getChildren()))
    print('evaluate result : ' + str(max(class_count, key=class_count.get)) )
    return max(class_count, key=class_count.get)


    #print(node.getExamples()[0]['Class'])
    #return node.getExamples()[0]['Class'] ###Todo:fix!! check accuracy. needs testing

  if example[node.getAttribute()] is not '?':
    #print("node examples : " + str(node.getExamples()))
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
    print('----->leaf')
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


