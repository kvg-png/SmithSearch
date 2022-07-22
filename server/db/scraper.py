from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

smith_URL = 'https://www.smith.edu/academics/academic-program/curriculum/course-search'

conn = sqlite3.connect('./courses.db')
c = conn.cursor()
#c.execute('''DROP TABLE courses''')
#c.execute('''CREATE TABLE courses(title TEXT, time TEXT, weekdays TEXT, courseNum INT, subject TEXT)''')

def get_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def get_courses(driver):
    driver.get(smith_URL)

    #find iframe
    iframe = driver.find_element(By.ID, 'myframe')

    #switch to iframe
    print("Switched to iframe...")
    driver.switch_to.frame(iframe)

    #find articles in iframe
    print('Fetching the courses...')
    courses = driver.find_elements(By.TAG_NAME, 'article')

    course_subjects = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-course-subject'))
        )

    course_titles = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-section-title'))
        )

    course_times = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-meeting'))
        )

    course_nums = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'course-course-num'))
        )        
            
    for course_index in range(0, 753):
        course_subject = course_subjects[course_index].text
        course_title = course_titles[course_index].text
        
        #raw course time/section numbers
        course_time_raw = course_times[course_index].get_attribute("innerHTML")
        course_num_raw = course_nums[course_index].text
        
        #cleaned course time/section numbers
        course_time = course_time_raw[32::]

        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        course_days = []
        for day in weekdays:
            if day in course_time_raw:
                course_days.append(day)

        course_days = ', '.join(map(str, course_days))

        course_num = int(''.join(filter(str.isdigit, course_num_raw)))    

        #print(course_days)
        c.execute('''INSERT INTO courses VALUES(?,?,?,?,?)''',  (course_title, course_time, course_days, course_num, course_subject))
        print(course_index)
    
    #conn.commit()
    print("complete")
    conn.commit()
    # c.execute('''SELECT * FROM courses''')
    # results = c.fetchall()
    # print(results)

    return courses

if __name__ == "__main__":
    print('Creating Driver...')
    driver = get_driver()

    #loads courses
    courses = get_courses(driver)

    print("Found: ", len(courses))

