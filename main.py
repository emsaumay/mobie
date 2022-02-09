import random
from flask import Flask, render_template, request
import requests as r


app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)


def movies(name):

  results = r.get(f"https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={name}&page=1&include_adult=false").json()["results"][0]

  id = results["id"]

  imdb_id = r.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={key}&language=en-US").json()["imdb_id"]

  vid = r.get(f"https://vidclouds.us/json.php?imdb={imdb_id}").json()

  title = vid["title"]
  year = vid["year"]
  link = vid["link"]
  poster_url = vid["poster"]
  
  return title, year, link, poster_url

def tvshows(name, s, ep):

  results = r.get(f"https://api.themoviedb.org/3/search/tv?api_key={key}&language=en-US&query={name}&page=1&include_adult=false").json()["results"][0]

  tvid = results["id"]

  imdb_id = r.get(f"https://api.themoviedb.org/3/tv/{tvid}/external_ids?api_key={key}&language=en-US").json()["imdb_id"]

  vid = r.get(f"https://vidclouds.us/json.php?imdb={imdb_id}&season={s}&episode={ep}").json()

  title = vid["title"]
  year = vid["year"]
  link = vid["link"]
  poster_url = vid["poster"]
  
  return title, year, link, poster_url


@app.route('/movie')
def movie():
  movie_name = request.args.get('name')
  title, year, link, poster_url = movies(movie_name)
  return render_template(
    'movie.html',
    video_url=link,
    title = f"{title} | {year}",
    poster = poster_url
  )

@app.route('/tv-show')
def tvshow():
  name = request.args.get('name')
  season = request.args.get('season', default=1)
  episode = request.args.get('episode', default=1)
  title, year, link, poster_url = tvshows(name, season, episode)
  return render_template(
    'tv.html',
    video_url=link,
    title = f"{season}x{episode} | {title} | {year}",
    poster = poster_url
  )


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)
