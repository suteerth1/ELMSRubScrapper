import requests
import json
import re
import os
import pycurl

GRADES_TXT = "../data/ids.txt"
TOK_FILE = "../data/auth_tok.txt"
COOKIES_TXT = "../data/cookies.txt"
OUTPUT_FOLDER = "../data/grades"
COURSE_ID = open("../data/course_id.txt",'r').read().strip()

def get_student_ids(access_token_filename, course_number):
    tok = open(access_token_filename).read().strip()
    url = "https://myelms.umd.edu/api/v1/courses/" + course_number + "/enrollments"  # + str(course_number) +"/enrollments"
    regex_page_number = re.compile("[^_]page=(\d+)")
    req = requests.get(url, data={"access_token": tok, "per_page": 100})
    req_links = req.headers['Link']
    req_links_arr = req_links.split(",")
    try:
        number_of_pages = int(regex_page_number.findall(req_links_arr[3])[0])
    except IndexError:
        print("Cant find the numbe of pages because the last page was not found in headers")
    print(number_of_pages)
    # ids = json.loads(temp.text)
    ret = []
    for i in range(1, number_of_pages):
        req = requests.get(url, data={"access_token": tok, "per_page": 100, "page": i})
        student_arr = json.loads(req.text)
        for stud in student_arr:
            if stud["type"] == "StudentEnrollment":
                new_html_url = stud["html_url"]
                new_html_url = re.compile("/users/").sub("/grades/", stud["html_url"])

                ret.append(new_html_url)
    return ret


def get_student_pages(cookies_txt, ids, course_id):
    with open(ids, "r") as stud_ids:
        for line in stud_ids:
            print("[-] getting "+repr(line))
            stud_id = line.split('/')[-1].strip()
            os.system('wget  -O '+OUTPUT_FOLDER+'/'+stud_id+' --load-cookies '+cookies_txt+' "https://umd.instructure.com/courses/'+course_id+'/grades/'+stud_id+'"')
            print(line)

            print("[+] Written to " + stud_id)



if __name__ == "__main__":
    temp = get_student_ids(TOK_FILE, COURSE_ID)
    print(temp)
    with open(GRADES_TXT, "w") as putemhere:
        for i in temp:
            putemhere.write(i + "\n")

    print("getting student pages")
    get_student_pages(COOKIES_TXT, GRADES_TXT, COURSE_ID)
# print(temp.headers)
