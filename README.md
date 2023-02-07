#Python Django - Blog

##Description
    - Blog developed with Django
    - uses MySQL database
    
##Run Project:
  - create venv inside project dir
    python -m venv venv
  - activate venv
    Win:
        .\venv\Scripts\activate
    Linux:
        source venv/bin/activate
        deactivate (to deactivate)
  - LINUX - install sql libraries
    sudo apt-get install default-libmysqlclient-dev	
  - install requirements
    pip install -r requirements.txt
  - initiate server
    python manage.py runserver
	or
    python manage.py runserver 0.0.0.0:3000
