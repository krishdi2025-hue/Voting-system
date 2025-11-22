# myvoting - Minimal Django voting example

What's included:
- Django project `myvoting`
- App `polls` with Candidate and Vote models
- Templates + static files (includes candidate image at `static/images/candidate5.png`)

Setup (run locally):
1. Create virtualenv and install requirements:
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt

2. Run migrations and create superuser:
   python manage.py migrate
   python manage.py createsuperuser

3. Populate a candidate:
   python manage.py shell
   >>> from polls.models import Candidate
   >>> Candidate.objects.create(name='डॉ. पिपाडा राजेंद्र मदनलाल', number=5, photo='/static/images/candidate5.png', symbol='ट्रैक्टर')

4. Run server:
   python manage.py runserver

5. Open http://127.0.0.1:8000/ to see the voting page.
