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
        if found_club and found_competition:
            return render_template('booking.html', club=found_club, competition=found_competition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
