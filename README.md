# kddcup-2015
kddcup 2015 challenge of predicting dropout in MOOCs

system：windows7 X64
software requirement：Python 2.7, pandas, scikit-learn, numpy
Dataset:KDDCup 2015 dataset, provided by MOOCs
Website:http://www.kddcup2015.com/information-introduction.html

Step1:unzip your dataset into two files:train,test
train includes:enrollment_test.csv,log_test.csv
test includes:enrollment_train.csv,log_train.csv,truth_train.csv

Step2:dataConvert.py:transform string into integer

Step3:create a new file "enrollment",then copy enrollment_test_num.csv and enrollment_train_num.csv into this file. Combine 2 csv file into a new one--"enrollment_all_num.csv"

Step4:libFM file have many features from gbdt model; Also train2.csv in file train and test2.csv in file test are 210 dimensionalities features derive from dataset.

Step5: dataAnalyse.py: derive a variety of features from dataset

Step6: main.py: using feature set for training and predicting