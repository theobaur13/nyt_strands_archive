from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, DateForm, ThemeLetterGridForm
from app.models import User, Strand, Letters, Words, WordLetters
from werkzeug.security import check_password_hash
from datetime import timedelta, datetime

@app.route("/")
def index():
    return render_template("home.html", title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("loader"))
    
    form = LoginForm()
    if form.validate_on_submit():
        form_username = form.username.data
        form_password = form.password.data
    
        user = User.query.filter_by(username=form_username).first()
        if user:
            if check_password_hash(user.hashed_password, form_password):
                login_user(user)
                flash(f"Logged in {form_username}!", "success")
                return redirect(url_for("loader"))
        flash(f"Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f"Logged out", "success")
    return redirect(url_for("index"))

@app.route("/loader", methods=["GET", "POST"])
@login_required
def loader():
    form = DateForm()
    if form.validate_on_submit():
        date = form.date.data
        return redirect(url_for("load_date", date=date))
    return render_template("loader.html", title="Admin Loader", form=form)

@app.route("/loader/<date>", methods=["GET", "POST"])
@login_required
def load_date(date):
    theme_letter_grid_form = ThemeLetterGridForm.create_grid_form()

    # Covert date into datetime object
    year, month, day = date.split("-")
    datetime_date = datetime(year=int(year), month=int(month), day=int(day))

    # Load any existing strand
    existing_strand = Strand.query.filter_by(date=datetime_date).first()

    # If existing strand prefill the form
    if existing_strand:
        theme_letter_grid_form.theme.data = existing_strand.theme
        letters = existing_strand.letters
        for letter in letters:
            getattr(theme_letter_grid_form, f"letter_{letter.index}").data = letter.letter

    # If form is submitted
    if theme_letter_grid_form.validate_on_submit():
        theme = theme_letter_grid_form.theme.data

        # Create or update the strand
        form_theme = request.form.get("theme")
        if existing_strand:
            existing_strand.theme = form_theme
        else:
            # Add strand to the database
            new_strand = Strand(date=datetime_date, theme=form_theme)
            db.session.add(new_strand)
            db.session.commit()
            existing_strand = Strand.query.filter_by(date=datetime_date).first()

        # Create or update the letters
        for i in range(1, 49):
            letter = request.form.get(f"letter_{i}")

            if existing_strand:
                existing_letter = Letters.query.filter_by(index=i, strand_id=existing_strand.id).first()
                if existing_letter:
                    existing_letter.letter = letter.capitalize()

                else:
                    new_letter = Letters(index=i, letter=letter.capitalize(), strand_id=existing_strand.id)
                    db.session.add(new_letter)

        db.session.commit()
        flash(f"Successfully loaded date {date}", "success")
        return redirect(url_for("load_words", date=date))
    return render_template("load_date.html", title="Load Strand", date=date, existing_strand=existing_strand, theme_letter_grid_form=theme_letter_grid_form)

@app.route("/loader/words/<date>")
@login_required
def load_words(date):
    # Covert date into datetime object
    year, month, day = date.split("-")
    datetime_date = datetime(year=int(year), month=int(month), day=int(day))

    # Get the strand and letters
    strand = Strand.query.filter_by(date=datetime_date).first()
    strand_dict = strand.to_dict()

    if strand:
        letters = Letters.query.filter_by(strand_id=strand.id).all()
        letters_dict = [letter.to_dict() for letter in letters]
    else:
        return redirect(url_for("load_date", date=date))
    
    return render_template("load_words.html", title="Load Words", date=date, strand=strand_dict, letters=letters_dict)

@app.route("/data_loader", methods=["GET", "POST"])
@login_required
def data_loader():
    data = request.get_json()
    strand_id = int(data["strand_id"])
    words = data["words"]

    # Delete existing words and wordletters
    Words.query.filter_by(strand_id=strand_id).delete()
    word_ids = [word.id for word in Words.query.filter_by(strand_id=strand_id).all()]

    if word_ids:
        WordLetters.query.filter(WordLetters.word_id.in_(word_ids)).delete(synchronize_session='fetch')

    # Add words to the database
    for word in words:
        word_string = word["word"]
        wordletters = word["wordletters"]
        spanagram = False

        new_word = Words(word=word_string, spanagram=spanagram, strand_id=strand_id)
        db.session.add(new_word)
        db.session.commit()

        # Get the word_id
        word_id = Words.query.filter_by(word=word_string, strand_id=strand_id).first().id

        # Add wordletters to the database
        for wordletter in wordletters:
            index = int(wordletter["index"])
            letter_id = int(wordletter["letter_id"])

            new_wordletter = WordLetters(index=index, word_id=word_id, letter_id=letter_id)
            db.session.add(new_wordletter)

        db.session.commit()

    flash(f"Successfully loaded words for strand {strand_id}", "success")
    return "Success"