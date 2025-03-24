import requests
from bs4 import BeautifulSoup
import time

AUTH_URL = 'https://mydy.dypatil.edu/rait/login/index.php'
SUBJECTS_URL = 'https://mydy.dypatil.edu/rait/blocks/academic_status/ajax.php?action=myclasses'
ATTENDANCE_URL = 'https://mydy.dypatil.edu/rait/blocks/academic_status/ajax.php?action=attendance' 
TIMETABLE_URL = 'https://mydy.dypatil.edu/rait/blocks/academic_status/ajax.php?action=timetable' 


email = input("Enter college email: ")
password = input("Enter college password: ")

# email = "vik.cha.rt22@dypatil.edu"
delay = 0.1

auth_result : requests.Response = requests.post(
    AUTH_URL,
    data={
        'username':email,
        'password':password
    },
    allow_redirects=False # must set this to avoid the damn cookies being lost because of a redirect
)

# print(auth_result.headers)
print(auth_result.cookies)






def get_subjects() -> list[dict]:

    
    def parse_subjects(html: str) -> list[dict]:
        """
            Creates a BeautifulSoup object that finds each subject block,
            returns an array of JSON Objects containing Name, Instructor, Attendance & Link
            to that particular subject
            
            Parameters:
                html (str): string object containing the response content (html, inline-css & inline-js code)
                
            Returns:
                subjects (list[dict]): List of dictionary object containing the subject details:
                    \t- Name
                    \t- Instructor
                    \t- Attendance
                    \t- Link
                    \t- Course ID
        """
        
        soup = BeautifulSoup(html, 'lxml')
        subjects = []
        
        subject_containers = soup.find_all(class_="subcontent-container")
        # print(len(subject_containers))

        for subject in subject_containers:
            #convert to raw string, so it can be parsed after being converted to BS4
            subject = str(subject)
            soup = BeautifulSoup(subject, 'lxml')

            #Name
            
            subject_name = soup.find('h4')
            subject_name = subject_name.contents[0] # getting the data within the actual tag that stored the name

            #Instructor
            subject_instructor = soup.select_one('.istruinfocontainer > div') # probably meant to write "instructor-info-container" but you never know 💀
            subject_instructor = subject_instructor.contents[0]

            #Subject Attendance
            subject_attendance = soup.select_one('.prg-container > span') #progress container is the weird horizontal graph thingy
            subject_attendance = subject_attendance.contents[0] if subject_attendance != None else "0%"
            
            #Subject links
            subject_link = soup.find('a')
            subject_link = subject_link['href']
            
            #Course id
            course_id = subject_link[-4:]

            subject_dict = {
                'name':subject_name,
                'instructor':subject_instructor,
                'attendance':subject_attendance,
                'link':subject_link,
                'course_id':course_id
            }
            
            subjects.append(subject_dict)
            
        return subjects
    
    # with requests.session() as session:

    #Insert the session cookies
    # session.cookies = requests.utils.cookiejar_from_dict(cookie_dict=cookies)
    response = requests.get(SUBJECTS_URL, cookies=auth_result.cookies)

    html_content = response.content
    #pass the html_content to a custom parsing block, that converts it into a neat json object 
    subjects = parse_subjects(html=html_content)
    # print(subjects)

    return subjects

subjects = get_subjects()

def get_subject_materials(link : str) -> list[dict]:
   

    def parse_materials(html : str) -> list[dict]:
        
        soup = BeautifulSoup(html, 'lxml')
        
        activities = soup.select(".activityinstance")

        # SELECTING all anchor tags, seems to give me access to past semester and all their contents, might be useful
        # Something to look into for the future.
        
        course_materials = []
        for activity in activities:
            soup = BeautifulSoup(str(activity), 'lxml')
            link = soup.select_one("a")
            link = link['href']
            # print(link)
            
            name = soup.find("span")
            name = name.contents[0]
            link_type = link[34:-19] # 34 and -19 are just constants to remove the unecessary part of the link
            
            obj = soup.select(".accesshide")
            doc_type = "unknown"
            if(len(obj)):
                doc_type = obj[0].contents[0]
            # else:
                # print(obj)
            # The handling for the different potential scenarios regarding the way the download links have to be made available is 
            # to be seperated from this request.
            activity_object = {
                'name':name,
                'link':link,
                'type':link_type,
                'doctype':doc_type
            }
            
            course_materials.append(activity_object)
            

        return course_materials




    
    response = requests.get(link, cookies=auth_result.cookies)
    #get the string version of the response to pass to the parser
    response = response.content
    
    materials_json = parse_materials(response)
    
    
    return materials_json





# for each subject iterate over each item and open it (but fast!)


material_links = []
print("Proceeding at opening at 10 req/sec")
for subject in subjects:
    subject_url = subject.get('link')
    links = get_subject_materials(subject_url)
    
    for link in links:
        url = link.get("link")
        print(f"opening: {url}")
        requests.get(url, cookies=auth_result.cookies)
        # break
        
        time.sleep(delay)

    print(f"{subject.get('name')} completed. {len(links)} in total.")
        

    
    






