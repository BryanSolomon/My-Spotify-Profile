# My-Spotify-Profile
 A web app that provides a visualization for personal Spotify data. View your top artists and tracks over different time periods, as well as your top genres, recently played, and playlists. This application provides an easy way for Spotify user's to see their stats and activity data at any time of the year.

### Technologies Used
- Python
- pip
- Virtual environment
- Django
- Rest APIs
- Spotify Web API
- Spotipy wrapper library
- JQuery

## Setup
1. Clone repository into your local machine
2. Open the `.env-template` file in the  `/Spotify` folder and follow the instructions
3. Open terminal and make sure you are in the project's repository. Create a virtual environment using python and activate it.<br>
#### On Windows:
```
python -m venv virtEnv .
.\Scripts\activate.bat
```
#### On Unix or MacOS:
```
python3 -m venv virtEnv .
bin/activate
```
4. Install the dependencies:
```
(virtEnv)$ pip install -r requirements.txt
``` 
(Note the `(virtEnv)` in front of the prompt. This indicates that this terminal session operates in a virtual environment)<br>

5. Once pip has finished downloading the dependencies, run the django server:
```
(virtEnv)$ python manage.py runserver
```
6. Navigate to http://127.0.0.1:8000 in your web browser and enjoy the web application.