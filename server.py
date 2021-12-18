from datetime import datetime

import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


competitions = load_competitions()
clubs = load_clubs()


def flash_message_mail_unknown():
    flash_message = "Sorry, but this email is unknown"
    return flash_message


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config)

    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def show_summary():
        # club = [club for club in clubs if club['email'] == request.form['email']][0]
        # return render_template('welcome.html', club=club, competitions=competitions)
        club = []
        for c in clubs:
            if c['email'] == request.form['email']:
                club.append(c)
        if len(club) != 0:
            return render_template('welcome.html', club=club[0], competitions=competitions)
        else:
            message = flash_message_mail_unknown()
            flash(message)
            # return redirect(url_for('index'))
            return render_template('index.html'), 404

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = [c for c in clubs if c['name'] == club][0]
        found_competition = [c for c in competitions if c['name'] == competition][0]
        today = str(datetime.now())
        if found_club and found_competition and found_competition["date"] > today:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash('Sorry, this event is already passed. Impossible to book it.')
            # reconstitution du dico cu club à partir de son nom
            return render_template('welcome.html', club=found_club, competitions=competitions), 403

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        today = str(datetime.now())
        if competition["date"] < today:
            flash('Sorry, this event is already passed. Impossible to book it')
            return render_template('welcome.html', club=club, competitions=competitions), 403
        else:
            if places_required > 12:
                flash("Sorry, it's not possible to book more than 12 places.")
                return render_template('booking.html', club=club, competition=competition), 403
            elif int(club['points']) < places_required:
                flash(f"Sorry, you have only {club['points']} points.")
                return render_template('booking.html', club=club, competition=competition), 403
            else:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                club['points'] = int(club['points']) - places_required
                flash('Great-booking succeded!')
                return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
