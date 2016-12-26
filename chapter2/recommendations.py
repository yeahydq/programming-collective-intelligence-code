#coding:utf-8
# A dictionary of movie critics and their ratings of a small
# set of movies
import json
import os.path

import re

import time

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0, 
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


from math import sqrt

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]: 
    if item in prefs[person2]: si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) 
                      for item in prefs[person1] if item in prefs[person2]])

  return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]: 
    if item in prefs[p2]: si[item]=1

  # if they are no ratings in common, return 0
  if len(si)==0: return 0

  # Sum calculations
  n=len(si)
  
  # Sums of all the preferences
  sum1=sum([prefs[p1][it] for it in si])
  sum2=sum([prefs[p2][it] for it in si])
  
  # Sums of the squares
  sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
  sum2Sq=sum([pow(prefs[p2][it],2) for it in si])	
  
  # Sum of the products
  pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/n)
  den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den==0: return 0

  r=num/den

  return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
  scores=[(similarity(prefs,person,other),other) 
                  for other in prefs if other!=person]
  scores.sort()
  scores.reverse()
  return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson):
  if person not in prefs :
    return "N/A"
    # return
  totals={}
  simSums={}
  # loop rows
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    # loop column
    for item in prefs[other]:
	    
      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings

def transformPrefs(prefs):
  result={}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})
      
      # Flip item and person
      result[item][person]=prefs[person][item]
  return result


def calculateSimilarItems(prefs,n=10):
  # Create a dictionary of items showing which other items they
  # are most similar to.
  result={}
  # Invert the preference matrix to be item-centric
  itemPrefs=transformPrefs(prefs)
  c=0
  for item in itemPrefs:
    # Status updates for large datasets
    c+=1
    if c%100==0: print "%d / %d" % (c,len(itemPrefs))
    # Find the most similar items to this one
    scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
    result[item]=scores
  return result

def getRecommendedItems(prefs,itemMatch,user):
  if user not in prefs :
    return user + ": not exist"
    # return
  userRatings=prefs[user]
  scores={}
  totalSim={}
  # Loop over items rated by this user
  for (item,rating) in userRatings.items( ):

    # Loop over items similar to this one
    for (similarity,item2) in itemMatch[item]:
      # Ignore if this user has already rated this item
      # pattern = re.compile(r'Wyatt')
      # match = pattern.match(item2)
      # if match: print "debug1:",item,item2
      if item2 in userRatings: continue
      # Weighted sum of rating times similarity
      scores.setdefault(item2,0)
      scores[item2]+=similarity*rating
      # if pattern.match(item2): print "Debug3",item2,similarity,rating
      # Sum of all the similarities
      totalSim.setdefault(item2,0)
      totalSim[item2]+=similarity
      # if (user == "675" & item2=='Wyatt Earp (1994)'): print "Debug",user,item2,similarity,rating
      #if (user == "675" ): print "Debug", user, item2, similarity, rating

  # Divide each total score by total weighting to get an average
  try:
    # rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
    rankings=[(score/totalSim[item],item) for item,score in scores.items( ) if totalSim[item]>0]
  except Exception,e:
    print item,scores[item],totalSim[item]
    print Exception,":",e
  # Return the rankings from highest to lowest
  rankings.sort( )
  rankings.reverse( )
  return rankings


def loadMovieLens(path='/data/movielens'):
  # Get movie titles
  movies = {}
  for line in open(path + '/u.item'):
    (id, title) = line.split('|')[0:2]
    movies[id] = unicode(title,errors='ignore')

  # Load data
  prefs = {}
  for line in open(path + '/u.data'):
    (user, movieid, rating, ts) = line.split('\t')
    prefs.setdefault(user, {})
    prefs[user][movies[movieid]] = float(rating)
  return prefs


def loadMovieLens_new(path='/data/movielens'):
  # Get movie titles
  movies = {}
  for line in open(path + '/movies.dat'):
    # (id, title) = line.split('||')[0:2]
    (id, title) = re.split('::',line)[0:2]
    movies[id] = title

  # Load data
  prefs = {}
  for line in open(path + '/ratings.dat'):
    # (user, movieid, rating, ts) = line.split('||')
    (user, movieid, rating, ts) = re.split('::',line)
    prefs.setdefault(user, {})
    prefs[user][movies[movieid]] = float(rating)
  return prefs


# loadMovieLens
# print critics['Lisa Rose']
# print critics['Lisa Rose']['Snakes on a Plane']


# for (d,x) in critics.items():
#      print "key:"+d+",value:"+str(x)
# print
# for d,x in critics.items():
#     print "key:"+d+",value:"+str(x)
# print
#
# for d,x in critics.items():
#     for e,f in x.items():
#       print "Name:"+d+",Move:"+e+",score:"+str(f)
# print
#
# for d, x in transformPrefs(critics).items():
#   for e, f in x.items():
#     print "Movie:" + d + ",Name:" + e + ",score:" + str(f)

#
# for user in critics:critics
#
#   for mv in user:
#     print mv

# print "sim_distance",sim_distance(critics,'Lisa Rose','Lisa Rose')
# print "topMatches",topMatches(critics,'Lisa Rose')
# print "getRecommendations", getRecommendations(critics,'Toby')

# print "calculateSimilarItems", calculateSimilarItems(critics)
# result=calculateSimilarItems(critics)
# for item, sub in result.items():
#     print item,sub

# print "Test For"
# for item, sub in critics.items():
#   for movie,score in sub.items():
#     print item,movie,score
#

# res2=getRecommendedItems(critics,result,'Toby')
# print res2
def final_test(loadmethod=loadMovieLens):
  a=loadmethod('/dick/PycharmProject/programming-collective-intelligence-code/data/movielens')
  print a['87']
  print "method A"
  # start = time.clock()
  # for id in range(1,1000):
  #   print "user:"+str(id)+":",\
  #   getRecommendations(a,str(id))[0:30]
  # end = time.clock()
  # print("The function run time is : %.03f seconds" % (end - start))

  print "method b"
  start = time.clock()
  js_file = "output.json"
  if not os.path.exists(js_file):
    # Writing JSON data
    with open(js_file, 'w') as f:
      itemsim = calculateSimilarItems(a, n=50)
      json.dump(itemsim, f)
  else:
    # Reading data back
    with open(js_file, 'r') as f:
      itemsim = json.load(f)

  for id in range(1,1000):
    print "user:"+str(id)+":",\
      getRecommendedItems(a,itemsim,str(id))[0:30]
  # # print getRecommendedItems(a,itemsim,'87')[0:30]
  # # print getRecommendedItems(a,itemsim,'1')[0:30]
  # # print getRecommendedItems(a,itemsim,'87')[0:30]
  end = time.clock()
  print("The function run time is : %.03f seconds" % (end - start))

# final_test()
final_test(loadMovieLens_new)

# a = loadMovieLens_new('/dick/PycharmProject/programming-collective-intelligence-code/data/movielens')
# print a['87']
