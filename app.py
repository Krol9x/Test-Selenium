from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, DateField, FileField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime, date
from config import Config
import pytz


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

def poland_now():
    tz = pytz.timezone("Europe/Warsaw")
    return datetime.now(tz)

# ---------- Models ----------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False, default="Your Full Name")
    headline = db.Column(db.String(200), nullable=False, default="My growing tech stack and projects")
    about = db.Column(db.Text, nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(120), nullable=True)

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text, nullable=True)


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(150), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    provider = db.Column(db.String(150), nullable=True)
    date_completed = db.Column(db.Date, nullable=True)
    credential_url = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)  # np. Początkujący, Średniozaawansowany, Zaawansowany


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(255), nullable=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=poland_now)
    
# ---------- Forms ----------
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Log in")


class ProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired()])
    headline = StringField("Headline", validators=[DataRequired()])
    about = TextAreaField("About Me")
    photo = FileField("Your Photo (png/jpg/webp/gif)")
    email = StringField("Email")
    phone = StringField("Phone Number")
    location = StringField("Location")
    submit = SubmitField("Save")


class ExperienceForm(FlaskForm):
    role = StringField("Job Title", validators=[DataRequired()])
    company = StringField("Company", validators=[DataRequired()])
    start_date = DateField("Start Date", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("End Date", format="%Y-%m-%d")
    is_current = BooleanField("I currently work here")
    description = TextAreaField("Description")
    submit = SubmitField("Save")


class EducationForm(FlaskForm):
    school = StringField("School/University", validators=[DataRequired()])
    degree = StringField("Field of Study/Degree")
    start_date = DateField("Start date", validators=[DataRequired()], format="%Y-%m-%d")
    end_date = DateField("End date", format="%Y-%m-%d")
    description = TextAreaField("About")
    submit = SubmitField("Save")


class CourseForm(FlaskForm):
    title = StringField("Course", validators=[DataRequired()])
    provider = StringField("Provider")
    date_completed = DateField("End date", format="%Y-%m-%d")
    credential_url = StringField("Link")
    notes = TextAreaField("Note")
    submit = SubmitField("Save")
    
class LanguageForm(FlaskForm):
    name = StringField("Language", validators=[DataRequired()])
    level = StringField("Level", validators=[DataRequired()])
    submit = SubmitField("Save")


class SkillForm(FlaskForm):
    name = StringField("Skill", validators=[DataRequired()])
    submit = SubmitField("Save")
    
from flask_wtf.file import FileField, FileAllowed
class PortfolioForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("About project")
    file = FileField("File", validators=[FileAllowed(['zip','pdf','png','jpg','jpeg','gif'])])
    submit = SubmitField("Save")

class LinkForm(FlaskForm):
    name = StringField("Link name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    submit = SubmitField("Save")
    
class MessageForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    content = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- Helpers ----------
def allowed_file(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in app.config["ALLOWED_EXTENSIONS"]


def init_db_with_admin():
    db.create_all()
    # Seed admin user if not exists
    if not User.query.filter_by(email="hubert.krol0000@gmail.com").first():
        u = User(email="hubert.krol0000@gmail.com")
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()

    # Ensure one profile exists
    if not Profile.query.first():
        p = Profile(about="About me.")
        db.session.add(p)
        db.session.commit()


# ---------- Public routes ----------
@app.route("/", methods=["GET", "POST"])
def index():
    profile = Profile.query.first()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    education = Education.query.order_by(Education.start_date.desc()).all()
    courses = Course.query.order_by(Course.date_completed.desc().nullslast()).all()
    skills = Skill.query.order_by(Skill.name.asc()).all()
    languages = Language.query.order_by(Language.name.asc()).all()
    portfolio = Portfolio.query.order_by(Portfolio.title.asc()).all()
    links = Link.query.order_by(Link.name.asc()).all()
    form = MessageForm()
    
    if form.validate_on_submit():
      msg = Message(
          name=form.name.data,
          email=form.email.data,
          content=form.content.data
      )
      db.session.add(msg)
      db.session.commit()
      flash("Send!", "success")
      return redirect(url_for("index"))
    
    return render_template("index.html",
                           profile=profile,
                           experiences=experiences,
                           education=education,
                           courses=courses,
                           skills=skills,
                           languages=languages,
                           portfolio=portfolio,
                           links=links,
                           form=form)


# ---------- Auth routes ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Zalogowano.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("wrong data.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("log out.", "info")
    return redirect(url_for("index"))


# ---------- Admin routes ----------
@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/profile", methods=["GET", "POST"])
@login_required
def admin_profile():
    profile = Profile.query.first()
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        profile.full_name = form.full_name.data
        profile.headline = form.headline.data
        profile.about = form.about.data
        profile.email = form.email.data
        profile.phone = form.phone.data
        profile.location = form.location.data

        # obsługa zdjęcia
        file = request.files.get("photo")
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(save_path)
                profile.photo_filename = filename
            else:
                flash("wrong file format.", "danger")
        
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_profile"))

    return render_template("admin/profile.html", form=form, profile=profile)


# Experience CRUD
@app.route("/admin/experience", methods=["GET", "POST"])
@login_required
def admin_experience():
    form = ExperienceForm()
    if form.validate_on_submit():
        exp = Experience(
            role=form.role.data,
            company=form.company.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data if not form.is_current.data else None,
            is_current=form.is_current.data,
            description=form.description.data,
        )
        db.session.add(exp)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_experience"))
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template("admin/experience.html", form=form, experiences=experiences)


@app.route("/admin/experience/delete/<int:exp_id>", methods=["POST"])
@login_required
def delete_experience(exp_id):
    exp = Experience.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_experience"))


# Education CRUD
@app.route("/admin/education", methods=["GET", "POST"])
@login_required
def admin_education():
    form = EducationForm()
    if form.validate_on_submit():
        edu = Education(
            school=form.school.data,
            degree=form.degree.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
        )
        db.session.add(edu)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_education"))
    records = Education.query.order_by(Education.start_date.desc()).all()
    return render_template("admin/education.html", form=form, records=records)


@app.route("/admin/education/delete/<int:edu_id>", methods=["POST"])
@login_required
def delete_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    db.session.delete(edu)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_education"))


# Courses CRUD
@app.route("/admin/courses", methods=["GET", "POST"])
@login_required
def admin_courses():
    form = CourseForm()
    if form.validate_on_submit():
        c = Course(
            title=form.title.data,
            provider=form.provider.data,
            date_completed=form.date_completed.data,
            credential_url=form.credential_url.data,
            notes=form.notes.data,
        )
        db.session.add(c)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_courses"))
    courses = Course.query.order_by(Course.date_completed.desc().nullslast()).all()
    return render_template("admin/courses.html", form=form, courses=courses)


@app.route("/admin/courses/delete/<int:course_id>", methods=["POST"])
@login_required
def delete_course(course_id):
    c = Course.query.get_or_404(course_id)
    db.session.delete(c)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_courses"))


# Skills CRUD
@app.route("/admin/skills", methods=["GET", "POST"])
@login_required
def admin_skills():
    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data
        )
        db.session.add(skill)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_skills"))
    
    skills = Skill.query.order_by(Skill.name.asc()).all()
    return render_template("admin/skills.html", form=form, skills=skills)


@app.route("/admin/skills/delete/<int:skill_id>", methods=["POST"])
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_skills"))

# Languages CRUD
@app.route("/admin/languages", methods=["GET", "POST"])
@login_required
def admin_languages():
    form = LanguageForm()
    if form.validate_on_submit():
        lang = Language(
            name=form.name.data,
            level=form.level.data
        )
        db.session.add(lang)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_languages"))
    
    languages = Language.query.order_by(Language.name.asc()).all()
    return render_template("admin/languages.html", form=form, languages=languages)


@app.route("/admin/languages/delete/<int:lang_id>", methods=["POST"])
@login_required
def delete_language(lang_id):
    lang = Language.query.get_or_404(lang_id)
    db.session.delete(lang)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_languages"))

import os
from werkzeug.utils import secure_filename

@app.route("/admin/portfolio", methods=["GET", "POST"])
@login_required
def admin_portfolio():
    form = PortfolioForm()
    if form.validate_on_submit():
        filename = None
        file = request.files.get("file")
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(app.config["UPLOAD_FOLDER"], "portfolio")
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))

        project = Portfolio(
            title=form.title.data,
            description=form.description.data,
            filename=filename
        )
        db.session.add(project)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_portfolio"))

    projects = Portfolio.query.order_by(Portfolio.title.asc()).all()
    return render_template("admin/portfolio.html", form=form, projects=projects)

@app.route("/admin/portfolio/delete/<int:project_id>", methods=["POST"])
@login_required
def delete_portfolio(project_id):
    project = Portfolio.query.get_or_404(project_id)
    # usuń też plik z dysku
    if project.filename:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], "portfolio", project.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(project)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_portfolio"))
# Serve uploaded files (optional direct link)
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/admin/links", methods=["GET", "POST"])
@login_required
def admin_links():
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(name=form.name.data, url=form.url.data)
        db.session.add(link)
        db.session.commit()
        flash("changes done.", "success")
        return redirect(url_for("admin_links"))

    links = Link.query.order_by(Link.name.asc()).all()
    return render_template("admin/links.html", form=form, links=links)

@app.route("/admin/links/delete/<int:link_id>", methods=["POST"])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("delete.", "info")
    return redirect(url_for("admin_links"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            name=form.name.data,
            email=form.email.data,
            content=form.content.data
        )
        db.session.add(msg)
        db.session.commit()
        flash("message send", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

@app.route("/admin/messages", methods=["GET", "POST"])
@login_required
def admin_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages)

@app.route("/admin/messages/delete/<int:id>", methods=["POST"])
@login_required
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash("delete.", "success")
    return redirect(url_for("admin_messages"))

@app.context_processor
def inject_year():
    return {"current_year": date.today().year}

# CLI helper to init DB on first run

if __name__ == "__main__":
    with app.app_context():
        init_db_with_admin()
    app.run(debug=True)
