from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from backend import *
from classes import *

bp = Blueprint('search', __name__)


@bp.route('/', methods=('GET', 'POST'))
def search():
    """
    Renders the search.html template if it is a GET request and the redirects to the get_results view if it is a POST
    """
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'A TV show name is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search.get_results', query=title))

    # add/update logged in user's show ids to its session
    shows_to_session()

    if ('user_id' in session) and (len(session['show_ids']) > 0):
        last_show_id = session['show_ids'][-1]
        try:
            shows, total_pages = get_shows_from_search(None, kind='recommendation', show_id=last_show_id)
        # We handle exceptions when the API is not working as we expect
        except APIError as error:
            print(error)
            return redirect(url_for('error'))
        except KeyError as error:
            print('ERROR The following field must have been removed from the API : ' + str(error))
            return redirect(url_for('error'))
        except TypeError as error:
            print('ERROR The following field must have been modified in the API : ' + str(error))
            return redirect(url_for('error'))
        session['last_show_name'] = ShowDetailedView(last_show_id).title
        return render_template('search/search.html', shows=shows)

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='trending_day')
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/search.html', shows=shows)


@bp.route('/results/<query>', defaults={'page': 1}, methods=('GET', 'POST'))
@bp.route('/results/<query>/<int:page>', methods=('GET', 'POST'))
def get_results(query, page):
    """
    Renders the results.html template if it is a GET request with the result of the search query and redirects to the
    get_results view if it is a POST
    """
    if request.method == 'POST':
        title = request.form['title']
        error = None

        if not title:
            error = 'A TV show name is required.'

        if error is not None:
            flash(error)
        else:
            return redirect(url_for('search.get_results', query=title))

    # add/update logged in user's show ids to its session
    shows_to_session()

    if query is None:
        query = 'house'

    try:
        shows, total_pages = get_shows_from_search(query, page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        raise APIError(error)
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/results.html', shows=shows, current_page=page, total_pages=total_pages, query=query)


@bp.route('/trending', defaults={'page': 1})
@bp.route('/trending/<int:page>', methods=('GET',))
def get_trending(page):
    """
    Renders the week's trends page
    """

    # add/update logged in user's show ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='trending_week', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))


    return render_template('search/trending.html', shows=shows, current_page=page, total_pages=total_pages)


@bp.route('/popular', defaults={'page': 1})
@bp.route('/popular/<int:page>', methods=('GET',))
def get_popular(page):
    """
    Renders the popular tv shows page
    """

    # add/update logged in user's show ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='popular', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/popular.html', shows=shows, current_page=page, total_pages=total_pages)


@bp.route('/top_rated', defaults={'page': 1})
@bp.route('/top_rated/<int:page>', methods=('GET',))
def get_top_rated(page):
    """
    Renders the top rated tv shows page
    """

    # add/update logged in user's show ids to its session
    shows_to_session()

    # Get the list of today's trending shows with an API call
    try:
        shows, total_pages = get_shows_from_search(None, kind='top_rated', page=page)
    # We handle exceptions when the API is not working as we expect
    except APIError as error:
        print(error)
        return redirect(url_for('error'))
    except KeyError as error:
        print('ERROR The following field must have been removed from the API : ' + str(error))
        return redirect(url_for('error'))
    except TypeError as error:
        print('ERROR The following field must have been modified in the API : ' + str(error))
        return redirect(url_for('error'))

    return render_template('search/top_rated.html', shows=shows, current_page=page, total_pages=total_pages)
