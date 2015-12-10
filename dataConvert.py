# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:30:04 2015
将enrollment_train.csv log_train.csv  enrollment_test.csv log_test.csv 各行的元素
量化（转化为数字），并写入文件夹train：enrollment_train_num.csv log_train_num.csv
test:enrollment_test_num.csv log_test_num.csv 
@author: litaisong
"""

import pandas as pd
import time
import sys


def read_user(filename):
    #return pd.read_csv(filename, index_col=[5],parse_dates=["time"])
    return pd.read_csv(filename)
    
#user_id,item_id,behavior_type,user_geohash,item_category,
# names=["user_id", "item_id", "behavior_type", "user_geohash", "item_category","time"], 
def read_test(filename):
    return pd.read_csv(filename, index_col=[0],
                   parse_dates=["time"])
                      
def confirm_data(user):    
    #print user.head()
    
    print '========================timemin'
    print user.index.min()
    print '========================timemax'
    print user.index.max()
    print '========================usershape'
    print user.shape[0]
    print '========================user_id'
    print user["user_id"].unique().size
    print '========================item_id'
    print user["item_id"].unique().size
    print '========================behavior_type'
    print user["behavior_type"].unique().size
    print '========================geohash'
    print user["user_geohash"].unique().size
    print '========================category'
    print user["item_category"].unique().size
    
def log_Convert(user,log_path):
     #将39门课转化为[0,38]的整数
    arr_course = [
    'DPnLzkJJqOOPRJfBxIHbQEERiYHu5ila','7GRhBDsirIGkRZBtSMEzNTyDr2JQm4xx',
    'AXUJZGmZ0xaYSWazu8RQ1G5c76ECT1Kd','5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2',
    'TAYxxh39I2LZnftBpL0LfF2NxzrCKpkx','KHPw0gmg1Ad3V07TqRpyBzA8mRjj7mkt',
    'fbPkOYLVPtPgIt0MxizjfFJov3JbHyAi','81UZtt1JJwBFYMj5u38WNKCSVA4IJSDv',
    '5Gyp41oLVo7Gg7vF4vpmggWP5MU70QO6','Er0RFawC4sHagDmmQZcBGBrzamLQcblZ',
    'mTmmr5zd8l4wXhwiULwjSmSbi9ktcFmV','SpATywNh6bZuzm8s1ceuBUnMUAeoAHHw',
    'shM3Yy9vxHn2aqjSYfQXOcwGo0hWh3MI','xMd9DzNyUCTLRPVbwWVzf4vq06oqrTT1',
    'HbeAZjZFFQUe90oTP0RRO0PEtRAqU3kK','H2lDW05SyKnwntZ6Fora76aPAEswcMa5',
    'NmbZ3BmS8V4pMg6oxXHWpqqMZCE1jvYt','a2E7NQC7nZB7WHEhKGhKnKvUWtsLAQzh',
    '9Bd26pfDLvkPINwLnpaGcf0LrLUvY1Mz','3cnZpv6ReApmCaZyaQwi2izDZxVRdC01',
    'ykoe1cCWK134BJmfbNoPEenJOIWdtQOZ','V4tXq15GxHo2gaMpaJLZ3IGEkP949IbE',
    'bWdj2GDclj5ofokWjzoa5jAwMkxCykd6','X78EhlW2JxwO1I6S3U4yZVwkEQpKXLOj',
    'A3fsA9Zfv1X2fVEQhTw51lKENdNrEqT3','G8EPVSXsOYB5YQWZGiz1aVq5Pgr2GrQu',
    'gvEwgd64UX4t3K7ftZwXiMkFuxFUAqQE','9Mq1P5hrrLw6Bh9X4W4ZjisQJDdxjz9x',
    'RXDvfPUBYFlVdlueBFbLW0mhhAyGEqpt','WM572q68zD5VW8pcvVTc1RhhFUq3iRFN',
    'I7Go4XwWgpjRJM8EZGEnBpkfSmBNOlsO','1pvLqtotBsKv7QSOsLicJDQMHx3lui6d',
    'Wm3dddHSynJ76EJV6hyLYKGGRL0JF3YK','nSfGxfEtzw5G72fVbfaowxsV46Pg1xIc',
    'tXbz2ZYaRyb2ZsWUBPoYzAmisOhHQrYl','q6A6QG7qMpyNcznyT2XaIxnfNGkZRxXl',
    'DABrJ6O4AotFwuAbfo1fuMj40VmMpPGX','3VkHkmOtom3jM2wCu94xgzzu1d6Dn7or',
    '9zpXzW9zCfU8KGBWkhlsGH8B8czISH4J']
    
    course =user["course_id"]
    for i in range(0,39):
        print arr_course[i]
        course = course.str.replace(arr_course[i], str(i)).astype('object')
        print "============================================"
        print course        
    print course
    course1 = course.to_frame(name="course_id_num")
    user_course_id = pd.merge(user, course1, how="outer",
                              left_index=True, right_index=True)
    
    #将source下的两项转化为0,1。server:0  ; browser:1
    arr_source = ["server","browser"]
    source = user["source"]
    for i in range(0,2):
        source = source.str.replace(arr_source[i], str(i)).astype('object')    
    source1 = source.to_frame(name="source_num")
    user_source = pd.merge(user_course_id, source1, how="outer",
                           left_index=True, right_index=True)
    
    #将event下的7项转化为整数[0,6]
    '''
    0. problem - Working on course assignments.
    1. video - Watching course videos.
    2. access - Accessing other course objects except videos and assignments.
    3. wiki - Accessing the course wiki.
    4. discussion - Accessing the course forum.
    5. nagivate - Navigating to other part of the course.
    6. page_close – Closing the web page.    
    '''
    arr_event = ["problem","video","access","wiki","discussion","nagivate","page_close"]
    event = user["event"]
    
    for i in range(0,7):
        event = event.str.replace(arr_event[i], str(i)).astype('object')    
    event1 = event.to_frame(name="event_num")
    user_event = pd.merge(user_source, event1, how="outer",
                          left_index=True, right_index=True)
                          
    #最后摘取部分数据写入csv文件
    user_num = user_event[["enrollment_id","username","course_id_num",
                           "time","source_num","event_num","object"]]
    user_num = user_num.set_index("enrollment_id") 
    user_num.to_csv(log_path)                      
    
def enrollment_Convert(user_en,enrollment_path):
    #将39门课转化为[0,38]的整数
    arr_course = [
    'DPnLzkJJqOOPRJfBxIHbQEERiYHu5ila','7GRhBDsirIGkRZBtSMEzNTyDr2JQm4xx',
    'AXUJZGmZ0xaYSWazu8RQ1G5c76ECT1Kd','5X6FeZozNMgE2VRi3MJYjkkFK8SETtu2',
    'TAYxxh39I2LZnftBpL0LfF2NxzrCKpkx','KHPw0gmg1Ad3V07TqRpyBzA8mRjj7mkt',
    'fbPkOYLVPtPgIt0MxizjfFJov3JbHyAi','81UZtt1JJwBFYMj5u38WNKCSVA4IJSDv',
    '5Gyp41oLVo7Gg7vF4vpmggWP5MU70QO6','Er0RFawC4sHagDmmQZcBGBrzamLQcblZ',
    'mTmmr5zd8l4wXhwiULwjSmSbi9ktcFmV','SpATywNh6bZuzm8s1ceuBUnMUAeoAHHw',
    'shM3Yy9vxHn2aqjSYfQXOcwGo0hWh3MI','xMd9DzNyUCTLRPVbwWVzf4vq06oqrTT1',
    'HbeAZjZFFQUe90oTP0RRO0PEtRAqU3kK','H2lDW05SyKnwntZ6Fora76aPAEswcMa5',
    'NmbZ3BmS8V4pMg6oxXHWpqqMZCE1jvYt','a2E7NQC7nZB7WHEhKGhKnKvUWtsLAQzh',
    '9Bd26pfDLvkPINwLnpaGcf0LrLUvY1Mz','3cnZpv6ReApmCaZyaQwi2izDZxVRdC01',
    'ykoe1cCWK134BJmfbNoPEenJOIWdtQOZ','V4tXq15GxHo2gaMpaJLZ3IGEkP949IbE',
    'bWdj2GDclj5ofokWjzoa5jAwMkxCykd6','X78EhlW2JxwO1I6S3U4yZVwkEQpKXLOj',
    'A3fsA9Zfv1X2fVEQhTw51lKENdNrEqT3','G8EPVSXsOYB5YQWZGiz1aVq5Pgr2GrQu',
    'gvEwgd64UX4t3K7ftZwXiMkFuxFUAqQE','9Mq1P5hrrLw6Bh9X4W4ZjisQJDdxjz9x',
    'RXDvfPUBYFlVdlueBFbLW0mhhAyGEqpt','WM572q68zD5VW8pcvVTc1RhhFUq3iRFN',
    'I7Go4XwWgpjRJM8EZGEnBpkfSmBNOlsO','1pvLqtotBsKv7QSOsLicJDQMHx3lui6d',
    'Wm3dddHSynJ76EJV6hyLYKGGRL0JF3YK','nSfGxfEtzw5G72fVbfaowxsV46Pg1xIc',
    'tXbz2ZYaRyb2ZsWUBPoYzAmisOhHQrYl','q6A6QG7qMpyNcznyT2XaIxnfNGkZRxXl',
    'DABrJ6O4AotFwuAbfo1fuMj40VmMpPGX','3VkHkmOtom3jM2wCu94xgzzu1d6Dn7or',
    '9zpXzW9zCfU8KGBWkhlsGH8B8czISH4J']
    
    course =user_en["course_id"]
    for i in range(0,39):
        print arr_course[i]
        course = course.str.replace(arr_course[i], str(i)).astype('object')
        print "============================================"
        print course        
    print course
    course1 = course.to_frame(name="course_id_num")
    user_course_id = pd.merge(user_en, course1, how="outer",
                              left_index=True, right_index=True)
    
    user_course_id.set_index("enrollment_id").to_csv(enrollment_path)    

def object_Convert():
    #未执行。。。
    user_ob = read_user('data\\object\\object_num.csv')
    array_ob = ['about', 'chapter', 'course', '2_info', 'html', 'outlink',
       'problem', 'sequential', 'static_tab', 'vertical', 'video',
       'combinedopenended', 'peergrading', 'discussion', 'dictation']
    category = user_ob['category']
    for i in range(15):
        category = category.str.replace(array_ob[i], str(i)).astype('object')
        print category 
    category1 = category.to_frame(name="category_num")
    user_ob_category = pd.merge(user_ob, category1, how="outer",
                              left_index=True, right_index=True)
    user_ob_category[['course_id_num','module_id','category_num','start',
    'children']].set_index('course_id_num').to_csv('data\\object\\object_num2.csv')                    

def data_for_libFM():
    #Transfer the feature_all_15.csv data to libFM type, as an input
    user_train = read_user('data\\train\\feature_all_15.csv')
    cols1 = [
    "210","day0","day1","day2","day3","day4","day5","day6","day7","day8","day9",
    "day10","day11","day12","day13","day14","day15","day16","day17","day18","day19",
    "day20","day21","day22","day23","day24","day25","day26","day27","day28","day29",
    "event0","event1","event2","event3","event4","event5","event6","all_events",
    "users_per_course_all","courses_per_user_all","source_num","day_times","blank_days",
        
    'user_weekday00','user_weekday11','user_weekday22','user_weekday33','user_weekday44','user_weekday55','user_weekday66',
    'weekday00','weekday11','weekday22','weekday33','weekday44','weekday55','weekday66',
    
    "category0","category1","category2","category3","category4","category5","category6","category7",
    "category8","category9","category10","category11","category12","category13","category14","category_all"
    ]
    user_train_part = user_train[cols1]
    f = open('data\\libfm\\train1.txt','w')
    
    colen = len(cols1)
    for i in range(len(user_train_part)):
        f.write(str(user_train_part.iat[i,0])+' ')
        for j in range(1,colen):
            if(user_train_part.iat[i,j]>0):
                f.write(str(j)+':'+str(user_train_part.iat[i,j])+' ')
        f.write('\n')
    f.close()
    
    
    cols2 = [
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
    
    user_test = read_user('data\\test\\feature_all_15.csv')
    user_test_part = user_test[cols2]
    f = open('data\\libfm\\test1.txt','w')
    for i in range(len(user_test_part)):
        f.write(str(0)+' ')
        for j in range(0,colen-1):
            if(user_test_part.iat[i,j]>0):
                f.write(str(j)+':'+str(user_test_part.iat[i,j])+' ')
        f.write('\n')
    f.close()
            
            
            
    
   
if __name__ == '__main__':
    start_time = time.time()
    train_log_file = 'data\\train\\log_train.csv'
    train_enrollment_file = 'data\\train\\enrollment_train.csv'
    
    test_log_file = 'data\\test\\log_test.csv'
    test_enrollment_file = 'data\\test\\enrollment_test.csv'
    
    train_log_path = "data\\train\\log_train_num.csv"
    train_enrollment_path = "data\\train\\enrollment_train_num.csv"
    
    test_log_path = "data\\test\\log_test_num.csv"
    test_enrollment_path = "data\\test\\enrollment_test_num.csv"
    
    train_user=read_user(train_log_file)
    train_user_en = read_user(train_enrollment_file)    
    
    test_user=read_user(test_log_file)
    test_user_en = read_user(test_enrollment_file)
    
    log_Convert(train_user,train_log_path)
    enrollment_Convert(train_user_en,train_enrollment_path)
    
    log_Convert(test_user,test_log_path)
    enrollment_Convert(test_user_en,test_enrollment_path)
    
    #data_for_libFM()    
    
    print 'total time: ',time.time()-start_time                 