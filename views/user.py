from flask import request, url_for, render_template, redirect, Flask, session
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy

from forms.user import SignUpForm, DeleteForm, UpdateForm
from models.users import User


class UserList(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(UserList, self).__init__()
        self.engine = engine

    def get(self):
        users: list[User] = self.engine.session.execute(User.query).scalars()
        return render_template("user/list.html", users=users)


class UserView(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(UserView, self).__init__()
        self.engine = engine

    def get(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: list[User] = self.engine.session.execute(query).scalar()
        if not user:
            return 'wtf'
        return render_template('user/read.html', user=user)


class UserSignUp(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(UserSignUp, self).__init__()
        self.engine = engine

    def get(self):
        form = SignUpForm()
        return render_template('user/signup.html', form=form)

    def post(self):
        form = SignUpForm(request.form)
        print(form.name.data, form.email.data, form.age.data)
        if form.validate():
            print('valid')
            user = User(name=form.name.data, email=form.email.data, age=form.age.data)
            self.engine.session.add(user)
            self.engine.session.commit()
            print('add user', form.name.data, form.email.data, form.age.data)
        else:
            print(form.errors)

        return redirect(url_for('user.list'))


class UserUpdate(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(UserUpdate, self).__init__()
        self.engine = engine

    def get(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()

        if not user:
            return 'wtf'

        form = UpdateForm(
            name=user.name, email=user.email, age=user.age
        )

        return render_template('user/update.html', form=form)

    def post(self, user_id: str):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()

        if not user:
            return 'wtf'

        form = UpdateForm(request.form)
        if form.validate():
            user.name = form.name.data
            user.email = form.email.data
            user.age = form.age.data
            self.engine.session.commit()

        return redirect(url_for('user.view', user_id=user.id))


class UserLogin(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(UserLogin, self).__init__()
        self.engine = engine

    def get(self):
        form = SignUpForm()
        return render_template('user/login.html', form=form)

    def post(self):
        form = SignUpForm(request.form)

        if form.validate():
            query = User.query.where(User.username == form.name.data and User.email == form.email.data
                                     and User.age == form.age.data)
            user: User = self.engine.session.execute(query).scalar()
            if not user:
                return 'wtf'
            session['user_id'] = user.id

            self.engine.session.commit()

        return redirect(url_for('user.list'))


class DeleteUser(MethodView):
    init_every_request = False

    def __init__(self, engine: SQLAlchemy):
        super(DeleteUser, self).__init__()
        self.engine = engine

    def get(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'wtf'
        form = DeleteForm()
        return render_template('user/delete.html', user=user, form=form)

    def post(self, user_id: int):
        query = User.query.where(User.id == user_id)
        user: User = self.engine.session.execute(query).scalar()
        if not user:
            return 'wtf'
        form = DeleteForm(request.form)
        if form.validate():
            self.engine.session.delete(user)
            self.engine.session.commit()
        return redirect(url_for('user.list'))


# class ListItems(MethodView):
#     init_every_request = False
#
#     def get(self):
#         render_template('api/main.html')


def add_user(app: Flask, engine: SQLAlchemy):
    common_func = UserList.as_view('user.list', engine=engine)
    app.add_url_rule('/', view_func=common_func)
    app.add_url_rule('/user/list', view_func=common_func)

    app.add_url_rule('/user/<user_id>', view_func=UserView.as_view('user.view', engine=engine))
    app.add_url_rule('/signup', view_func=UserSignUp.as_view('user.signup', engine=engine))
    app.add_url_rule('/user/<user_id>/update', view_func=UserUpdate.as_view('user.update', engine=engine))
    app.add_url_rule('/login', view_func=UserLogin.as_view('user.login', engine=engine))
    app.add_url_rule('/user/<user_id>/delete', view_func=DeleteUser.as_view('user.delete', engine=engine))
    # app.add_url_rule('/api', view_func=ListItems.as_view('api.list'))
