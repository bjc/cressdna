#!/home/erik/bin/python3

#import packages to be used
import cgi, cgitb
import warnings
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import re
warnings.simplefilter("ignore", UserWarning)#ignore a joblib version warning

#----------------------------------------------\
#  Parse the web-form information to variables  \
#                                                \_______________________________________________________
#																										 |
cgitb.enable(display=1, logdir="/var/www/html/bin/")
form=cgi.FieldStorage()
alignment = form.getvalue('fasta')
if alignment.startswith(">"):		#naive check for FASTA format
	list=alignment.split(">")
	if list[0] == "":
		list.pop(0)#get rid of the leading empty string

	seqList=[]
	lenList=[]
	nameList=[]

	for a in list:
		tempList=a.split("\r\n")
		if tempList[-1]=="":
			tempList.pop(-1)#get rid of the trailing empty string
		
		tempSeq=""
		nameList.append(tempList[0])
		for element in tempList[1:]:
			tempSeq+=element
		
		seqList.append(tempSeq)
		lenList.append(str(len(tempSeq)))

	if len(seqList)==0:				#check for empty sequence list
		seqList = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
		nameList=['Demo']
		lenList=[str(len(alignment[0]))]

else:
	seqList = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
	nameList=['Demo']
	lenList=[str(len(alignment[0]))]

#--------------------------------------------------------------------------------------------------------+	

#----------------------------------------------\
#  predict genus of input sequences             \
#                                                \_______________________________________________________	
#																										 |
#list of amino acids as vocabulary for the CountVectorizer
AAs=['a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y']

#load the classifier and scaler
clf=joblib.load("./SVM_linear_aa_clf.pkl")

StSc=joblib.load("./UniqRepsGemys_6089_StSCALER.pkl")

cv=CountVectorizer(analyzer='char',ngram_range=(1,1),vocabulary=AAs)

#initialize text data vectorizer
dataVect=cv.transform(seqList)

#Scale the data to the training set
X=StSc.transform(dataVect.astype("float64"))

#make predictions for the original dataset
predictions=clf.predict(X)


#----------------------------------------------\
#  Build HTML table of results                  \
#                                                \_______________________________________________________	
# 
#results="<p> Entered Text Content Seq Name is {0} length {1}</p>".format(nameList,predictions)
results=""
results+="""
<table>
<tr>
<th>Sequence Name</th>
<th>Length</th>
<th>Prediction</th>
</tr>

"""


for k in range(len(nameList)):
	results+="<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(nameList[k],lenList[k],predictions[k])

results+="</table>"


#----------------------------------------------\
#  Build output page                            \
#                                                \_______________________________________________________	
# 																										 |
#build output page parts
#Header and CSS Style bits

header="""Content-type:text/html

<html>
<head>
<style>
*{box-sizing: border-box;}
body {font-family: "Lato", sans-serif;}
/* Style the tab */
div.tab {
	float: left;
	border: 1px solid #ccc;
	background-color: #f1f1f1;
	width: 20%;
	height: 250px;
}
/* Style the buttons inside the tab */
div.tab button {
	display: block;
	background-color: inherit;
	color: black;
	padding: 22px 16px;
	width: 100%;
	border: none;
	outline: none;
	text-align: left;
	cursor: pointer;
	transition: 0.3s;
	font-size: 17px;
}
/* Change background color of buttons on hover */
div.tab button:hover {
	background-color: #ddd;
}
/* Create an active/current "tab button" class */
div.tab button.active {
	background-color: #1acefc;
}
/* Style the tab content */
.tabcontent {
	float: left;
	padding: 0px 12px;
	border: 1px solid #ccc;
	width: 80%;
	min-height: 250px;
}
table {
	border-collapse: collapse;
	width: 80%;
}

th, td {
	text-align: left;
	padding: 8px;
}

tr:nth-child(even){background-color: #f2f2f2}

th {
	background-color: #ff0000;
	color: white;
}
</style>
</head>

"""
#Page contents, first part
body1="""<body>

<p>Welcome to CRESSdna.org</p>

<div class="tab">
  <button class="tablinks" onclick="openTab(event, 'Home')" >Home</button>
  <button class="tablinks" onclick="openTab(event, 'Taxonomy')">Taxonomy</button>
  <button class="tablinks" onclick="openTab(event, 'Contact')">Contact</button>
  <button class="tablinks" onclick="openTab(event, 'Results')"id="defaultOpen">Results</button>
</div>

<div id="Home" class="tabcontent">
  <h3>Home</h3>
  <p>Part of the <a href='http://www.nsf.gov/pubs/2010/nsf10513/nsf10513.htm'>National Science Foundation's Assembling the Tree of Life</a>.</p>
    <img src='../nsf1.jpg' alt='Sponsored with a Grant from the National Science Foundation'>
</div>

<div id="Taxonomy" class="tabcontent">
  <h3>Taxonomy</h3>
  <form action="classifier.py" method="post"><br>
  <textarea rows="4" cols="50" name="fasta" input type="submit">
>Demo
MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI</textarea>
</textarea>
			<br>
		<input type="reset">
		<input type="submit">
</form>	
  		<p>
  			<ul>
	<li>This classifier requires Rep protein sequence to be:</li>
		<ul>
		<li>Complete</li>
		<li>Unaligned</li>
		<li>in FASTA format</li>
		</ul>
	<p>And has been trained on the following Genera:</p>
		<li>Circoviridae</li>	
			<ul>
			<li>Circovirus</li>
			<li>Cyclovirus</li>
			</ul>
		<li>Nanoviridae</li>
			<ul>
			<li>Babuvirus</li>
			<li>Nanovirus</li>
			</ul>
		<li>Genomoviridae</li>	
			<ul>
			<li>Gemycircularvirus</li>
			<li>Gemygorvirus</li>
			<li>Gemykibivirus</li>
			<li>Gemykolovirus</li>
			<li>Gemykrogvirus</li>
			<li>Gemyvongvirus</li>
			</ul>
		<li>Geminiviridae</li>
			<ul>
			<li>Becurtovirus</li>
			<li>Begomovirus</li>
			<li>Capulavirus</li>
			<li>Curtovirus</li>
			<li>Eragrovirus</li>
			<li>Grablovirus</li>
			<li>Mastrevirus</li>
			<li>Turncurtovirus</li>
			</ul>
		<li>Smacovirus</li>
</ul>  		</p>
</div>
<div id="Contact" class="tabcontent">
  <h3>Contact</h3>
  <p>This site is under construction</p>
	<p>Please be patient while we tidy up a bit!</p>

</div> 

<div id="Results" class="tabcontent">
  <h3>Results</h3>
  <p>Results from Taxonomy prediction</p>

"""  

#Page contents, second part (results fit between body1 and body2)
body2="""<p>This classifier will return the best fit of the submitted sequence to the training data.<br>
Currently included in the training data:<br>
<li>Circoviridae</li>	
			<ul>
			<li>Circovirus</li>
			<li>Cyclovirus</li>
			</ul>
		<li>Nanoviridae</li>
			<ul>
			<li>Babuvirus</li>
			<li>Nanovirus</li>
			</ul>
		<li>Genomoviridae</li>	
			<ul>
			<li>Gemycircularvirus</li>
			<li>Gemygorvirus</li>
			<li>Gemykibivirus</li>
			<li>Gemykolovirus</li>
			<li>Gemykrogvirus</li>
			<li>Gemyvongvirus</li>
			</ul>
		<li>Geminiviridae</li>
			<ul>
			<li>Becurtovirus</li>
			<li>Begomovirus</li>
			<li>Capulavirus</li>
			<li>Curtovirus</li>
			<li>Eragrovirus</li>
			<li>Grablovirus</li>
			<li>Mastrevirus</li>
			<li>Turncurtovirus</li>
			</ul>
		<li>Smacovirus</li>
<br><br>	
</p>	
</div> 
 
<script>
function openTab(evt, tabTitle) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabTitle).style.display = "block";
    evt.currentTarget.className += " active";
}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
</script>
</body>
"""

#close the Page
footer="""
</html>"""

#build the output page
page=header+body1+results+body2+footer

#send the output as html 	
print (page)	
quit()
