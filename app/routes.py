from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.forms import MatchForm, SignUpForm, LogInForm, SearchForm
from app.models import User, Matches

@app.route("/")
def index():
    myUser = User.query.all()
    return render_template('index.html', myUser=myUser)

@app.route("/signup", methods= ["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User(email=email, username=username, password=password)

        login_user(new_user)

        print(email, username, password)
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):

            login_user(user)
            return redirect(url_for('index'))

        else:
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account/user_id", methods= ["GET"])
@login_required
def account():
    email = User.email
    username = User.username

    account = User.query.filter_by(username=username, email=email)

    return render_template('account.html', account=account)

@app.route("/account/user_id", methods= ["GET"])
@login_required
def profile():
    email = User.email
    username = User.username

    profile = User.query.filter_by(username=username, email=email)

    return render_template('profile.html', profile=profile)

@app.route("/match", methods= ["GET", "POST"])
@login_required
def match():
    form = MatchForm()
    if form.validate_on_submit():
        maps = form.maps.data
        modes = form.modes.data

        new_match = Matches(maps=maps, modes=modes, user_id=current_user.id)

        print(new_match)
        return redirect(url_for('eights'))

    return render_template('match.html', form=form)

@app.route("/teammates/<user_id>", methods= ["GET", "POST"])
@login_required
def teammates(user_id):
    user = User.query.get(user_id)
    return render_template('teammates.html', user=user)

@app.route("/search_teammates", methods= ["GET", "POST"])
@login_required
def search_teammates():
    form = SearchForm()
    if form.validate_on_submit():

        username = form.username.data
        search_user = User.query.filter(User.username == username).first()

        if search_user is not None:
            return redirect(url_for('teammates', user_id=search_user.id))
        else:
            return redirect(url_for('search_teammates', form=form))

    return render_template('search_teammates.html', form=form)


@app.route("/eights", methods= ["GET", "POST"])
@login_required
def eights():
    matches = Matches.query.order_by(Matches.date_created.desc()).all()
    print(matches)

    return render_template('eights.html', matches=matches)


@app.route('/edit_match/<match_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_match(match_id):
    match = Matches.query.get(match_id)
    if not match:
        return redirect(url_for('index'))
    if match.user_id != current_user.id:
        return redirect(url_for('index'))
    form = MatchForm()
    if form.validate_on_submit():
        new_maps = form.maps.data
        new_modes = form.modes.data

        match.update(maps=new_maps, modes=new_modes)

        return redirect(url_for('eights', match_id=match.id))
    return render_template('edit_match.html', match=match, form=form)

@app.route('/delete_match/<match_id>/delete')
@login_required
def delete_match(match_id):
    match = Matches.query.get(match_id)
    if not match:
        return redirect(url_for('eights'))
    if match.user_id != current_user.id:
        return redirect(url_for('eights'))
    match.delete()
    return redirect(url_for('eights'))