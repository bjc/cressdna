#!/home/erik/bin/python3.6

#import packages to be used
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import cgi, cgitb

#----------------------------------------------\
#  Parse the web-form information to variables  \
#                                                \_______________________________________________________
#																										 |
cgitb.enable()
form=cgi.FieldStorage()
alignment = str(form.getvalue('fasta'))
if alignment.startswith(">"):		#naive check for FASTA format
	list=alignment.split(">")
	book={}
	for a in list:
		tempList=a.splitlines()
		nameLine=tempList.pop(0)
		name=nameLine.split(" ")[0]
		seq="".join(tempList)
		book[name]=seq
	seqList=[]
	lenList=[]
	nameList=[]
	for i in book:
		nameList.append(i)
		seqList.append(book[i])
		lenList.append(str(len(book[i])))
	
	if len(seqList)==0:				#check for empty sequence list
		seqList = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
		nameList=['demo']
		lenList=[str(len(alignment[0]))]
		
else:
	seqList = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
	nameList=['demo']
	lenList=[str(len(alignment[0]))]

#--------------------------------------------------------------------------------------------------------+	

#----------------------------------------------\
#  predict genus of input sequences             \
#                                                \_______________________________________________________	
#																										 |
#list of amino acids as vocabulary for the CountVectorizer
AAs=['a','c','d','e','f','g','h','i','k','l','m','n','p','q','r','s','t','v','w','y']

#load the classifier and scaler
clf=joblib.load("SVM_linear_aa_clf.pkl")
StSc=joblib.load("UniqRepsGemys_6089_StSCALER.pkl")
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
# 																										 |
results=""""""
if "demo" in nameList:
	results+="""<p>There seems to have been an error.<br>If you are expecting more than one prediction or 
	do not see the name you entered please try the submission form again, making sure that the input is in FASTA format."""																								
else:
	for k in len(seqList):
		results+="""<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>""".format(nameList[k],lenList[k],predictions[k])


#----------------------------------------------\
#  Build output page                            \
#                                                \_______________________________________________________	
# 																										 |
#build output page parts
#Header and CSS Style bits
header="""<!DOCTYPE html>

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
body1="""
<body>

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
    <img src='nsf1.jpg' alt='Sponsored with a Grant from the National Science Foundation'>
</div>

<div id="Taxonomy" class="tabcontent">
  <h3>Taxonomy</h3>
  <p>Please enter only one word as the name(no space) and only one Rep sequence</p>
  <form action="./cgi-bin/classifier.py" method="post"><br>
	<input type="text" name="seqname" value="seqID"><br>
	<textarea rows="4" cols="50" name="fasta" input type="submit">
Enter ONE Rep protein sequence here...</textarea>
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
  <p>Questions or comments? Send us an email:</p>
	<p>email At domain Dot something</p>
</div> 

<div id="Results" class="tabcontent">
  <h3>Results</h3>
  <p>Results from Taxonomy prediction</p>
  <table>
  <tr>
    <th>Sequence Name</th>
    <th>Length</th>
    <th>Prediction</th>
  </tr>
"""  

#Page contents, second part (results fit between body1 and body2)
body2="""
</table>
  <p>This classifier will return the best fit of the submitted sequence to the training data.<br>
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
</html> 
"""

#build the output page
page=header+body1+results+body2+footer
	
#send the output as html 	
#output = page.format()
print (page)	

quit()
