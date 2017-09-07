# ML-Pipeline
Scripts for Shiu Lab Machine Learning

## Environment Requirements
biopython                 1.68
matplotlib                1.5.1
numpy                     1.11.3
pandas                    0.18.1
python                    3.4.4
scikit-learn              0.18.1
scipy                     0.18.1

## Data Preprocessing

### Feature Selection (Azodi)
Available feature selection tools: RandomForest, Chi2, LASSO (L1 penalty), enrichement (Fisher's Exact test).

Example:
<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python Feature_Selection_sklearn.py -df [path/to/dataframe] -f [rf/chi2/lasso/fet] -n [needed for chi2/rf] -p [needed for LASSO/FET] -type [needed for LASSO] -list T </code></pre>
Use -list T/F to either just save a list of selected features (can use as -feat input during model building) or a filtered data frame

### Impute Data (Moore)

This script imputes msising data in a given matrix. Matrices must be separate if data types are different (ie. numeric separate from binary). This script takes at least one matrix, you only need one if you have only one type of data, but if you have multiple types you need to input them separate.

Inputs:
Data matrix- columns should be gene|Class|feature1|feature2| (-df*)

Data types (-dtype*):
1. numeric: n
2. categorical: c
3. binary: b

Available imputation methods (-mv):
1. impute data from a random selection from your data distribution (-mv 1)
2. impute data by using the median for numeric data and the mode for categorical/binary data (-mv 2)
3. drop all rows with NAs (-mv 0)

Example:
<pre><code> python impute_data.py -df1 [path/to/dataframe] -dtype1 [n,c,b] -mv [0,1,2] -df2 [path/to/dataframe2] -dtype2 [n,c,b] -df3 [path/to/dataframe3] -dtype3 [n,c,b]</code></pre>

### Convert categorical data to binary (Moore)

This script converts a categorical matrix to a binary matrix to run on machine-learning algorithms

<pre><code> python get_cat_as_binmatrix.py [categorical_matrix] </code></pre> 

output: [categorical_matrix]_binary.matrix.txt

## Building Models

### Classification
See ML_classification.py docstrings for additional options (and ML_clf_functions.py)

Available model algorithms: RF, SVM, SVMpoly, SVMrbf, Logistic Regression (LogReg)

Example binary classification:
<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python ML_classification.py -df example_Bin.txt -alg [ALG] </code></pre>

Example multiclass classification:
<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python ML_classification.py -df example_MC.txt -alg [ALG] -class Biotech_cluster -cl_train a,b,c -cm T</code></pre>

*Note: To run tests use -gs T -gs_n 3 -n 5 

### Regression
See ML_regression.py docstrings for additional options (and ML_clf_functions.py)

Available model algorithms: RF, SVM, SVMpoly, SVMrbf, GradientBoostingRegressor (GBRT), Linear Regression (LR - no GS)

<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python ML_regression.py -df data.txt -alg [ALG]</code></pre>


## Post-Processing

### AUC-ROC & AUC-PR Plots
Use this code to build plots with multiple classification _scores files.

<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python ML_plots.py [SAVE_NAME] name1 [Path_to_1st_scores_file] name3 [Path_to_2nd_scores_file] etc.</code></pre>

### Compare classifiers (Venn-Diagrams)
Given a set of *_scores.txt results files, output a list of which instances were classified correctly and which incorrectly and summarize with a table of overlaps.
Example:
<pre><code>export PATH=/mnt/home/azodichr/miniconda3/bin:$PATH
python compare_classifiers.py -scores [comma sep list of scores files] -ids [comma sep list of classifier names] -save [out_name]</code></pre>



## TO DO LIST

- Imporve regression model by adding: predicting unknowns, importance scores
- Merge pre-processing scripts so you can deal with NAs, imputations, and one-hot encoding categorical variables in one script.
- Add additional classification models: Naive Bayes, basic neural network (1-2 layers)
- Add validation set hold out option

