# Shop project
### Shop project is an e-commerce website based on Python and Django.

# How to run
For run this project on your system as development mode, you can use steps below:
  1. Install `python3` and `pip` on your system.
  2. Clone the project from `https://github.com/jaladati/shop_project`.
  3. Create a virtual-environment using python and activate it.
  4. Install the requirements of project.
  5. Rename the `settings.py.sample` file to `settings.py` 
  6. Create the database tables.
  7. Create a super user.
     
     The following commands are for above tasks:

     For mac/linux:
     ```bash
     git clone https://github.com/jaladati/shop_project # step 2
     cd shop_project # Enter the project.
     python3 -m venv venv && source venv/bin/activate # step 3
     pip install -r requirements.txt # step 4
     mv shop_project/settings.py.sample shop_project/settings.py # step 5
     python manage.py makemigrations && python manage.py migrate # step 6
     python manage.py createsuperuser2 # step 7
     ```
     For windows:
     ```bash
     git clone https://github.com/jaladati/shop_project # step 2
     cd shop_project # Enter the project.
     python -m venv venv && venv/Scripts/activate # step 3
     pip install -r requirements.txt # step 4
     move shop_project/settings.py.sample shop_project/settings.py # step 5
     python manage.py makemigrations && python manage.py migrate # step 6
     python manage.py createsuperuser2 # step 7
     ```
  8. Run project using `python manage.py runserver`
  9. Open project on <u>http://localhost:8000</u>

# TODO
  - [ ] site settings app for more accessibilities on site.
