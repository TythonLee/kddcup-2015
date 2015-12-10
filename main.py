# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:38:38 2015

@author: litaisong
"""
import pandas as pd
import numpy as np
import time
import datetime
from sklearn import preprocessing

def read_user(filename):
    return pd.read_csv(filename)

def rfc(X,y,Z,test_data):    
    # Random Forest model
    from sklearn.ensemble import RandomForestClassifier
    rfclf = RandomForestClassifier(n_estimators=100, max_features='auto')
    rfclf.fit(X, y)
    test_probs_rf = rfclf.predict_proba(Z)[:, 1]
    # create a DataFrame to store my submissions
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 'truth':test_probs_rf}).set_index("enrollment_id")
    #sub = sub[sub["buy"]!=0]
    # write the submission to a CSV file
    sub.truth = sub.truth.where(sub.truth >= 0.5, 0)
    sub.truth = sub.truth.where(sub.truth < 0.5, 1)
    sub = sub[['truth']].astype('int')
    sub.to_csv('data\\result\\first_rfc.csv')

def rfr(X,y,Z,test_data):
    from sklearn.ensemble import RandomForestRegressor
    clf = RandomForestRegressor(n_estimators=60, max_features='sqrt')   
    clf.fit(X, y)
    test_probs_rf = clf.predict(Z)
    print '-----------------------------------------'
    print test_probs_rf     
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 'truth':test_probs_rf}).set_index("enrollment_id")
    #sub = sub[sub["buy"]!=0]
    # write the submission to a CSV file
    sub.truth = sub.truth.where(sub.truth >= 0.5, 0)
    sub.truth = sub.truth.where(sub.truth < 0.5, 1)
    sub = sub[['truth']].astype('int')
    sub.to_csv('data\\result\\second_rfr_1.csv')
    
def lr(X,y,Z,test_data):
    from sklearn.linear_model import LogisticRegression  
    lr = LogisticRegression()
    lr.fit(X, y)

    # calculate predicted probabilities on testing data
    test_probs_lr = lr.predict_proba(Z)[:, 1]
    # create a DataFrame to store my submissions
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 'truth':test_probs_lr}).set_index("enrollment_id")
    #sub = sub[sub["buy"]!=0]
    # write the submission to a CSV file
    #sub.truth = sub.truth.where(sub.truth >= 0.5, 0)
    #sub.truth = sub.truth.where(sub.truth < 0.5, 1)
    #sub = sub[['truth']].astype('int')
    sub.to_csv('data\\result\\third_lr_1.csv')
    
def gbdt(X,y,Z,test_data):
    from sklearn.ensemble import GradientBoostingClassifier
    gbdt = GradientBoostingClassifier(n_estimators=200,max_depth=5)
    gbdt.fit(X, y)  # 训练。喝杯咖啡吧
        
    test_probs_gbdt = gbdt.predict_proba(Z)[:, 1]
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 
                        'truth':test_probs_gbdt}).set_index("enrollment_id") 
    sub.to_csv('data\\result\\fourth_gbdt_28.csv')
    '''
    GradientBoostingClassifier(init=None, learning_rate=0.1, loss='deviance',  
              max_depth=3, max_features=None, max_leaf_nodes=None,
              min_samples_leaf=1, min_samples_split=2,
              min_weight_fraction_leaf=0.0, n_estimators=100,
              random_state=None, subsample=1.0, verbose=0,
              warm_start=False)
    '''
    print gbdt.feature_importances_   # 据此选取重要的特征
    ##array([  2.08644807e-06,   0.00000000e+00,   8.93452010e-04, ...,  5.12199658e-04,   0.00000000e+00,   0.00000000e+00])
    #gbdt.feature_importances_.shape
    ##(19630,)  
    
def gbdt_feature(X,y,Z):
    
    from sklearn.ensemble import GradientBoostingClassifier
    gbdt = GradientBoostingClassifier(n_estimators=200,max_depth=5)
    gbdt.fit(X, y)  # 训练。喝杯咖啡吧
    
    f = gbdt.transform(Z, threshold=None)
    ff = pd.DataFrame(f)
    ff.columns = ['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10',
        'f11','f12','f13','f14','f15','f16','f17','f18','f19','f20','f21']   
        
    feature_all = read_user('data\\test\\feature_all_15.csv')
    feature_all1 = pd.merge(feature_all,ff,how='outer',left_index=True,right_index=True)
    feature_all1.set_index('enrollment_id').to_csv('data\\test\\feature_all_16.csv')    
    
    
def mnb(X,y,Z,test_data):  
    from sklearn.naive_bayes import MultinomialNB
    mnb = MultinomialNB() 
    mnb.fit(X,y)
    #MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)  
    test_probs_mnb = mnb.predict_proba(Z)[:1]
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 
                        'truth':test_probs_mnb}).set_index("enrollment_id")
    sub.to_csv('data\\result\\fifth_mnb.csv')
    
def bnb(X,y,Z,test_data):  
    from sklearn.naive_bayes import BernoulliNB
    bnb = BernoulliNB()
    bnb.fit(X,y)
    #MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)  
    test_probs_bnb = bnb.predict_proba(Z)[:, 1]
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"], 
                        'truth':test_probs_bnb}).set_index("enrollment_id")
    sub.to_csv('data\\result\\sixth_bnb.csv')

def svc(X,y,Z,test_data):
    from sklearn.svm import SVC
    svc = SVC(probability=True)
    svc.fit(X, y) 
    test_probs_svc = svc.predict_proba(Z)[:1]
    sub = pd.DataFrame({'enrollment_id':test_data["enrollment_id"],
                        'truth':test_probs_svc}).set_index("enrollment_id")
    sub.to_csv('data\\result\\seventh_svc.csv')
    
def validate(X,y):
    from sklearn.cross_validation import cross_val_score    
    
    from sklearn.ensemble import RandomForestRegressor
    clf = RandomForestRegressor(n_estimators=100, max_features='auto')  
    
    from sklearn.ensemble import RandomForestClassifier
    rfclf = RandomForestClassifier(n_estimators=100, max_features='auto')
    
    from sklearn.linear_model import LogisticRegression  
    lr = LogisticRegression()
    
    from sklearn.ensemble import GradientBoostingClassifier
    gbdt = GradientBoostingClassifier(n_estimators=100,max_depth=3)#100,3	
    
    from sklearn.naive_bayes import MultinomialNB
    mnb = MultinomialNB() 
    
    from sklearn.naive_bayes import BernoulliNB
    bnb = BernoulliNB()
    
    from sklearn.svm import SVC
    svc = SVC()
    #svc.fit(X, y)     
    
    scores_rfclf = cross_val_score(rfclf, X, y, cv=5, scoring='roc_auc')
    #cv是交叉验证的份数。k-fold cross-validation,cv=k,scoring='roc_auc'
    print scores_rfclf
    print np.mean(scores_rfclf)
    
    scores_lr = cross_val_score(lr, X, y, cv=5, scoring='roc_auc')
    #cv是交叉验证的份数。k-fold cross-validation,cv=k,scoring='roc_auc'
    print scores_lr
    print np.mean(scores_lr)
    
    scores_bnb = cross_val_score(bnb, X, y, cv=5, scoring='roc_auc')
    #cv是交叉验证的份数。k-fold cross-validation,cv=k,scoring='roc_auc'
    print scores_bnb
    print np.mean(scores_bnb)
    
    return scores_rfclf    
    
if __name__ == '__main__':
    start_time = time.time()
    
    user_train = read_user('data\\train\\feature_all_19_g30.csv')
    user_test = read_user('data\\test\\feature_all_19_g30.csv')
    
    result = read_user('data\\train\\truth_train.csv')
    '''
    cols = [
    "0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","209",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30",
    "31","32","33","34","35","36","37","38","39","40","41","42","43","44","45",
    "46","47","48","49","50","51","52","53","54","55","56","57","58","59","60",
    "61","62","63","64","65","66","67","68","69","70","71","72","73","74","75",
    "76","77","78","79","80","81","82","83","84","85","86","87","88","89","90",
    "91","92","93","94","95","96","97","98","99","100","101","102","103","104",
    "105","106","107","108","109","110","111","112","113","114","115","116","117",
    "118","119","120","121","122","123","124","125","126","127","128","129","130",
    "131","132","133","134","135","136","137","138","139","140","141","142","143",
    "144","145","146","147","148","149","150","151","152","153","154","155","156",
    "157","158","159","160","161","162","163","164","165","166","167","168","169",
    "170","171","172","173","174","175","176","177","178","179","180","181","182",
    "183","184","185","186","187","188","189","190","191","192","193","194","195",
    "196","197","198","199","200","201","202","203","204","205","206","207","208",
    
    "category0","category1","category2","category3","category4","category5","category6","category7",
    "category8","category9","category10","category11","category12","category13","category14","category_all",
    "users_per_course_all","courses_per_user_all","source_num","duration_days"
    ]
    
    cols = [
    "0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","209",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30",
    "31","32","33","34","35","36","37","38","39","40","41","42","43","44","45",
    "46","47","48","49","50","51","52","53","54","55","56","57","58","59","60",
    "61","62","63","64","65","66","67","68","69","70","71","72","73","74","75",
    "76","77","78","79","80","81","82","83","84","85","86","87","88","89","90",
    "91","92","93","94","95","96","97","98","99","100","101","102","103","104",
    "105","106","107","108","109","110","111","112","113","114","115","116","117",
    "118","119","120","121","122","123","124","125","126","127","128","129","130",
    "131","132","133","134","135","136","137","138","139","140","141","142","143",
    "144","145","146","147","148","149","150","151","152","153","154","155","156",
    "157","158","159","160","161","162","163","164","165","166","167","168","169",
    "170","171","172","173","174","175","176","177","178","179","180","181","182",
    "183","184","185","186","187","188","189","190","191","192","193","194","195",
    "196","197","198","199","200","201","202","203","204","205","206","207","208",
    
    "event0","event1","event2","event3","event4","event5","event6","all_events",
    
    "category0","category1","category2","category3","category4","category5","category6","category7",
    "category8","category9","category10","category11","category12","category13","category14","category_all",
    
    "users_per_course_all","courses_per_user_all","source_num","duration_days",
    'user_weekday00','user_weekday11','user_weekday22','user_weekday33','user_weekday44','user_weekday55','user_weekday66',
    'weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66'
    ]
    '''
    cols = [
    "day0","day1","day2","day3","day4","day5","day6","day7","day8","day9",
    "day10","day11","day12","day13","day14","day15","day16","day17","day18","day19",
    "day20","day21","day22","day23","day24","day25","day26","day27","day28","day29",
    
    "event0","event1","event2","event3","event4","event5","event6","all_events",
    "users_per_course_all","courses_per_user_all","source_num","day_times","blank_days",
    
    
    'user_weekday00','user_weekday11','user_weekday22','user_weekday33','user_weekday44','user_weekday55','user_weekday66',
    'weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66',
    
    "category0","category1","category2","category3","category4","category5","category6","category7",
    "category8","category9","category10","category11","category12","category13","category14","category_all"
    ]
    cols_100 = ["g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10",
    "g11","g12","g13","g14","g15","g16","g17","g18","g19","g20","g21","g22","g23",
    "g24","g25","g26","g27","g28","g29","g30","g31","g32","g33","g34","g35","g36",
    "g37","g38","g39","g40","g41","g42","g43","g44","g45","g46","g47","g48","g49",
    "g50","g51","g52","g53","g54","g55","g56","g57","g58","g59","g60","g61","g62",
    "g63","g64","g65","g66","g67","g68","g69","g70","g71","g72","g73","g74","g75",
    "g76","g77","g78","g79","g80","g81","g82","g83","g84","g85","g86","g87","g88",
    "g89","g90","g91","g92","g93","g94","g95","g96","g97","g98","g99"
    
    
    "g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14",
    "g15","g16","g17","g18","g19","g20","g21","g22","g23","g24","g25","g26","g27",
    "g28","g29","g30","g31","g32","g33","g34","g35","g36","g37","g38","g39","g40",
    "g41","g42","g43","g44","g45","g46","g47","g48","g49","g50","g51","g52","g53",
    "g54","g55","g56","g57","g58","g59","g60","g61","g62","g63","g64","g65","g66",
    "g67","g68","g69","g70","g71","g72","g73","g74","g75","g76","g77","g78","g79",
    "g80","g81","g82","g83","g84","g85","g86","g87","g88","g89","g90","g91","g92",
    "g93","g94","g95","g96","g97","g98","g99","g100","g101","g102","g103","g104","g105",
    "g106","g107","g108","g109","g110","g111","g112","g113","g114","g115","g116","g117",
    "g118","g119","g120","g121","g122","g123","g124","g125","g126","g127","g128","g129",
    "g130","g131","g132","g133","g134","g135","g136","g137","g138","g139","g140","g141",
    "g142","g143","g144","g145","g146","g147","g148","g149","g150","g151","g152","g153",
    "g154","g155","g156","g157","g158","g159","g160","g161","g162","g163","g164","g165",
    "g166","g167","g168","g169","g170","g171","g172","g173","g174","g175","g176","g177",
    "g178","g179","g180","g181","g182","g183","g184","g185","g186","g187","g188","g189",
    "g190","g191","g192","g193","g194","g195","g196","g197","g198","g199"
    ]
    #"courses_per_user","all_events","source_num","day_times","blank_days","muti_ad","muti_ab",
    #"users_per_course_all","courses_per_user_all",
    
    #"category0","category1","category2","category3","category4","category5","category6","category7",
    #"category8","category9","category10","category11","category12","category13","category14","category_all",
    
    #"weekday1", "weekday2", "weekday3","weekday4", "weekday5","weekday6","weekday7",
    #'user_weekday00','user_weekday11','user_weekday22','user_weekday33','user_weekday44','user_weekday55','user_weekday66',
    #'weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66',
    
    #"day0","day1","day2","day3","day4","day5","day6","day7","day8","day9",
    #"day10","day11","day12","day13","day14","day15","day16","day17","day18","day19",
    #"day20","day21","day22","day23","day24","day25","day26","day27","day28","day29",
    
    #'f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11',
    #'f12','f13','f14','f15','f16','f17','f18','f19','f20','f21'
    '''
    courses_per_user:每个用户username的选课数
    courses_per_user_all:（训练集+测试集）每个用户username的选课数
    users_per_course_all：（训练集+测试集）每门课的选课人数
    all_events：每个enrollment_id的所有events
    source_num：每个enrollment_id访问browser的次数
    day_times：每个enrollment_id的活跃天数
    blank_days：每个enrollment_id的最后活跃日期与第30天的时间差
    muti_ad：all_events*day_times
    muti_ab：all_events/(blank_days+1)
    event0-6：每个enrollment_id产生每个event的总数
    category0-14:一门课下的有15个类别，每个类别下的module数量
    category_all:一门课下含有不同的模块数量
    weekday1-7:30天的特征按间隔7相加得到的特征
    weekday00-66：每个enrollment_id按30天的星期聚类相加
    user_weekday00-66：每个用户按30天的星期聚类相加
    '''        
    cols_30 = [
    "day0","day1","day2","day3","day4","day5","day6","day7","day8","day9",
    "day10","day11","day12","day13","day14","day15","day16","day17","day18","day19",
    "day20","day21","day22","day23","day24","day25","day26","day27","day28","day29",
    
    "event0","event1","event2","event3","event4","event5","event6","all_events",
    "users_per_course_all","courses_per_user_all","source_num","day_times","blank_days",
    
    
    'user_weekday00','user_weekday11','user_weekday22','user_weekday33','user_weekday44','user_weekday55','user_weekday66',
    'weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66',
    
    "category0","category1","category2","category3","category4","category5","category6","category7",
    "category8","category9","category10","category11","category12","category13","category14","category_all",
    "g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14",
    "g15","g16","g17","g18","g19","g20","g21","g22","g23","g24","g25","g26","g27",
    "g28","g29"
    ]
    train_data = pd.merge(user_train, result,how="outer",left_index=True,right_index=True)
    
    X_data = train_data[cols]
    X = preprocessing.normalize(X_data,norm='l1')
    #X = train_data[cols]
    
    
    y = train_data.truth
    
    Z = user_test[cols]
    test_data = read_user('data\\test\\enrollment_test.csv')
    #rfr(X,y,Z,test_data)
    #lr(X,y,Z,test_data)
    #rfc(X,y,test_data)
    gbdt(X,y,Z,test_data)
    #bnb(X,y,Z,test_data)
    #svc(X,y,Z,test_data)
    #score = validate(X,y)
    
    
    
    
    
    
    print 'total time: ',time.time()-start_time 