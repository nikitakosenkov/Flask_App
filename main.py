from flask import Flask, request, make_response, redirect
from flask import render_template
from data import db_session
from data.jobs import Jobs
from flask_login import LoginManager, login_user, logout_user
from data.users import User
from forms.jobs import JobsForm, JobsFormChange, JobsFormDelete
from forms.register import RegisterForm
from forms.login import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

user_id = 0


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global user_id
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user_id = user.id
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['POST', 'GET'])
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        job = Jobs(
            team_leader=form.team_leader_id.data,
            job=form.job_title.data,
            is_finished=form.is_job_finished.data,
            collaborators=form.collaborators.data,
            work_size=form.work_size.data
        )

        db_sess.add(job)
        db_sess.commit()
        return redirect('/')

    return render_template('jobs.html', title='Adding a Job', form=form)


@app.route('/change_job', methods=['POST', 'GET'])
def change_job():
    global user_id
    form = JobsFormChange()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        job = Jobs(
            id=form.id.data,
            team_leader=form.team_leader_id.data,
            job=form.job_title.data,
            is_finished=form.is_job_finished.data,
            collaborators=form.collaborators.data,
            work_size=form.work_size.data
        )
        j = db_sess.query(Jobs).filter(Jobs.id == job.id).first()
        if user_id == 1 or user_id == int(j.team_leader):
            db_sess.query(Jobs).filter(Jobs.id == job.id).update({'team_leader': job.team_leader,
                                                                  'job': job.job,
                                                                  'work_size': job.work_size,
                                                                  'collaborators': job.collaborators,
                                                                  'is_finished': job.is_finished})
        db_sess.commit()
        return redirect('/')

    return render_template('change.html', title='Changing a Job', form=form)


@app.route('/delete_job', methods=['POST', 'GET'])
def delete_job():
    form = JobsFormDelete()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        job = Jobs(
            id=form.id.data
        )
        j = db_sess.query(Jobs).filter(Jobs.id == job.id).first()
        if user_id == 1 or user_id == int(j.team_leader):
            db_sess.query(Jobs).filter(Jobs.id == job.id).delete()
        db_sess.commit()
        return redirect('/')

    return render_template('job_delete.html', title='Deleting a Job', form=form)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
