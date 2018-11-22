from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

import requests, werkzeug
from myfavshows.db import get_db
from myfavshows.classes import *

# Parameters that are used several times in the code below
api_path = 'https://api.themoviedb.org/3/'
params = {'api_key': '7ecd6a3ceec1b96921b4647095047e8e'}


def get_shows_from_search(query, kind='search_query', show_id=None, page=1):
    """
    This function handles the different API calls and returns the results.
    The different API calls have to be specified in the 'kind' parameter, possibilities are : 'search_query' (default),
    'trending_day','trending_week','popular','top_rated','recommendation'
    All the results are stored in Show objects (cf classes.py).
    """
    params['page'] = page

    if kind == 'search_query':
        params['query'] = query
        req = requests.get(api_path + 'search/tv', params)
    elif kind == 'trending_day':
        # Get the list of today's trending shows with an API call
        req = requests.get(api_path + 'trending/tv/day', params)
    elif kind == 'trending_week':
        # Get the list of today's trending shows with an API call
        req = requests.get(api_path + 'trending/tv/week', params)
    elif kind == 'popular':
        req = requests.get(api_path + 'tv/popular', params)
    elif kind == 'top_rated':
        req = requests.get(api_path + 'tv/top_rated', params)
    elif kind == 'recommendation' and show_id is not None:
        req = requests.get(api_path + 'tv/' + str(show_id) + '/recommendations', params)
    else:
        print('Please enter a correct request type.')

    # Check the response status code and raise a custom exception if not 200
    if not req.ok:
        raise APIError(req.status_code)

    req_json = req.json()

    results = []
    if req_json["total_results"] == 0:
        flash("No results were found for your search.")

    for res in req_json["results"]:
        results += [Show(res)]

    return results, req_json["total_pages"]


def shows_to_session():
    """
    Fetches the user's favourite shows' ids and stores it in the 'session' object, aborts if no user logged in
    """
    if 'user_id' not in session:
        return None

    shows = []
    show_ids = get_db().execute(
        'SELECT show_id'
        ' FROM shows_users '
        ' WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

    for show in show_ids:
        shows += [show['show_id']]

    session['show_ids'] = shows
    return None


def make_multi_requests(show_ids):
    """
    Takes the ids to request and creates one thread by id to query the API
    :param show_ids: list of the shows' ids
    :return: list of shows objects corresponding
    """

    # lets make the new shows appear first
    temp = []
    for i in range(len(show_ids)):
        temp.append(show_ids[-(i+1)])
    show_ids = temp

    # lets launch all the API call threads
    APIrequest.initiate()
    APIrequest.show_ids = show_ids
    threads = []
    for i in show_ids:
        threads.append(APIrequest())

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    results = [0] * len(show_ids)

    # we reorder the results
    for show_id in APIrequest.shows.keys():
        results[show_ids.index(show_id)] = APIrequest.shows[show_id]

    return results


