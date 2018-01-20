# ELMSRubScrapper
It is a simple script to extract relevant rubric information from canvas.
 
Requirements:

Fill out:
    
    data/auth_tok.txt   : The authorization token generated from canvas settings
    data/cookies.txt    : This has the cookie that can access the grades page.
    data/coutse_id.txt  : This has the course id. The course id can be found when opening up the course elms page  
                                        https://<elms>/courses/<course_id>
                                        
                                        
                                        
To get the result execute:
    
    1)
    python grade_page_getter.py
    This gets all the grade pages and puts them in data/grades
    
    2)
    python html_parser.py
    This extracts the relaven information out of the grade pages and puts it in scores.json
    