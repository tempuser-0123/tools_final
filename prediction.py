import operator
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
import json
from collections import defaultdict
import operator
import sys

sys.path.append('C:\\wamp64\\www\\')
from mvoiedict import movies

forPredict=[]
try:
    budgetForPredict=float(sys.argv[1])
except:
    budgetForPredict=0
predicActorsL=[]
for i in range(2,len(sys.argv)):
	predicActorsL.append(sys.argv[i].replace('_',' '))
	
# Is the money in different years have the same rate too? Obviousely no, so we are going to consider base of the year the rate
# the exchange effect, our movie database is from 1986 until today.
# base of the http://www.dollartimes.com/calculators/inflation.htm   the value $1 dolar today is equal to $2.16
# we create a table of value of dolars so we can estimate the groas base of the today value and calculate the previous 
# table agaiin to see which movie had highest value
dolarYearRate=[1,1.01,1.01,1.03,1.05,1.08,1.10,1.13,1.13,1.17,1.20,1.24,1.28,1.31,1.34,1.36,
               1.41,1.44,1.47,1.49,1.54,1.58,1.62,1.67,1.72,1.77,1.88,1.96,2.05,2.14,2.16]
dolarYearValue={}
for y in range(31,0,-1):
    dolarYearValue[str(2017-y)]=dolarYearRate[y-1]
	
# Now count profit rate base of the dolar value 
profity={}
for movie in movies.keys():
    profity[movie]=float(movies[movie]['gross'])*dolarYearValue[movies[movie]['year']]-float(movies[movie]['budget'])*dolarYearValue[movies[movie]['year']]
	
# create the actor1, 2, 3 as one list
actors={}
for title in movies.keys():
    actors[movies[title]['actor1']]=[movies[title]['actor1_rank'],movies[title]['actor1_sex']]
    actors[movies[title]['actor2']]=[movies[title]['actor2_rank'],movies[title]['actor2_sex']]
    actors[movies[title]['actor3']]=[movies[title]['actor3_rank'],movies[title]['actor3_sex']]

	
actorsList=[]
actorsId={}
i=0
for actor in actors.keys():
    i+=1
    actorsList.append([i,actor,actors[actor][0],actors[actor][1]])
    actorsId[actor]=i
	
# create a list of actors and their movies total gross	
acorsPrifit=defaultdict(float)
numberOfMovies=0
for actorArr in actorsList:
    actor=actorArr[1]
    acorsPrifit[actor]=0.
    numberOfMovies=0.
    for movie in movies:
        if actor==movies[movie]['actor1'] or actor==movies[movie]['actor2'] or actor==movies[movie]['actor3']:
            acorsPrifit[actor]=acorsPrifit[actor]+float(movies[movie]['gross'])*dolarYearValue[movies[movie]['year']]-float(movies[movie]['budget'])*dolarYearValue[movies[movie]['year']]
            numberOfMovies+=1.
    #acorsPrifit[actor]=acorsPrifit[actor]/numberOfMovies
    acorsPrifit[actor]=int(acorsPrifit[actor])
	

actorAmount=len(predicActorsL)
xlist=[]
ylist=[]
movielist=[]
actor1list=[]
budgetList=[]
profitList=[]
predicActors=[]
if (budgetForPredict!=0):
	predicActors.append(budgetForPredict)
for actori in predicActorsL:
	predicActors.append(acorsPrifit[actori]/1000000.)
for movie in movies.keys():
	xlistItems=[]
	if(budgetForPredict!=0):
	    xlistItems.append(int(float(int(int(movies[movie]['budget'])*dolarYearValue[movies[movie]['year']]/1000000))))
	for actor in range(1,actorAmount+1):
	    xlistItems.append(acorsPrifit[movies[movie]['actor'+str(actor)]]/1000000.)
	xlist.append(xlistItems)
	ylist.append(float(int(int(movies[movie]['gross'])*dolarYearValue[movies[movie]['year']]/1000000)))
xlist=np.reshape(xlist, (len(xlist), len(predicActors))) 
X=np.array(xlist)
y=np.array(ylist)

resultDict={}
# Split the targets into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)


# Create polynomial lenear regression model and fit to get prediction
# Create a dictionary of the results
model = make_pipeline(PolynomialFeatures(3), LinearRegression())
model.fit(X_train, y_train)
mse = mean_squared_error(model.predict(X_test), y_test)
socre=model.score(X_test, y_test)
resultDict['Predicted gross']=str("%.3f" % model.predict(np.array(predicActors).reshape(1,-1))[0]) + " M$"
resultDict['Score'] = "%.3f" % socre

# Return the results as json
print json.dumps(resultDict)
