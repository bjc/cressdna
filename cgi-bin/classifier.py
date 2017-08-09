<<<<<<< HEAD
#!/home/erik/bin/python3.6m
=======
#!/home/erik/bin/python3.6
>>>>>>> f7d7849fcd6ce02a59db8c5fadc29d1962476493

#import packages to be used
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import cgi, cgitb

cgitb.enable()
form=cgi.FieldStorage()
if form.getvalue('fasta'):
	alignment = form.getvalue('fasta')
	alignment=[alignment]
	name=form.getvalue('seqname')
	size=len(alignment[0])
else:
	alignment = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
	name='demo'
	size=len(alignment[0])
	
<<<<<<< HEAD
html = open("./var/www/html/CRESSresults.html")
=======
html = open("./www.html/CRESSresults.html")
>>>>>>> f7d7849fcd6ce02a59db8c5fadc29d1962476493
page=html.read()


AAs=['a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y']
clf=joblib.load("./cgi-bin/SVM_linear_aa_clf.pkl")
StSc=joblib.load("./cgi-bin/UniqRepsGemys_6089_StSCALER.pkl")
cv=CountVectorizer(analyzer='char',ngram_range=(1,1),vocabulary=AAs)


#initialize text data vectorizer

dataVect=cv.transform(alignment)
 	
#Scale the data to the training set
X=StSc.transform(dataVect.astype("float64"))

#make predictions for the original dataset
results=",".join([name,clf.predict(X)[0]])
results=",".join([results,str(size)])
#for i in results:
	#print(i[0],"\t",i[1])

output = page.format(prediction=results)
"""f=open('test.html','w')
f.write(output)
f.close()"""
print (output)	

	
<<<<<<< HEAD
quit()
=======
quit()
>>>>>>> f7d7849fcd6ce02a59db8c5fadc29d1962476493
