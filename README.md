# socialweb
Flask web 2.0 project setup requirements

Steps 

-> install python Python 3.9.9

-> Open project socialweb inside ide 

-> pip install -r requirements.txt

-> Install latest mysql database  
        
        --- version I used(mysql  Ver 8.0.27 for macos11.6 on arm64 (Homebrew))
        version 8.0.27 for your respective OS should work

-> Open msql cli
        
        1) setup my sql password 
        2) create database socialweb
        3) use database socialweb
        4) Update password and database name inside "constants.py"
        5) run the script databasesetup.txt either copy pasting all the commands into the cli or run it as a script 

-> run "python WebApp.py" or click on run within the IDE

-> to generate profile vectors for your users using user_profile_vector_script.py 
    generated profile vector files will be created inside folder "UserInfo" 
