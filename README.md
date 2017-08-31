# cressdna
Circular Eukaryotic Single Stranded DNA site source

index.html is the main web page
classifier.py is a python script that takes the submitted textarea form from index.html (needs to be FASTA format input) and makes a prediction
              of the CRESS virus genus for each sample, given the caveats listed on the submission form page
              
              This script is meant to output a new index.html type page with the results of the prediction as an HTML table in the Results tab
                           
SVM_linear_aa_clf.pkl is a compressed trained SVM classifier for prediction
UniqRepsGemys_6089_StSCALER.pkl is a compressed trained scaler to fit input data to the same scale as the trained data
