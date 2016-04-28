import requests
import re
from bs4 import BeautifulSoup
from sender import Sender
import time

class Course_enrollment:
    """ 
    There are two situations that you may need this little helper.
    First, you just want to play with python.
    Second, you really need to get enrolled in the class you want.
    Let's consider you are in the second situation.  
    So now your wanted course is already full, otherwise, you wouldn't want to use this.
    Esesstially, you need to feed in the course id and the v variable to get you enrolled.
    """
    def __init__(self, username = yourusername, password = yourpassword):
        # initialize the enrollment helper by logging into the system
        # And reach to the selectCourse page.
        self.s = requests.session()

        url = 'https://login.sufe.edu.cn/cas/login?service=http%3A%2F%2Feams.sufe.edu.cn%2Feams%2Fsso%2Flogin%3FSsoClientServiceURI%3DaHR0cDovL2VhbXMuc3VmZS5lZHUuY24vZWFtcy9ob21lLmFjdGlvbg%3D%3D'
        soup = BeautifulSoup(self.s.get(url).content, "html.parser")
        lt = soup.find(r'input', attrs={'name':'lt'})['value']

        data = {'username': username,
                'password': password,
                'imageCodeName':'',
                'errors': '0',
                'lt': lt,
                '_eventId': 'submit'}
        
        headers = {
                   'Referer':'https://login.sufe.edu.cn/cas/login?service=http%3A%2F%2Feams.sufe.edu.cn%2Feams%2Fsso%2Flogin%3FSsoClientServiceURI%3DaHR0cDovL2VhbXMuc3VmZS5lZHUuY24vZWFtcy9ob21lLmFjdGlvbg%3D%3D',
                   'RA-Ver':'3.0.7'}

        self.s.post(url, data = data, headers = headers)
        #进入选课界面
        self.s.get('http://eams.sufe.edu.cn/eams/stdElectCourse.action?_=1461743685644')
        self.s.get('http://eams.sufe.edu.cn/eams/stdElectCourse!defaultPage.action?electionProfile.id=2084')
    
    def update_names(self):
        # update the course name that can be 
        res = self.s.get("http://eams.sufe.edu.cn/eams/stdElectCourse!data.action?profileId=2084").content.decode('utf-8')
        courseName = re.findall(re.compile(r'(name:\')(.*?)\','), res[18:])
        self.courseNames = {content[1] for content in courseName}
        return self.courseNames
    
    def enroll(self, id, v): 
        # here is the problem
        # The program cannot discover id and v itself.
        # Or I didn't come up with a way to find them in the .js files in the sufe enrollment page.
        # Lukily we can find id and v manually, which is a stupid way.
        
        key_url = "http://eams.sufe.edu.cn/eams/stdElectCourse!batchOperator.action?profileId=2084&electLessonIds=" + str(id) +"&withdrawLessonIds=&v=" + str(v)
        msg = self.s.get(key_url).content
        return re.findall(re.compile('(\t{4})(.*?)(</br>)'), msg)[0][1]

    def check(self, name):
        if name in self.courseNames:
            return True
        else:
            return False
    
    # missing part:
    # For getting enrolled in a course, there are two strategies:
    # One, waiting the course to be released and be the first one to get enrolled, which is what I've already realized.
    # Two, cannot get enrolled right now, so wait until there are more room in this course and be the first one to get enrolled.
    # The second strategy is not realized yet.
    # But I think it's pretty simple and can be done in a few codes.
    
    # First, get the id of a course, which can be something you feed in the program
    # Second, use crawler to get the limit students number(ln) and current students number(cn) of the course.
    # Third, if ln > cn, enroll in it.
    # Fourth, if not, return to second step.

if __name__ == "__main__":
    ryan_helper = Course_enrollment()
    wanted_course = ['深度学习中的优化算法', '大数据金融', '量化定价策略'] # the course you may want to select
    ryan_helper.update_names()

    sender = Sender(youremailaddress, youremailpwd)
    
    #####################################################################
    ## Just to print all the classes in the beginning for you to check.##
    #####################################################################
    print('##############')
    print('当前开放课程: ')
    for course in ryan_helper.courseNames:
        print(course)
    print('##############')
    ### End checking  ###
    
    detect = False
    while not detect:
        try:
            last = ryan_helper.courseNames
            time.sleep(4) # check every four seconds
            ryan_helper.update_names()
            cur = ryan_helper.courseNames

            if last != cur:
                sender.createMsg(body = "课程已更新，\n %s" %(str(cur)) , subject = '选课提醒')
                sender.sendmail()
            for course in wanted_course:
                res = ryan_helper.check(course)
                if res:
                    print("%s : 开放" %(course))
                    # send you an email if the course you wanted is open for selection.
                    sender.createMsg(body = "%s 已开放" %(course), subject = '选课提醒')
                    sender.sendmail()
                    detect = True
                else:
                    print("%s : 未开放" %(course))
        except Exception as e:
            ryan_helper = Course_enrollment() 
            ryan_helper.update_names()

        
