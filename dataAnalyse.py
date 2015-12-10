# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:50:17 2015

@author: litaisong
"""

import pandas as pd
import numpy as np
import time
import datetime

def read_user(filename):
    #return pd.read_csv(filename, index_col=[5],parse_dates=["time"])
    return pd.read_csv(filename)
    
def session_duration(user):
    # 每一门课的开课时长（天）
    timestamp_by_session = user[["enrollment_id","time"]].groupby("enrollment_id")
    print timestamp_by_session
    print '-----============='
    mints = timestamp_by_session.min()
    maxts = timestamp_by_session.max()
    min0 = pd.to_datetime(mints["time"])
    max0 = pd.to_datetime(maxts["time"])
    min1 = min0.to_frame(name = "time")
    max1 = max0.to_frame(name = "time")

    duration = max1 - min1
    duration.columns = ["duration"]
    print duration.describe()

    # KDE of session duration in seconds
    # 将年月日格式的时长转化为小时
    #duration_in_s = duration["duration"] / np.timedelta64(1, 's')
    duration_in_h = duration["duration"] / np.timedelta64(1, 'h')
    duration_in_h = duration_in_h.to_frame(name="duration")
    print duration_in_h

def day_events():
    #用户在开课的30天中每天的event数量，生成30features_test.csv
    #enroll = pd.read_csv('data\\train\\enrollment_train_num.csv')
    user = read_user('data\\train\\log_train_num.csv')
    enroll = pd.read_csv('data\\train\\enrollment_train_num.csv')
    enroll = enroll[["enrollment_id","course_id_num"]]
    user_en = user["enrollment_id"]
    user_co = user["course_id_num"]
    
    user_coix = user[["course_id_num","time"]]
    all_time = pd.to_datetime(user_coix["time"])
    date_time = all_time.apply(lambda x : x.date())
    d1 = date_time.to_frame(name="date")
    d2 = user_co.to_frame(name="course_id_num")
    d3 = pd.merge(d2,d1,how="outer",left_index=True,right_index=True)
    d4 = d3.drop_duplicates()
    #d5 = d4[d4["course_id_num"]==0][["date"]].set_index("date")
    user_ent = user[["enrollment_id","time"]]
    all_time1 = pd.to_datetime(user_ent["time"])
    date_time1 = all_time1.apply(lambda x : x.date())
    e1 = date_time1.to_frame(name="date")
    e2 = user_en.to_frame(name="enrollment_id")
    e3 = pd.merge(e2,e1,how="outer",left_index=True,right_index=True)
    e4 = pd.merge(e3,e1,how="outer",left_index=True,right_index=True)
    
    e5 = e4.groupby(["enrollment_id","date_x"]).count()
    e6 = e5.copy()
    e6.reset_index(level=0, inplace=True)
   
    
    for i in range(len(enroll)):
        print i
        
        e7 = e6[e6["enrollment_id"]==enroll.iat[i,0]][["date_y"]]
        d5 = d4[d4["course_id_num"]==enroll.iat[i,1]][["date"]].set_index("date")
        
        c = pd.merge(e7,d5,how="outer", left_index = True, right_index=True)
        c.fillna(0, inplace=True)
        d = c[["date_y"]]
        
        
        f = open('data\\train\\30features_train.csv','a')
        for j in range(29):
            f.write(str(int(d.iat[j,0]))+',')
        f.write(str(int(d.iat[29,0]))+'\n')
        f.close()
        
def courses_per_user():
    #用户的选课数量，生成courses_per_user_test.csv
    user = read_user('data\\train\\log_train_num.csv')
    a = user[['username','course_id_num']].drop_duplicates()
    b = a.groupby(['username']).count()
    c = user.set_index('username')
    d = c[['enrollment_id']]
    e = pd.merge(d,b,how="outer",left_index=True,right_index=True)
    f = e.set_index('enrollment_id')
    f.sort_index(inplace=True)
    f.columns = ["courses_per_user"]
    f.to_csv('data\\train\\courses_per_user_train.csv')


def ensemble_features():
    #将新的特征加入到30天特征后
    feature1 = read_user('data\\train\\30features_train.csv')#两处改动
    feature2 = read_user('data\\train\\courses_per_user_train.csv').drop_duplicates().set_index("enrollment_id")
    
    enroll = read_user('data\\train\\enrollment_train.csv')
    
    a = enroll[['enrollment_id']]
    c = pd.merge(a,feature1,how='outer',left_index=True,right_index=True)
    d = c.set_index("enrollment_id")
    d.to_csv('data\\train\\30features_train.csv')
    
    
    #newcol = feature2['courses_per_user']
    #feature_all = feature1.assign(courses_per_user=newcol)
    feature_all = pd.merge(d,feature2,how='outer',left_index=True,right_index=True)
    feature_all.to_csv('data\\train\\feature_all.csv')

def all_events(user):
    #用户的event总和.生成feature_all_1.csv
    u1 = user[['enrollment_id','event_num']]
    u2 = u1.groupby(['enrollment_id']).count()
    u2.columns = ["all_events"]
    u2.to_csv('data\\train\\all_events_train.csv')#两处改动
    
    feature_all = read_user('data\\train\\feature_all.csv').set_index("enrollment_id")
    feature_all1 = pd.merge(feature_all,u2,how='outer',left_index=True,right_index=True)
    feature_all1.to_csv('data\\train\\feature_all_1.csv')
    
    
def source(user):
    #enrollment_id访问browser的次数.生成feature_all_2.csv
    u1 = user[['enrollment_id','source_num']]
    u2 = u1.groupby(['enrollment_id']).sum()
    u2.to_csv('data\\train\\source_num.csv')
    
    feature_all = read_user('data\\train\\feature_all_1.csv').set_index("enrollment_id")
    feature_all1 = pd.merge(feature_all,u2,how='outer',left_index=True,right_index=True)
    feature_all1.to_csv('data\\train\\feature_all_2.csv')

def last_event():
    #用户在30天中上课的天数.生成feature_all_3.csv
    f1 = read_user('data\\train\\30features_train.csv')
    len_f1 = len(f1)
    array_event=[]
    for i in range(len_f1):
        print i
        a = f1.loc[i].values
        b = a[a>0].size
        array_event.append(b)
        
    print  array_event   
    day_times = pd.DataFrame({'day_times':array_event})
    
    feature_all = read_user('data\\train\\feature_all_2.csv')
    feature_all1 = pd.merge(feature_all,day_times,how='outer',left_index=True,right_index=True)
    feature_all1.set_index("enrollment_id").to_csv('data\\train\\feature_all_3.csv')

def blank_days():
    #用户最后一次的action日期距离第30天的时差。生成feature_all_4.csv
    f1 = read_user('data\\train\\30features_train.csv')
    len_f1 = len(f1)
    array_days=[]
    for i in range(len_f1):
        print i
        a = f1.loc[i].values    
        for j in range(29,-1,-1):
            if (a[j]==0):
                continue
            else:
                b = 29-j
                array_days.append(b)
                break
    print array_days     
    blank_days = pd.DataFrame({'blank_days':array_days})
    
    feature_all = read_user('data\\train\\feature_all_3.csv')
    feature_all2 = pd.merge(feature_all,blank_days,how='outer',left_index=True,right_index=True)
    feature_all2.set_index("enrollment_id").to_csv('data\\train\\feature_all_4.csv')   
        
def muti_features1():
    #将all_events*day_times，即用户的所有events乘以用户活跃的天数。生成feature_all_5.csv
    feature_4 = read_user('data\\train\\feature_all_4.csv')[["all_events","day_times","blank_days"]]
    all_events = feature_4["all_events"]
    day_times = feature_4["day_times"]
    muti_ad = all_events*day_times
    muti_ad = muti_ad.to_frame(name = "muti_ad")
    
    feature_all = read_user('data\\train\\feature_all_4.csv')
    feature_all2 = pd.merge(feature_all,muti_ad,how='outer',left_index=True,right_index=True)
    feature_all2.set_index("enrollment_id").to_csv('data\\train\\feature_all_5.csv') 
 
def muti_features2():
    #将all_events/blank_days，即enrollment_id的所有events除以用户后期不活跃的天数+1。生成feature_all_6.csv
    feature_5 = read_user('data\\train\\feature_all_5.csv')[["all_events","day_times","blank_days"]]
    all_events = feature_5["all_events"]
    blank_days = feature_5["blank_days"]+1
    muti_ab = all_events/blank_days
    muti_ab = muti_ab.to_frame(name = "muti_ab")
    
    feature_all = read_user('data\\train\\feature_all_5.csv')
    feature_all2 = pd.merge(feature_all,muti_ab,how='outer',left_index=True,right_index=True)
    feature_all2.set_index("enrollment_id").to_csv('data\\train\\feature_all_6.csv') 

def features_210():
    #将30天特征扩展成30*7=210维，7表示7类events,生成feature_all_7.csv
    feature_210 = read_user('data\\train\\train2.csv')#两处改动
    
    feature_all = read_user('data\\train\\feature_all_6.csv')
    feature_all2 = pd.merge(feature_210,feature_all,how='outer',left_index=True,right_index=True)
    feature_all2.set_index("enrollment_id").to_csv('data\\train\\feature_all_7.csv') 


def events_7():
    #每个enrollment_id产生event{0,1,...,6}的次数
    events = read_user("data\\train\\log_train_num.csv")[['enrollment_id','event_num']]
    user = read_user('data\\train\\feature_all_7.csv')
    events_en = user[['enrollment_id']].set_index('enrollment_id')
    
    for i in range(7):
        events_cnt =  events[events['event_num']==i].groupby(['enrollment_id']).count()
        events_cnt.columns = ['event'+str(i)]
        events_en = pd.merge(events_en,events_cnt,how='outer',left_index=True,right_index=True)
    events_en.fillna(0,inplace=True)
    events_en = events_en.astype('int')
    
    feature_all = user.set_index('enrollment_id')
    feature_all2 = pd.merge(feature_all,events_en,how='outer',left_index=True,right_index=True)
    feature_all2.to_csv('data\\train\\feature_all_8.csv')
    
def duration_days():
    #用户最后一次的action日期距离第30天的时差。生成feature_all_9.csv
    f1 = read_user('data\\train\\30features_train_1.csv')
    len_f1 = len(f1)
    array_days=[]
    for i in range(len_f1):
        print i
        a = f1.loc[i].values
        for k in range(1,31):
            if(a[k]==0):
                continue
            else:
                begin = k
                break
                
        for j in range(30,0,-1):
            if (a[j]==0):
                continue
            else:
                end = j
                array_days.append(end-begin+1)
                break
    print array_days     
    duration_days = pd.DataFrame({'duration_days':array_days})
    
    feature_all = read_user('data\\train\\feature_all_8.csv')
    feature_all2 = pd.merge(feature_all,duration_days,how='outer',left_index=True,right_index=True)
    feature_all2.set_index("enrollment_id").to_csv('data\\train\\feature_all_9.csv')   

def courses_per_user_all():
    #训练集+测试集中，每个用户的选课数。生成文件feature_all_10.csv
    u1 = read_user('data\\enrollment\\enrollment_all_num.csv')
    u2 = u1[['username','course_id_num']].groupby(['username']).count()
    u2.columns = ['courses_per_user']
    u3 = u1.copy().set_index('username')[['enrollment_id']]
    e = pd.merge(u3,u2,how="outer",left_index=True,right_index=True)
    f = e.set_index('enrollment_id')
    f.sort_index(inplace=True)
    
    train = read_user('data\\train\\enrollment_train_num.csv')
    test = read_user('data\\test\\enrollment_test_num.csv')
    tr1 = train[['enrollment_id']].set_index('enrollment_id')
    tr1m = pd.merge(tr1,f,how="inner",left_index=True,right_index=True)
    tr1m.columns = ['courses_per_user_all']
    te1 = test[['enrollment_id']].set_index('enrollment_id')
    te1m = pd.merge(te1,f,how="inner",left_index=True,right_index=True)
    te1m.columns = ['courses_per_user_all']
    
    feature_all = read_user('data\\train\\feature_all_9.csv').set_index('enrollment_id')
    feature_all1 = pd.merge(feature_all,te1m,how='outer',left_index=True,right_index=True)
    feature_all1.to_csv('data\\train\\feature_all_10.csv')
    

def users_per_course_all():
     #训练集+测试集中，每个课程的用户数。生成文件feature_all_11.csv
    u1 = read_user('data\\enrollment\\enrollment_all_num.csv')
    u2 = u1[['username','course_id_num']].groupby(['course_id_num']).count()
    u2.columns = ['users_per_course']
    u3 = u1.copy().set_index('course_id_num')[['enrollment_id']]
    e = pd.merge(u3,u2,how="outer",left_index=True,right_index=True)
    f = e.set_index('enrollment_id')
    f.sort_index(inplace=True)
    
    train = read_user('data\\train\\enrollment_train_num.csv')
    test = read_user('data\\test\\enrollment_test_num.csv')
    tr1 = train[['enrollment_id']].set_index('enrollment_id')
    tr1m = pd.merge(tr1,f,how="inner",left_index=True,right_index=True)
    tr1m.columns = ['users_per_course_all']
    te1 = test[['enrollment_id']].set_index('enrollment_id')
    te1m = pd.merge(te1,f,how="inner",left_index=True,right_index=True)
    te1m.columns = ['users_per_course_all']
    
    feature_all = read_user('data\\test\\feature_all_10.csv').set_index('enrollment_id')
    feature_all1 = pd.merge(feature_all,te1m,how='outer',left_index=True,right_index=True)
    feature_all1.to_csv('data\\test\\feature_all_11.csv')  
    
    feature_all2 = read_user('data\\train\\feature_all_10.csv').set_index('enrollment_id')
    feature_all3 = pd.merge(feature_all2,tr1m,how='outer',left_index=True,right_index=True)
    feature_all3.to_csv('data\\train\\feature_all_11.csv')  

        
def course_feature():
    user = read_user('data\\object\\object_num2.csv')[['course_id_num','module_id','category_num','start','children']]
    #total1 = user[['course_id_num','module_id']].groupby(['course_id_num']).count()
    total2 = user[['course_id_num','module_id']].drop_duplicates().groupby(['course_id_num']).count()
    total2.columns = ['category_all']
    part = user[['course_id_num','module_id','category_num']].drop_duplicates()
    part1 = part[['course_id_num','category_num']]
    part_en = user[['course_id_num']].drop_duplicates().set_index('course_id_num')    
    
    for i in range(15):
        category_cnt = part1[part1['category_num']==i].groupby(['course_id_num']).count()
        
        category_cnt.columns = ['category'+str(i)]
        part_en = pd.merge(part_en,category_cnt,how='outer',left_index=True,right_index=True)
    part_all = pd.merge(part_en,total2,how='outer',left_index=True,right_index=True)
    part_all.fillna(0,inplace=True)
    part_all = part_all.astype('int')
    
    
    enroll = read_user('data\\train\\enrollment_train_num.csv')[['enrollment_id','course_id_num']].set_index('course_id_num')
    part_enroll = pd.merge(enroll,part_all,how='outer',left_index=True,right_index=True)
    part_enroll_1 = part_enroll.set_index('enrollment_id')#ort_index(inplace=True)
   
    
    feature_all = read_user('data\\train\\feature_all_11.csv').set_index('enrollment_id')
    feature_all2 = pd.merge(feature_all,part_enroll_1,how='outer',left_index=True,right_index=True)
    feature_all2.to_csv('data\\train\\feature_all_12.csv')   
    '''
    feature_all = user.set_index('enrollment_id')
    feature_all2 = pd.merge(feature_all,events_en,how='outer',left_index=True,right_index=True)
    feature_all2.to_csv('data\\test\\feature_all_8.csv')    
    '''  
    
def events_by_week():
    #feature_all_13
    user = read_user('data\\train\\feature_all_12.csv')
    cols = ["day0","day1","day2","day3","day4","day5","day6","day7","day8","day9",
            "day10","day11","day12","day13","day14","day15","day16","day17","day18","day19",
            "day20","day21","day22","day23","day24","day25","day26","day27","day28","day29"]
    
    weekday1 = user[cols[0]] 
    weekday2 = user[cols[1]] 
    weekday3 = user[cols[2]] 
    weekday4 = user[cols[3]] 
    weekday5 = user[cols[4]] 
    weekday6 = user[cols[5]] 
    weekday7 = user[cols[6]] 
    for i in range(1,5):
        weekday1 = weekday1 + user[cols[7*i]] 
        weekday2 = weekday2 + user[cols[7*i+1]] 
    for i in range(1,4):   
        weekday3 = weekday3 + user[cols[7*i+2]] 
        weekday4 = weekday4 + user[cols[7*i+3]] 
        weekday5 = weekday5 + user[cols[7*i+4]] 
        weekday6 = weekday6 + user[cols[7*i+5]] 
        weekday7 = weekday7 + user[cols[7*i+6]] 
    
    weekday1 = weekday1.to_frame(name = 'weekday1')
    weekday2 = weekday2.to_frame(name = 'weekday2')
    weekday3 = weekday3.to_frame(name = 'weekday3')
    weekday4 = weekday4.to_frame(name = 'weekday4')
    weekday5 = weekday5.to_frame(name = 'weekday5')
    weekday6 = weekday6.to_frame(name = 'weekday6')
    weekday7 = weekday7.to_frame(name = 'weekday7')  
    
    weekday_all = pd.merge(weekday1,weekday2,how='outer',left_index = True,right_index=True)
    weekday_all = pd.merge(weekday_all,weekday3,how='outer',left_index = True,right_index=True)
    weekday_all = pd.merge(weekday_all,weekday4,how='outer',left_index = True,right_index=True)
    weekday_all = pd.merge(weekday_all,weekday5,how='outer',left_index = True,right_index=True)
    weekday_all = pd.merge(weekday_all,weekday6,how='outer',left_index = True,right_index=True)
    weekday_all = pd.merge(weekday_all,weekday7,how='outer',left_index = True,right_index=True)

    
    feature_all2 = pd.merge(user,weekday_all,how='outer',left_index=True,right_index=True)
    feature_all2.set_index('enrollment_id').to_csv('data\\train\\feature_all_13.csv') 
    
    
def id_events_by_week():
    #按周统计每个enrollment_id的event次数,生成feature_all_14.csv

    ##提取log中的时间列，转化成时间格式，再合并回去
    user = read_user('data\\train\\log_train_num.csv')[['enrollment_id','time','event_num']]
    user_time = pd.to_datetime(user['time']).apply(lambda x : x.date())
    time_frame = user_time.to_frame(name = 'date')
    d4 = pd.merge(user,time_frame,how="outer",left_index=True,right_index=True)
    
    ##将时间列转化为星期格式
    d5 = d4.copy()
    d6 = d5.set_index('date')
    d6.index = pd.to_datetime(d6.index)
    d6['weekday'] = d6.index.weekday
    ##计数：计算每个enrollment_id在一周7天中每天的event总数
    d7 = d6[['enrollment_id','weekday','event_num']].groupby(['enrollment_id','weekday']).count()
    d7.reset_index(level=0,inplace =True)
    d7.reset_index(level=0,inplace =True)
    d8 = d7.set_index(['enrollment_id','weekday'])
    
    enroll = pd.read_csv('data\\train\\enrollment_train_num.csv')
    enroll = enroll[["enrollment_id","course_id_num"]]
    ##生成weekday_test.csv文件，该文件是每个enrollment_id对应7天，方便后续合成dataframe
    len_en = len(enroll)
    f = open('data\\train\\weekday_train.csv','a')
    f.write('weekday'+','+'enrollment_id'+'\n')
    for j in range(len_en):
        for i in range(7):
            f.write(str(i)+','+str(enroll.iat[j,0])+'\n')
        
    f.close()
    ##合成，统计中没有的天数对应的值为0
    week = read_user('data\\train\\weekday_train.csv').set_index(['enrollment_id','weekday'])
    week_all = pd.merge(week,d8,how="outer", left_index = True, right_index=True)
    week_all.fillna(0,inplace=True)
    week_all_1 = week_all.reset_index()
    ##写入weekday.csv
    fw = open('data\\train\\weekday.csv','a')
    fw.write('weekday00'+','+'weekday11'+','+'weekday22'+','+'weekday33'+','+'weekday44'+','+'weekday55'+','+'weekday66'+'\n')
    for i in range(len(week_all_1)):
        print i
        
        if ((i+1)%7==0):
            fw.write(str(int(week_all_1.iat[i,2]))+'\n')
        else:
            fw.write(str(int(week_all_1.iat[i,2]))+',')
        
        
    fw.close()
    ##最后加入特征矩阵
    feature_all = read_user('data\\train\\feature_all_13.csv')
    week_all_2 = read_user('data\\train\\weekday.csv')
    feature_all1 = pd.merge(feature_all,week_all_2,how='outer',left_index=True,right_index=True)
    feature_all1.set_index('enrollment_id').to_csv('data\\train\\feature_all_14.csv')
            
    
def user_events_by_week():
    #生成feature_all_15.csv
    user = read_user('data\\train\\feature_all_14_all.csv').set_index('enrollment_id')
    enroll = read_user('data\\enrollment\\enrollment_all_num.csv').set_index('enrollment_id')
    clos = ['weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66']
    
    user1 = user[clos]
    enroll1 = enroll[['username']]
    ue = pd.merge(enroll1,user1,how='outer',left_index=True,right_index=True)
    ue.fillna(0,inplace=True)
    
    ue_sum = ue.groupby(['username']).sum()
    enroll2 = enroll.copy().reset_index().set_index('username')[['enrollment_id']]
    uee = pd.merge(enroll2,ue_sum,how='outer',left_index=True,right_index=True)
    uee_1 = uee.set_index('enrollment_id')
    uee_1.columns = ['user_weekday00','user_weekday11','user_weekday22',
    'user_weekday33','user_weekday44','user_weekday55','user_weekday66']
    
    feature_all = read_user('data\\train\\feature_all_14.csv').set_index('enrollment_id')
    feature_all1 = pd.merge(feature_all,uee_1,how='inner',left_index=True,right_index=True)
    feature_all2 = feature_all1.sort_index()
    feature_all2.to_csv('data\\train\\feature_all_15.csv')
    

def gbdt_feature_100():
    #将gbdt提取的100维特征添加到原来特征中，生成feature_all_17.csv
    cols = ["g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10",
    "g11","g12","g13","g14","g15","g16","g17","g18","g19","g20","g21","g22","g23",
    "g24","g25","g26","g27","g28","g29","g30","g31","g32","g33","g34","g35","g36",
    "g37","g38","g39","g40","g41","g42","g43","g44","g45","g46","g47","g48","g49",
    "g50","g51","g52","g53","g54","g55","g56","g57","g58","g59","g60","g61","g62",
    "g63","g64","g65","g66","g67","g68","g69","g70","g71","g72","g73","g74","g75",
    "g76","g77","g78","g79","g80","g81","g82","g83","g84","g85","g86","g87","g88",
    "g89","g90","g91","g92","g93","g94","g95","g96","g97","g98","g99"]
    feature = pd.read_csv("data\\libfm\\train_final.csv",
                          names = cols)
                          
    feature_all = read_user('data\\train\\feature_all_15.csv')
    feature_all2 = pd.merge(feature_all,feature,how='outer',left_index=True,right_index=True)
    feature_all2.set_index('enrollment_id').to_csv('data\\train\\feature_all_17.csv') 

def gbdt_feature_200():
    #将gbdt提取的200维特征添加到原来特征中，生成feature_all_18_g200.csv
    cols_200 = [
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
    feature_200 = pd.read_csv("data\\libfm\\train_final2.csv",
                          names = cols_200)
    feature_all = read_user('data\\train\\feature_all_15.csv')
    feature_all2 = pd.merge(feature_all,feature_200,how='outer',left_index=True,right_index=True)
    feature_all2.set_index('enrollment_id').to_csv('data\\train\\feature_all_18_g200.csv') 
    
def gbdt_feature_30():
    #将gbdt提取的30维特征添加到原来特征中，生成feature_all_19_g30.csv
    cols_30 = [
    "g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14",
    "g15","g16","g17","g18","g19","g20","g21","g22","g23","g24","g25","g26","g27",
    "g28","g29"]
    feature_30 = pd.read_csv("data\\libfm\\train_final3.csv",
                          names = cols_30)
    feature_all = read_user('data\\train\\feature_all_15.csv')
    feature_all2 = pd.merge(feature_all,feature_30,how='outer',left_index=True,right_index=True)
    feature_all2.set_index('enrollment_id').to_csv('data\\train\\feature_all_19_g30.csv') 
    
if __name__ == '__main__':
    start_time = time.time()
    
    user = read_user('data\\train\\log_train_num.csv')
    #user = read_user('data\\test\\log_test_num.csv')
    
    day_events()#30features_train.csv
    courses_per_user()#courses_per_user_test.csv
    ensemble_features()#feature_all.csv
    all_events(user)#feature_all_1.csv
    source(user)#feature_all_2.csv
    last_event()#feature_all_3.csv
    blank_days()#feature_all_4.csv
    muti_features1()#feature_all_5.csv
    muti_features2()#feature_all_6.csv
    features_210()#feature_all_7.csv
    events_7()#feature_all_8.csv
    duration_days()#feature_all_9.csv
    courses_per_user_all()#feature_all_10.csv
    users_per_course_all()#feature_all_11.csv
    course_feature()#feature_all_12.csv
    events_by_week()#feature_all_13.csv
    id_events_by_week()#feature_all_14.csv
    user_events_by_week()#feature_all_15.csv
    gbdt_feature_100()#feature_all_17.csv
    gbdt_feature_200()#feature_all_18_g200.csv
    gbdt_feature_30()#feature_all_19_g30.csv
    print 'total time: ',time.time()-start_time 