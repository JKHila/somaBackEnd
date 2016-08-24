
# coding: utf-8

# 

# In[1]:

from sklearn.externals import joblib
from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Twitter
from konlpy.utils import pprint
twitter = Twitter()
hannanum = Hannanum()
kkma = Kkma()
komoran = Komoran()


# In[2]:

import sys
default_stdout = sys.stdout
default_stderr = sys.stderr
reload(sys)
sys.stdout = default_stdout
sys.stderr = default_stderr
sys.setdefaultencoding('utf-8')


# In[3]:


clf = joblib.load('classify.model')
cate_dict = joblib.load('cate_dict.dat')
vectorizer = joblib.load('vectorizer.dat')


# In[4]:

joblib.dump(clf,'n_classify.model')


# In[5]:

joblib.dump(cate_dict,'n_cate_dict.dat')
joblib.dump(vectorizer,'n_vectorizer.dat')


# In[6]:

cate_id_name_dict = dict(map(lambda (k,v):(v,k),cate_dict.items()))


# In[7]:

removeList = [u"정품",u"해외",u"할인",u"%",u"쿠폰"]


# In[8]:

pred = clf.predict(vectorizer.transform(['[신한카드5%할인][서우한복] 아동한복 여자아동 금나래 (분홍)']))[0]
print cate_id_name_dict[pred]


# In[9]:

import re
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')


# In[ ]:

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])


# In[ ]:

from bottle import route, run, template,request,get, post


import  time
from threading import  Condition
_CONDITION = Condition()
@route('/classify')
def classify():
    #print "classify called"
    tmplist =[]
    img = request.GET.get('img','')
    name = request.GET.get('name', '')
    tmp_name = name
    for key in removeList:
        if tmp_name.find(key):
            tmp_name =  tmp_name.replace(key,"")
    analysis = twitter.morphs(name)
    for key in analysis:
        if len(key)==1:
                analysis.remove(key)     
        """if result:
            if len(key)==3:
                analysis.remove(key)
        else:
            if len(key)==1:
                analysis.remove(key)"""  
    ngramList = find_ngrams(tmp_name,3)
    str2=""
    for each in ngramList:
        str2 += ''.join(each)
        str2 +=' '
    str1 = ' '.join(analysis)    
    name += ' '+str1+' '+str2
    pred = clf.predict(vectorizer.transform([name]))[0]
    return {'cate':cate_id_name_dict[pred]}


run(host='0.0.0.0', port=8887)


# # * 추후 여기 docker 에서 뭔가 python package 설치할게 있으면 
#  * /opt/conda/bin/pip2 install bottle 이런식으로 설치 가능

# In[ ]:




# In[ ]:



