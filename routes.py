from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import Application
from extensions import db
from forms import ApplicationForm

main = Blueprint("main", __name__)

# View all applications
@main.route("/")
def index():
    status_filter = request.args.get("status")
    if status_filter:
        applications = Application.query.filter_by(status=status_filter).all()
    else:
        applications = Application.query.all()
    return render_template("index.html", applications=applications)

# Add new application
@main.route("/add", methods=["GET", "POST"])
def add_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        app_obj = Application(
            name=form.name.data,
            email=form.email.data,
            job_title=form.job_title.data,
            status=form.status.data
        )
        db.session.add(app_obj)
        db.session.commit()
        flash("Application added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("application_form.html", form=form, title="Add Application")

# Edit application
@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    app_obj = Application.query.get_or_404(id)
    form = ApplicationForm(obj=app_obj)
    if form.validate_on_submit():
        form.populate_obj(app_obj)
        db.session.commit()
        flash("Application updated successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("application_form.html", form=form, title="Edit Application")

# Delete application
@main.route("/delete/<int:id>")
def delete_application(id):
    app_obj = Application.query.get_or_404(id)
    db.session.delete(app_obj)
    db.session.commit()
    flash("Application deleted!", "success")
    return redirect(url_for("main.index"))

# API endpoint for Postman testing (JSON)
@main.route("/api/applications", methods=["GET","POST"])
def api_applications():
    if request.method == "POST":
        data = request.get_json()
        app_obj = Application(
            name=data["name"],
            email=data["email"],
            job_title=data["job_title"],
            status=data.get("status","applied")
        )
        db.session.add(app_obj)
        db.session.commit()
        return jsonify({"message":"Application added","id":app_obj.id}), 201
    # GET all
    applications = Application.query.all()
    result = [{"id":a.id,"name":a.name,"email":a.email,"job_title":a.job_title,"status":a.status} for a in applications]
    return jsonify(result)
