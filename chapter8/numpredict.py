from random import random,randint


def wineprice(rating,age):
  peak_age=rating-50
  
  # Calculate price based on rating
  price=rating/2
  if age>peak_age:
    # Past its peak, goes bad in 10 years
    price=price*(5-(age-peak_age)/2)
  else:
    # Increases to 5x original value as it
    # approaches its peak
    price=price*(5*((age+1)/peak_age))
  if price<0: price=0
  return price


def wineset1():
  rows=[]
  for i in range(300):
    # Create a random age and rating
    rating=random()*50+50
    age=random()*50

    # Get reference price
    price=wineprice(rating,age)
    
    # Add some noise
    price*=(random()*0.2+0.9)

    # Add to the dataset
    rows.append({'input':(rating,age),
                 'result':price})
  return rows

def euclidean(v1,v2):
  d=0.0
  for i in range(len(v1)):
    d+=(v1[i]-v2[i])**2
  return math.sqrt(d)


def getdistances(data,vec1):
  distancelist=[]
  
  # Loop over every item in the dataset
  for i in range(len(data)):
    vec2=data[i]['input']
    
    # Add the distance and the index
    distancelist.append((euclidean(vec1,vec2),i))
  
  # Sort by distance
  distancelist.sort()
  return distancelist


def knnestimate(data,vec1,k=5):
  # Get sorted distances
  dlist=getdistances(data,vec1)
  avg=0.0
  
  # Take the average of the top k results
  for i in range(k):
    idx=dlist[i][1]
    avg+=data[idx]['result']
  avg=avg/k
  return avg

def inverseweight(dist,num=1.0,const=0.1):
  return num/(dist+const)

def subtractweight(dist,const=1.0):
  if dist>const: 
    return 0
  else: 
    return const-dist

def gaussian(dist,sigma=5.0):
  return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gaussian):
  # Get distances
  dlist=getdistances(data,vec1)
  avg=0.0
  totalweight=0.0
  
  # Get weighted average
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]
    weight=weightf(dist)
    avg+=weight*data[idx]['result']
    totalweight+=weight
  if totalweight==0: return 0
  avg=avg/totalweight
  return avg

def dividedata(data,test=0.05):
  trainset=[]
  testset=[]
  for row in data:
    if random()<test:
      testset.append(row)
    else:
      trainset.append(row)
  return trainset,testset

def testalgorithm(algf,trainset,testset):
  error=0.0
  for row in testset:
    guess=algf(trainset,row['input'])
    error+=(row['result']-guess)**2
    #print row['result'],guess
  #print error/len(testset)
  return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.1):
  error=0.0
  for i in range(trials):
    trainset,testset=dividedata(data,test)
    error+=testalgorithm(algf,trainset,testset)
  return error/trials

def wineset2():
  rows=[]
  for i in range(300):
    rating=random()*50+50
    age=random()*50
    aisle=float(randint(1,20))
    bottlesize=[375.0,750.0,1500.0][randint(0,2)]
    price=wineprice(rating,age)
    price*=(bottlesize/750)
    price*=(random()*0.2+0.9)
    rows.append({'input':(rating,age,aisle,bottlesize),
                 'result':price})
  return rows

def rescale(data,scale):
  scaleddata=[]
  for row in data:
    scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
    scaleddata.append({'input':scaled,'result':row['result']})
  return scaleddata

def createcostfunction(algf,data):
  def costf(scale):
    sdata=rescale(data,scale)
    return crossvalidate(algf,sdata,trials=20)
  return costf

weightdomain=[(0,10)]*4

def wineset3():
  rows=wineset1()
  for row in rows:
    if random()<0.5:
      # Wine was bought at a discount store
      row['result']*=0.6
  return rows

def probguess(data,vec1,low,high,k=5,weightf=gaussian):
  dlist=getdistances(data,vec1)
  nweight=0.0
  tweight=0.0
  
  for i in range(k):
    dist=dlist[i][0]
    idx=dlist[i][1]
    weight=weightf(dist)
    v=data[idx]['result']
    
    # Is this point in the range?
    if v>=low and v<=high:
      nweight+=weight
    tweight+=weight
  if tweight==0: return 0
  
  # The probability is the weights in the range
  # divided by all the weights
  return nweight/tweight

from pylab import *

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
  t1=arange(0.0,high,0.1)
  cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])
  plot(t1,cprob)
  show()


def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
  # Make a range for the prices
  t1=arange(0.0,high,0.1)
  
  # Get the probabilities for the entire range
  probs=[probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]
  
  # Smooth them by adding the gaussian of the nearby probabilites
  smoothed=[]
  for i in range(len(probs)):
    sv=0.0
    for j in range(0,len(probs)):
      dist=abs(i-j)*0.1
      weight=gaussian(dist,sigma=ss)
      sv+=weight*probs[j]
    smoothed.append(sv)
  smoothed=array(smoothed)
    
  plot(t1,smoothed)
  show()


def testPrice():
  print wineprice(95.0,3.0)
  print wineprice(95.0, 40.0)
  print wineprice(95.0, 50.0)
  print wineprice(95.0, 52.0)
  print wineprice(95.0, 53.0)
  print wineprice(95.0, 54.0)
  wines=wineset1()
  print wines[1]
  print wines[2]
  print euclidean(wines[1]['input'],wines[2]['input'])

def testKnnEst():
  data=wineset1()
  print knnestimate(data,(95,3))
  print wineprice(85.0,3.0)

def testDivide():
  a=[i for i in range(100)]
  b,c=dividedata(a)
  print len(b),len(c)

def knn3(data,vect):
  return knnestimate(data,vect,k=3)

def testRescaleValidate():
  data=wineset2()
  print crossvalidate(knnestimate,data)
  sdata=rescale(data,[10,10,0,0.5])
  print crossvalidate(knnestimate,sdata)

import optimization

def testValidate():
  data=wineset1()
  print "Knn:",crossvalidate(knnestimate,data)
  print "weightKnn:",crossvalidate(weightedknn,data)
def testGenScale():
    data = wineset2()
    print crossvalidate(knnestimate, data)
    print crossvalidate(weightedknn, data)
    weighdomain=[(0,20)]*4
    costfunction=createcostfunction(knnestimate,data)

    #rating,age,aisle,bottlesize
    lenghuo_S=optimization.annealingoptimize(weighdomain, costfunction,step=2)
    print lenghuo_S
    lenghuo_data=rescale(data,lenghuo_S)
    print crossvalidate(knn3,lenghuo_data)

    climbHill_S = optimization.hillclimb(weighdomain, costfunction)
    print climbHill_S
    climbHill_data = rescale(data, climbHill_S)
    print crossvalidate(knn3, climbHill_data)

def testProbgguess():
  data=wineset3()
  vec=[99.0,20.0]
  print wineprice(99.0,20.0)
  print weightedknn(data,vec)

  print probguess(data,vec,40,80)
  print probguess(data, vec, 80, 120)
  print probguess(data, vec, 120, 1200)
  print probguess(data, vec, 30, 120)
  cumulativegraph(data,vec,200)

def testPrint_1():
  from pylab import *
  a=array([1,2,3,4])
  b=array([4,2,3,1])
  plot(a,b)
  show()
  t1=arange(0.0,10.0,0.1)
  plot(t1,sin(t1))
  show()

def testPrint_2():
  import matplotlib.pyplot as plt
  N = 50
  x = np.random.rand(N)
  y = np.random.rand(N)
  area = np.pi * (15 * np.random.rand(N)) ** 2  # 0 to 15 point radiuses
  color = 2 * np.pi * np.random.rand(N)
  plt.scatter(x, y, s=area, c=color, alpha=0.5, cmap=plt.cm.hsv)
  plt.show()

if __name__ == '__main__' :
  #testPrice()
  #testKnnEst()
  # testValidate()
  # testDivide()
  # testRescaleValidate()
  # testGenScale()
  # testProbgguess()
  # testPrint_1()
  testPrint_2()
