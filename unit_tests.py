import ID3, parse, random

def testID3AndEvaluateJimin():
  dataj = [dict(a=2, b=0, c=1, Class=2), dict(a=1, b=0, c=2, Class=3), dict(a=1, b=1, c=1, Class=1), dict(a=2,b=0,c=2, Class=4), dict(a=3,b=1,c=2, Class=3)]
  data1 = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
  data2 = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=0)]
  data3 = [dict(a=1, b=0, Class=2)] #one node tre
  data4 = [dict(a=1, b=0, Class=1), dict(a=0, b=1, Class=0)]
  data_t=[dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1),
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  data_tnt=[dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1),
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  #dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)
  tree = ID3.ID3(data_tnt, 0)
  ID3.print_tree(tree)
  #ID3.print_tree(tree)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=0, c=1))
    print("ans : " + str(ans))
  else:
    print("ID3 test failed -- no tree returned")

def testID3AndEvaluate():
  data = [dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=1)]
  tree = ID3.ID3(data, 0)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=1, b=0))
    if ans != 1:
      print("ID3 test failed.")
    else:
      print("ID3 test succeeded.")
  else:
    print("ID3 test failed -- no tree returned")

def testPruning():
  # data = [dict(a=1, b=1, c=1, Class=0), dict(a=1, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1), dict(a=0, b=0, c=0, Class=1), dict(a=0, b=0, c=1, Class=0)]
  # validationData = [dict(a=0, b=0, c=1, Class=1)]
  data = [dict(a=0, b=1, c=1, d=0, Class=1), dict(a=0, b=0, c=1, d=0, Class=0), dict(a=0, b=1, c=0, d=0, Class=1), dict(a=1, b=0, c=1, d=0, Class=0), dict(a=1, b=1, c=0, d=0, Class=0), dict(a=1, b=1, c=0, d=1, Class=0), dict(a=1, b=1, c=1, d=0, Class=0)]
  validationData = [dict(a=0, b=0, c=1, d=0, Class=1), dict(a=1, b=1, c=1, d=1, Class = 0)]
  tree = ID3.ID3(data, 0)
  ID3.prune(tree, validationData)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=0, c=1, d=0))
    if ans != 1:
      print("pruning test failed.")
    else:
      print("pruning test succeeded.")
  else:
    print("pruning test failed -- no tree returned.")

def testPruningJimin():
  # data = [dict(a=1, b=1, c=1, Class=0), dict(a=1, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1), dict(a=0, b=0, c=0, Class=1), dict(a=0, b=0, c=1, Class=0)]
  # validationData = [dict(a=0, b=0, c=1, Class=1)]
  data = [dict(a=0, b=1, c=1, d=0, Class=1), dict(a=0, b=0, c=1, d=0, Class=0), dict(a=0, b=1, c=0, d=0, Class=1), dict(a=1, b=0, c=1, d=0, Class=0), dict(a=1, b=1, c=0, d=0, Class=0), dict(a=1, b=1, c=0, d=1, Class=0), dict(a=1, b=1, c=1, d=0, Class=0)]
  validationData = [dict(a=0, b=0, c=1, d=0, Class=1), dict(a=1, b=1, c=1, d=1, Class = 0)]
  tree = ID3.ID3(data, 0)


  print("========tree before pruning")
  ID3.print_tree(tree)
  ID3.test(tree, validationData)

  ID3.prune(tree, validationData)

  print("=========tree after pruning")
  ID3.print_tree(tree)
  ID3.test(tree, validationData)
  if tree != None:
    ans = ID3.evaluate(tree, dict(a=0, b=0, c=1, d=0))
    if ans != 1:
      print("pruning test failed.")
    else:
      print("pruning test succeeded.")
  else:
    print("pruning test failed -- no tree returned.")


def testID3AndTest():
  trainData = [dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1), 
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  testData = [dict(a=1, b=0, c=1, Class=1), dict(a=1, b=1, c=1, Class=1), 
  dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)]
  tree = ID3.ID3(trainData, 0)
  ID3.print_tree(tree)
  fails = 0
  if tree != None:
    acc = ID3.test(tree, trainData)
    if acc == 1.0:
      print("testing on train data succeeded.")
    else:
      print("testing on train data failed.")
      fails = fails + 1
    acc = ID3.test(tree, testData)
    if acc == 0.75:
      print("testing on test data succeeded.")
    else:
      print("testing on test data failed.")
      fails = fails + 1
    if fails > 0:
      print("Failures: ", fails)
    else:
      print("testID3AndTest succeeded.")
  else:
    print("testID3andTest failed -- no tree returned.")	

def testID3AndTestJimin():
  trainData = [dict(a=1, b=0, c=0, Class=1), dict(a=1, b=1, c=0, Class=1),
  dict(a=0, b=0, c=0, Class=0), dict(a=0, b=1, c=0, Class=1)]
  testData = [dict(a=1, b=0, c=1, Class=1), dict(a=1, b=1, c=1, Class=1),
  dict(a=0, b=0, c=1, Class=0), dict(a=0, b=1, c=1, Class=0)]
  data = [dict(a=0, b=1, c=1, d=0, Class=1), dict(a=0, b=0, c=1, d=0, Class=0), dict(a=0, b=1, c=0, d=0, Class=1),
          dict(a=1, b=0, c=1, d=0, Class=0), dict(a=1, b=1, c=0, d=0, Class=0), dict(a=1, b=1, c=0, d=1, Class=0),
          dict(a=1, b=1, c=1, d=0, Class=0)]
  validationData = [dict(a=0, b=0, c=1, d=0, Class=1), dict(a=1, b=1, c=1, d=1, Class=0)]
  tree = ID3.ID3(data, 0)
  ID3.print_tree(tree)
  fails = 0
  if tree != None:
    acc = ID3.test(tree, validationData)
    print('acc = ' + str(acc))
  else:
    print("testID3andTest failed -- no tree returned.")


# inFile - string location of the house data file
def testPruningOnHouseData(inFile,idx):
  withPruning = []
  withoutPruning = []
  data = parse.parse(inFile)

  for i in range(100):
    print('============================= i : ' + str(i))
    random.shuffle(data)
    train = data[:idx]
    #train = data[:len(data)//2]
    valid = data[len(data)//2:3*len(data)//4]
    test = data[3*len(data)//4:]
  
    tree = ID3.ID3(train, 'democrat')
    ID3.print_tree(tree)
    acc = ID3.test(tree, train)
    print("training accuracy: ",acc)
    acc = ID3.test(tree, valid)
    print("validation accuracy: ",acc)
    acc = ID3.test(tree, test)
    print("test accuracy: ",acc)
  
    ID3.prune(tree, valid)
    acc = ID3.test(tree, train)
    print("pruned tree train accuracy: ",acc)
    acc = ID3.test(tree, valid)
    print("pruned tree validation accuracy: ",acc)
    acc = ID3.test(tree, test)
    print("pruned tree test accuracy: ",acc)
    withPruning.append(acc)
    tree = ID3.ID3(train+valid, 'democrat')
    acc = ID3.test(tree, test)
    print("no pruning test accuracy: ",acc)
    withoutPruning.append(acc)
  print(withPruning)
  print(withoutPruning)
  print("average with pruning",sum(withPruning)/len(withPruning)," without: ",sum(withoutPruning)/len(withoutPruning))
  reslist=[sum(withPruning)/len(withPruning), sum(withoutPruning)/len(withoutPruning)]
  return reslist

#####added by Jimin for testing
def main():
  data = [dict(a=2, b=0, Class=1),dict(a=1, b=0, Class=1), dict(a=1, b=1, Class=0)]

  #Todo: test with no-splitting data too
  #print(ID3.get_values_of_attr(data,'a'))
  #print(ID3.partition(data,'b'))
  #print(ID3.class_counts(data))
  #print(ID3.IG(ID3.partition(data,'a'),ID3.entropy(data)))
  #print(ID3.count_attributes(data))
  #print(ID3.get_attr_list(data))
  #print(ID3.find_best_split(data))
  #print(ID3.ID3(data,0))
  #testID3AndEvaluate()
  #testID3AndEvaluateJimin()
  #testPruning()
  #testPruningJimin()
  #testID3AndTest()
  #testID3AndTestJimin()
  n_tr_exmpls=[]
  w_pruneavgs=[]
  wo_pruneavgs=[]
  for i in range (10,301,15):
    indivres = testPruningOnHouseData("house_votes_84.data",i)
    n_tr_exmpls.append(i)
    w_pruneavgs.append(indivres[0])
    wo_pruneavgs.append(indivres[1])
  print("number of training examples : " + str(n_tr_exmpls))
  print("withprune averages : " + str(w_pruneavgs))
  print("without prune averages : " + str(wo_pruneavgs))

  #print(ID3.getSubset(data,'b',0))




if __name__ == "__main__":
  main()


