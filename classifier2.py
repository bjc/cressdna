#!/home/erik/bin/python3

#%% Load libraries
import cgi, cgitb
from sklearn.externals import joblib
import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Embedding, Conv1D, Dense, Flatten
from keras.initializers import RandomNormal
from keras.optimizers import RMSprop
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

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
		nameList=['AAF97593.1']
		lenList=[str(len(alignment[0]))]

else:
	seqList = ["MPSKKSGPQPHKRWVFTLNNPSEEEKNKIRELPISLFDYFVCGEEGLEEGRTAHLQGFANFAKKQTFNKVKWYFGARCHIEKAKGTDQQNKEYCSKEGHILIECGAPRNQGKRSDLSTAYFDYQQSGPPGMVLLNCCPSCRSSLSEDYYFAILEDCWRTINGGTRRPI"]
	nameList=['AAF97593.1']
#%% Constants for the models	
max_len=573
lenList=[str(len(alignment[0]))]

#%%load the models
GeneModel=load_model("./GeneModel.model")
GenusModel=load_model("./Gene_Rep_vs_Other.model")
le=joblib.load("./LabelEncoder.pkl")

#%%transfrom the input for the models 
X=[" ".join(seq) for seq in seqList]
X=[one_hot(x,26, lower=False) for x in X]
X=[one_hot(x,n=26,lower=False) for x in X]
X=pad_sequences(X,maxlen=max_len,value=0,padding="post")

#%% make predictions
rep_pred=GeneModel.predict_classes(X)
genus_prob=[max(x) for x in GenusModel.predict(X)]
genus_pred=GenusModel.predict_classes(X)


#----------------------------------------------\
#  Build HTML table of results                  \
#                                                \_______________________________________________________	
# 
#results="<p> Entered Text Content Seq Name is {0} length {1}</p>".format(nameList,predictions)
resultsTable=""
resultsTable+="""
<table>
<tr>
<th>Sequence Name</th>
<th>Length</th>
<th>Rep?</th>
<th>Predicted Genus</th>
<th>Genus Probability</th>
</tr>

"""


for k in range(len(nameList)):
	resultsTable+="<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(nameList[k],lenList[k],rep_pred[k],genus_pred[k],genus_prob[k])

resultsTable+="</table>"


#----------------------------------------------\
#  Build output page                            \
#                                                \_______________________________________________________	
# 																										 |
#build output page parts
#Header and CSS Style bits

header="""Content-type:text/html

<html>
<head>
<meta name="description" content="Home of CRESS virus" />
<title>CRESS virus home</title>
<meta name="robots" content="nofollow, nosnippet" />
<link rel="stylesheet" type="text/css" href="./bin/mystyle.css">
</head>

"""
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
/* Menu Styles */
.third-level-menu
{
    position: absolute;
    top: 0;
    right: -150px;
    width: 150px;
    list-style: none;
    padding: 0;
    margin: 0;
    display: none;
}

.third-level-menu > li
{
    height: 30px;
    background: #ddd;
}
.third-level-menu > li:hover { background: #1acefc; }

.second-level-menu
{
    position: absolute;
    top: 30px;
    left: 0;
    width: 150px;
    list-style: none;
    padding: 0;
    margin: 0;
    display: none;
}

.second-level-menu > li
{
    position: relative;
    height: 30px;
    background: #ddd;
}
.second-level-menu > li:hover { background: #1acefc; }

.top-level-menu
{
    list-style: none;
    padding: 0;
    margin: 0;
}

.top-level-menu > li
{
    position: relative;
    float: left;
    height: 30px;
    width: 150px;
    background: #ddd;
}
.top-level-menu > li:hover { background: #1acefc; }

.top-level-menu li:hover > ul
{
    /* On hover, display the next level's menu */
    display: inline;
}


/* Menu Link Styles */

.top-level-menu a /* Apply to all links inside the multi-level menu */
{
    font: bold 14px Arial, Helvetica, sans-serif;
    color: black;
    text-decoration: none;
    padding: 0 0 0 10px;

    /* Make the link cover the entire list item-container */
    display: block;
    line-height: 30px;
}
.top-level-menu a:hover { color: black; }

.tabcontent {
    float: left;
    padding: 0px 12px;
    border: 1px solid #ccc;
    width: 100%;
    min-height: 250px;
}
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 50%;
}

th{
	background-color: red;
	color: white;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>

"""
#Page contents, first part
body1="""<body>

<p>Welcome to CRESSdna.org</p>

<ul class="top-level-menu">
    <li><a href="#" class="tablinks" onclick="openTab(event, 'Home')" >Home</a></li>
    <li>
	    <a href="#">Taxonomy</a>
        <ul class="second-level-menu">
            <li><a href="#" class="tablinks" onclick="openTab(event, 'Circoviridae')">Circoviridae</a></li>
			<li><a href="#" class="tablinks" onclick="openTab(event, 'Nanoviridae')">Nanoviridae</a></li>
			<li><a href="#"><i>more on the way</i></a></li>
		</ul>
	</li>
	<li>
		<a href="#">Classifier</a>
		<ul class="second-level-menu">
				<li><a href="#" class="tablinks" onclick="openTab(event, 'Classifier')">Run the classifier</a></li>
				<li><a href="#" class="tablinks" onclick="openTab(event, 'Results')" id="defaultOpen">Results</a></li>
		</ul>
	</li>	
    <li><a href="#" class="tablinks" onclick="openTab(event, 'Contributers')">Contributers</a></li>	
 	<li><a href="#" class="tablinks" onclick="openTab(event, 'Contact')">Contact</a></li>
	
</ul>

<div id="Home" class="tabcontent">
  <h3>Home</h3>
  <p>Part of the <a href='http://www.nsf.gov/pubs/2010/nsf10513/nsf10513.htm'>National Science Foundation's Assembling the Tree of Life</a>.</p>
    <img src='../nsf1.jpg' alt='Sponsored with a Grant from the National Science Foundation'>
</div>

<div id="Circoviridae" class="tabcontent">
  <h3><i>Circoviridae</i></h3>
<p>
<br>
Many animal-infecting CRESS-DNA viruses are classified into the <a href="http://jgv.microbiologyresearch.org/content/journal/jgv/10.1099/jgv.0.000871"><i>Circoviridae</i> family</a>.  There are two genera within the group, the older <i>Circovirus</i> and the more recently codified <i>Cyclovirus</i>, but both are well represented.  At least one disease of economic importance is associated with circovirus infections: <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3652492/">post-weaning maturation wasting syndrome</a> in pigs (caused in part by porcine circovirus 2, which is now largely controlled through <a hfref="https://www.ncbi.nlm.nih.gov/pubmed/27769529">vaccination in commercial hog production</a>).  However, several worldwide veterinary diseases are due to circoviruses, including <a href="https://en.wikipedia.org/wiki/Psittacine_beak_and_feather_disease">beak and feather disease</a> and <a href="https://www.ncbi.nlm.nih.gov/pubmed/28242782">fatal acute diarrhea</a> in dogs.
</p>
<figure>
	<img class=scaled src="../DogCV.png", alt='missing' />
	<figcaption><a href="https://wwwnc.cdc.gov/eid/article/19/4/12-1390-f2">Gastrointestinal system of dogs infected with dog circovirus</a> (DogCV) with hemorrhaging in stomach and intestines. CC-BY Li et al. 2013</figcaption>
</figure>
<figure>
	<img class=scaled src="../PCV2.jpg", alt='missing' />
	<figcaption><a href="https://virologyj.biomedcentral.com/articles/10.1186/1743-422X-8-291">Immune electron microscopy image of PCV2</a> (porcine circovirus 2) particles.  CC-BY Guo et al. 2011</figcaption>
</figure>
<p>
While some of the environmental isolates assigned to <i>Circoviridae</i> have genomes over 3,000 and 4,000 bases, it also contains some of the smallest genomes of CRESS-DNA viruses - some well-studied circoviruses have genomes  about 1700nt long, and circularized putative genomes from metagenomics studies can be even smaller.  Most analyzed sequences have two ORFs: the replication-associated protein (Rep, also referred to as the replication initiator protein) and capsid protein (Cp or Cap), with some isolates having had a third ORF experimentally verified, and some sequences having many hypothetical ORFs called that have not yet been studied in the lab.
</p>
<p>
Both cycloviruses and circoviruses have non-enveloped, icosahedral virions of 15-25nm encapsidating their circular, ssDNA genomes, but while members of <i>Circovirus</i> are found infecting or associated with mammals, birds and fish, cycloviruses have been found infecting or associated with mammals, birds and insects.  Sequences assigned to <i>Circovirus</i> have ambisense genomes, with the Rep gene in sense, sequences in Cyclovirus typically are ambisense in the opposite orientation (Rep gene in anti-sense).
</p>
<p>
A great <a href="http://jgv.microbiologyresearch.org/content/journal/jgv/10.1099/jgv.0.000871">primer</a> on <i>Circoviridae</i>
</p>
<p>
For more information about <i>Circovirus</i>:
<br>
<a href="https://talk.ictvonline.org/ictv-reports/ictv_online_report/ssdna-viruses/w/circoviridae/659/genus-circovirus">ICTV report</a> on circovirus<br>
<a href="https://viralzone.expasy.org/118">ExPASy ViralZone summary of circovirus</a>
Type species: <i>Porcine circovirus</i> 1 (<a href="https://www.ncbi.nlm.nih.gov/nuccore/12280941">NC_001792.2</a>)
</p>
<p>
For more information about <i>Cyclovirus</i>:
<br>
<a href="https://talk.ictvonline.org/ictv-reports/ictv_online_report/ssdna-viruses/w/circoviridae/660/genus-cyclovirus">ICTV report</a> on cyclovirus<br>
<a href="https://viralzone.expasy.org/7296">ExPASy ViralZone summary of cyclovirus</a>
Type species: <i>Human-associated cyclovirus 8</i> (<a href="https://www.ncbi.nlm.nih.gov/nuccore/KF031466">KF031466</a>)
</p>
</div>

<div id="Nanoviridae" class="tabcontent">
<h3><i>Nanoviridae</i></h3>
<p>
The plant infecting CRESS-DNA viruses with more than two genomic segments belong in the family <a href="https://talk.ictvonline.org/ictv-reports/ictv_9th_report/ssdna-viruses-2011/w/ssdna_viruses/149/nanoviridae"><i>Nanoviridae</i></a>, which includes the genera <i>Babuvirus</i> and <i>Nanovirus</i>. One of the most economically important species in the family <i>Nanoviridae</i> is Banana bunchy top virus (BBTV), the type species of babuvirus. BBTV causes <a href="http://www.promusa.org/Bunchy+top">banana bunchy top disease</a>, which is common in banana growing areas such as Southeast Asia, the South Pacific, India and Africa. This virus is transmitted by the banana aphid and causes <a href="http://www.musarama.org/en/image/bunchy-top-symptom-81.html">plant crumpling, shrinking and chlorosis</a>, which may develop into necrosis.
<br>
<figure>
	<img class=scaled src="../bbv.jpg", alt='missing', width="512", height="384"/>
	<figcaption>Banana bunchy top, caused by Banana bunchy top virus (BBTV).  CC-BY Scott Nelson 2014.</figcaption>
</figure>

<p>
Viruses in the Family Nanoviridae have <a href="https://talk.ictvonline.org/ictv-reports/ictv_9th_report/ssdna-viruses-2011/w/ssdna_viruses/149/nanoviridae">multipartite genomes</a> consisting of 6 to 8 ~1000 nucleotide segments of circular ssDNA. Five of these DNA components are shared between babuviruses and nanoviruses. <a href="https://talk.ictvonline.org/ictv-reports/ictv_9th_report/ssdna-viruses-2011/w/ssdna_viruses/150/nanoviridae-figures">(DNA-R, -N, -S, -C and -M)</a>. Nanoviruses infect <a href="http://theseedsite.co.uk/monocots2.html">dicots</a>, have 8 genomic DNAs and may include three other DNA components with functions that have yet to be determined (DNA-U1, -U2 and U-4). Babuviruses infect <a href="http://theseedsite.co.uk/monocots2.html">monocots</a>, have 6 genomic DNAs and may include another DNA component with an unknown function (DNA-U4). Each of these components encode a single ORF that is transcribed in one direction, thogh a second putative ORF has been identified on one segment of BBTV (DNA-R). The virions are non-enveloped, sized 17-20nm in diameter and have on CP (coat protein). Additional DNA segments (alphasatellites) are also associated with many viruses in the family and can alter disease symptoms.
</p>

<p>
For more information about Nanovirus:
<br>
<a href="https://talk.ictvonline.org/ictv-reports/ictv_9th_report/ssdna-viruses-2011/w/ssdna_viruses/149/nanoviridae">ICTV report</a> on nanovirus.
<br>
<a href="https://viralzone.expasy.org/565?outline=all_by_species">ExPASy ViralZone summary of nanovirus</a>
<br>
Type Species: <i>Subterranean clover stunt virus</i> (<a href="https://www.ncbi.nlm.nih.gov/nuccore/NC_003818.1">NC_003818.1</a>)                                
</p>

<p>
For more information about Babuvirus:
<br>
<a href="https://talk.ictvonline.org/ictv-reports/ictv_9th_report/ssdna-viruses-2011/w/ssdna_viruses/149/nanoviridae">ICTV report</a> on babuvirus.
<br>
<a href="https://viralzone.expasy.org/564?outline=all_by_species">ExPASy ViralZone summary of babuvirus</a>
<br>
Type Species: <i>Banana bunchy top virus</i> (<a href="https://www.ncbi.nlm.nih.gov/nuccore/NC_003479.1">NC_003479.1</a>)
</p>
</div>

<div id="Classifier" class="tabcontent">
  <h3>Taxonomy</h3>
  <form action="classifier2.py" method="post"><br>
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
			<li><strike>Gemyvongvirus</strike></li>
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
			<ul>
			<li>Huchismacovirus</li>
			<li>Porprismacovirus</li>
			</ul>
		<li>Bacilladnaviridae</li>	
			<ul>
			<li>Protobacilladnavirus</li>
			</ul>
</ul>  		</p>
</div>
<div id="Contact" class="tabcontent">
  <h3>Contact</h3>
  <p>This site is under construction</p>
	<p>Please be patient while we tidy up a bit!</p>

</div> 

<div id="Contributers" class="tabcontent">
  <h3>Contributors</h3>
  <p>This site is under construction</p>
	<p>Please be patient while we tidy up a bit!</p>

</div> 

<div id="Results" class="tabcontent">
  <h3>Results</h3>
  <p>Results from Taxonomy prediction</p>

"""  

#Page contents, second part (results fit between body1 and body2)
body2="""<p><br><br>This classifier will return the best fit of the submitted sequence to the training data.<br>
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
			<li><strike>Gemyvongvirus</strike></li>
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
			<ul>
			<li>Huchismacovirus</li>
			<li>Porprismacovirus</li>
			</ul>
		<li>Bacilladnaviridae</li>	
			<ul>
			<li>Protobacilladnavirus</li>
			</ul>
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

#build the output page
page=header+body1+home+aboutus+classifier+circovirus+contact+results1+resultsTable+results2+body2+footer

#send the output as html 	
print (page)	
quit()

