
from bs4 import BeautifulSoup
import requests
import re

base_url = 'https://www.naukri.com/'  # the url of the website

"""for each data we are passing it as individual bsobj from the findall list and hence each data is a bsobj"""


def get_org_name(data):
    dummy = data.find_all('span', {'class': 'orgRating'})
    org_name = dummy[0].text
    return org_name


def get_exp(data):
    dummy = data.find_all('span', {'class': 'exp'})
    exp = 100
    if re.match('\d+', dummy[0].text):
        dummy = re.findall('\d+',(dummy[0].text))
        for i in dummy:
            if re.match('\d+',i):
                if int(i) < exp:
                    exp = int(i)
        return exp
    else:
        return 0


def get_loc(data):
    dummy = data.find_all('span', {'class', 'loc'})
    if len(dummy) > 0:
        loc = dummy[0].text
        return loc
    else:
        return None

# here there might be a problem of return skills of list


def get_skills(data):
    dummy = data.find_all('span', {'class', 'skill'})
    if len(dummy) > 0:
        skill = re.split('\s+ | ,+',dummy[0].text)
        print (skill)
        return skill
    else:
        return None


# here there might be a problem of return skills of list


def get_job_desc(data):
    dummy = data.find_all('span', {'class': 'desc'})
    if len(dummy) > 0:
        desc = dummy[0].text
        return desc
    else:
        return None
    """here salary if not specified is retuned as none"""

def convert_to_int(string_data):
    try:
        data = string_data.split(',')
        string_data = ''
        for i in data:
            string_data += i
        return int(string_data)
    except :
        return 0


def get_salary(data):
    salary_list=[]
    salary = data.find_all('span', {'class': 'salary'})
    try:
        if len(salary) > 0:
            salary = re.split('\s+ | (P\.A\.)+ | -+ | \w+',salary[0].text)
            for i in salary:
                if i is not None:
                    if re.match('\d+',i):
                        salary_list.append(convert_to_int(i))
            if len(salary_list)>0:
                return max(salary_list)
        else:
            return 0
    except:
        return 0

def get_info_from_each_tuple(data):
    dummy_dict = dict()
    dummy_dict['salary'] = get_salary(data)
    dummy_dict['company'] = get_org_name(data)
    dummy_dict['loc'] = get_loc(data)
    dummy_dict['skills'] = get_skills(data)
    dummy_dict['description'] = get_job_desc(data)
    dummy_dict['exp'] = get_exp(data)
    return dummy_dict


"""here pass the bsobj as an argument"""


def get_jobs_count(bsobj):
    dummy_regex = re.compile('\\d+')
    data = bsobj.find_all('span', {'class': 'cnt'})
    count_first = data[0].text
    count = count_first.split(" ")
    index = 0
    if re.search(dummy_regex, count_first) is not None:
        for i in count:
            if i == 'of':
                break
            else:
                index += 1
        count = int(count[index + 1])
        return count
    else:
        return 0


""" here main function starts for searching the jobs """

"""here there may be error"""

"""
def prepare_parameters(data, cnt):  # this prepares parameters for the given options
    data = data.split('\\w+')
    dummy_str = "-"
    for i in range(len(data)):
        data[i] = data[i].lower()
    dummy_str = dummy_str.join(data)
    dummy_str += '-jobs'
    cnt = str(cnt)
    if int(cnt) > 0: dummy_str += '-%s' % (cnt)
    print (dummy_str)
    delay()
    return dummy_str"""


# to get pages pass the url  here there is exception needed
def make_obj(paramet, cnt):
    flg=0
    if int(cnt)==0:
        flg=1
    if flg!=1:
        new_url =base_url+str(paramet)+'-jobs'+'-'+str(cnt)
    else:
        new_url =base_url+str(paramet)+'-jobs'   
    url = requests.get(new_url)
    delay()
    bsobj = BeautifulSoup(url.text)
    return bsobj

def make_count(count):
    if count/50 > 1:
        return count//50
    if count!=0 and count/50 < 1:
        return (count+50)//50
    else:
        return 0
"""here pass the job specification of the containing individual jobs """

def delay():
    pass

def run_scraper(paramet):
    total_list_fetched=[]
    bsobj = make_obj(paramet, 0)
    check = bsobj.find_all('div', {'type': 'tuple'})
    a = 0
    if len(check) == 0:
    	pass
    else:
        count = get_jobs_count(bsobj)
        for i in range(int(make_count(count))):
            bsobj = make_obj(paramet, int(i))
            bsobj_len = bsobj.find_all('div', {'type': 'tuple'})
            for j in range(len(bsobj_len)):
                #print (j,bsobj_len[j])
                try:
                    total_list_fetched.append(get_info_from_each_tuple(bsobj_len[j]))
                    print("done", " ",a)
                    print (total_list_fetched[a])
                    a+=1
                    print (len(total_list_fetched))
                    if a > int(3000):
                        return total_list_fetched
                except:
                    j+=1
                    continue
        try:
            avg_l=[0,0,0,0,0,0] 
            sal_l=sorted(total_list_fetched,key=itemgetter('salary'),reverse=True)
            exp_l=sorted(total_list_fetched,key=itemgetter('exp'))
            if len(sal_l) > 0:
                for i in range(len[sal_l]):
                    if (sal_l[i])['salary'] > 0:
                        avg_l[0]+=(sal_l[i])['salary']
                        avg_l[3]+=1
            if len(exp_l) > 0:
                for i in range(len[exp_l]):
                    if (sal_l[i])['exp'] is not None:
                        avg_l[1]+=(sal_l[i])['exp']
                        avg_l[4]+=1
            avg_l[0]=avg_l[0]//avg_l[3]
            avg_l[1]=avg_l[1]//avg_l[4]
            avg_l[2]=len(total_list_fetched)
            avg_l=avg_l[:4]
            print ('job computed')
            return total_list_fetched , avg_l
        except:
            pass
    return total_list_fetched
