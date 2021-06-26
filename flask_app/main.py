# Import necessary modules
from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *
from sqlalchemy import or_, and_, func
from flask import Blueprint
from flask_login import login_required, current_user
import random

# This file includes all main routes (no login related routes)
main = Blueprint('main', __name__)

# Define global variables
orgs_search_results_data = Organizations.query.filter(
    Organizations.name.contains(""))
projects_search_results_data = Projects.query.filter(
    Projects.description.contains(""))
search_term = None
projectsPerPage = 25
orgsPerPage = 25

# Route for home page
@app.route('/')
@app.route('/index')
def index():

    # Return the static homepage
    return render_template('index.html', title='Open Source Platform')

# Route for projects page, includes searching and favoriting projects
@app.route('/projects', methods=['GET', 'POST'])
def projects():

    # Pull in the necessary global variables
    global projects_search_results_data
    global search_term
    global projectsPerPage

    # Get the page number from request arguments
    page = request.args.get('page', 1, type=int)

    # Logic for processing project searches
    if request.method == 'POST' and 'search_term' in request.form:

        # Pull in search term from search form
        search_term=request.form['search_term']
        
        # Basic search logic: Look in project parameters for search term
        projects_search_results_data = Projects.query.filter(
        or_(Projects.description.contains(search_term),
                Projects.name.contains(search_term),
                Projects.language.contains(search_term),
                Projects.owner.contains(search_term),
                Projects.source.contains(search_term)))

        # Pull in the item per page count, if necessary
        if 'per_page' in request.form:
            projectsPerPage = int(request.form['per_page'])

        # Logic for sorting items by name
        if 'sort_by' in request.form and request.form['sort_by'] == 'name':
            
            # Logic for reverse alphabetic search
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(Projects.name.desc())

            # Logic for standard alphabetic search
            else:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(Projects.name)

        # Logic for sorting items by creation date
        elif 'sort_by' in request.form and request.form['sort_by'] == 'created':

            # Logic for standard recent search
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(func.date(
                                                   Projects.created_time))

            # Logic for reverse recent search
            else:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(func.date(
                                                   Projects \
                                                   .created_time).desc())

        # Logic for sorting items by number of forks
        elif 'sort_by' in request.form and request.form['sort_by'] == 'forks':

            # Logic for sorting items by fork count, least first
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(Projects.forks)

            # Logic for sorting items by fork count, greatest first
            else:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(Projects.forks.desc())

        # Logic for sorting items by number of watchers
        elif 'sort_by' in request.form \
             and request.form['sort_by'] == 'watchers':

            # Logic for sorting items by watcher count, least first
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(Projects.watchers)

            # Logic for sorting items by watcher count, greatest first
            else:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(
                                                   Projects.watchers.desc())

        # Logic for sorting items by number of issues
        elif 'sort_by' in request.form \
             and request.form['sort_by'] == 'issues':

            # Logic for sorting items by issues count, least first
            if 'reverse' in request.form:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(
                                                   Projects.open_issues)

            # Logic for sorting items by issues count, greatest first
            else:
                projects_search_results_data = projects_search_results_data \
                                               .order_by(
                                                   Projects \
                                                   .open_issues.desc())

        # Refresh the page after searching
        return redirect(request.path)

    # Logic for favoriting a project
    elif request.method == 'POST' and 'fav_name' in request.form:

        # Look for whether this project is already favorited
        favorite = Favorites.query.filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['fav_name'],
                 Favorites.fav_type=='project')).first()

        # If the favorite does not already exist, continue adding the favorite
        if favorite is None:

            # Form the Favorites object
            new_fav = Favorites(
                id=random.randint(-9223372036854775808, 9223372036854775807),
                user_id=current_user.id,
                fav_name=request.form['fav_name'],
                fav_type='project')

            # Add and commit the Favorites object
            db.session.add(new_fav)
            db.session.commit()

        # Refresh the page after favoriting
        return redirect(request.path)

    # Logic for unfavoriting a project
    elif request.method == 'POST' and 'unfav_name' in request.form:

        # Look for the Favorite going to be deleted
        fav = db.session.query(Favorites).filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['unfav_name'],
                 Favorites.fav_type=='project')).first()

        # Remove the Favorites record and commit
        db.session.delete(fav)
        db.session.commit()

        # Refresh the page after unfavoriting
        return redirect(request.path)

    # Render the page for logged-in users and anonymous users
    else:
        try:
            
            # Render the page for logged-in users
            return render_template(
                'projects_search.html',
                search_results=projects_search_results_data.paginate(
                    page=page,
                    per_page=projectsPerPage),
                search_term=search_term,
                title='OSP | Projects',
                favorites=Favorites.query.filter(
                    and_(Favorites.user_id==current_user.id,
                         Favorites.fav_type=='project')) \
                .with_entities(
                    Favorites.fav_name))

        # If the previous rendering fails, default to anonymous rendering
        except:

            # Render the page for anonymous users
            return render_template(
                'projects_search.html',
                search_results=projects_search_results_data.paginate(
                    page=page,
                    per_page=projectsPerPage),
                search_term=search_term,
                title='OSP | Projects',
                favorites=[])

# Route for the organizations page
@app.route('/organizations', methods=['GET', 'POST'])
def organizations():

    # Bring in te necessary global variables
    global orgs_search_results_data
    global search_term
    global orgsPerPage

    # Bring in the page number from the arguments
    page = request.args.get('page', 1, type=int)

    # Logic for searching orgs
    if request.method == 'POST' and 'search_term' in request.form:

        # Bring in the search term from the form
        search_term=request.form['search_term']

        # Perform search by looking for search term in org names
        orgs_search_results_data = Organizations.query.filter(
            Organizations.name.contains(search_term))

        # Pull in the item count per page if necessary
        if 'per_page' in request.form:
                        orgsPerPage = int(request.form['per_page'])

        # Logic for search by name
        if 'name' in request.form:

            # Logic for reverse alphabetic search
            if 'reverse' in request.form:
                orgs_search_results_data = orgs_search_results_data.order_by(
                    Organizations.name.desc())
                
            # Logic for standard alphabetic search
            else:
                orgs_search_results_data = orgs_search_results_data.order_by(
                    Organizations.name)

        # Refresh the page after search
        return redirect(request.path)

    # Logic for favoriting an org
    if request.method == 'POST' and 'fav_name' in request.form:

        # Check if the favorites object already exists
        favorite=Favorites.query.filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['fav_name'],
                 Favorites.fav_type=='org')).first()

        # If the favorite does not already exist, form the Favorites record
        if favorite is None:

            # Form the favorites record
            new_fav = Favorites(
                id=random.randint(-9223372036854775808, 9223372036854775807),
                user_id=current_user.id,
                fav_name=request.form['fav_name'],
                fav_type='org')

            # Add the favorite and commit it
            db.session.add(new_fav)
            db.session.commit()

        # Refresh the page after searching
        return redirect(request.path)

    # Logic for unfavoriting an org
    elif request.method == 'POST' and 'unfav_name' in request.form:

        # Look for the existing favorites record
        fav = db.session.query(Favorites).filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['unfav_name'],
                 Favorites.fav_type=='org')).first()

        # delete the favorite and commit
        db.session.delete(fav)
        db.session.commit()

        # Refresh the page after unfavoriting
        return redirect(request.path)

    # Render the page for logged-in users and anonymous users
    else:
        try:

            # Render page for logged-in users
            return render_template(
                'organizations.html',
                search_results=orgs_search_results_data.paginate(
                    page=page,
                    per_page=orgsPerPage),
                search_term=search_term,
                projects=Projects.query.all(),
                title='OSP | Organizations',
                favorites=Favorites.query.filter(
                    and_(Favorites.user_id==current_user.id,
                         Favorites.fav_type=='org')) \
                .with_entities(Favorites.fav_name))

        # If the above rendering fails, render the anonymous page
        except:

            #Render page for anonymous users
            return render_template(
                'organizations.html',
                search_results=orgs_search_results_data.paginate(
                    page=page,
                    per_page=orgsPerPage),
                search_term=search_term,
                projects=Projects.query.all(),
                title='OSP | Organizations',
                favorites=[])

# Route for individual project pages
@app.route('/project/<projectName>', methods=['GET', 'POST'])
def project(projectName):

    # Logic for favoriting the project
    if request.method == 'POST' and 'fav_name' in request.form:

        # Look for whether the favorite record already exists
        favorite=Favorites.query.filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['fav_name'],
                 Favorites.fav_type=='project')).first()

        # If the Favorite record does not yet exist, create it
        if favorite is None:
            
            # Create the Favorites record
            new_fav = Favorites(
                id=random.randint(-9223372036854775808, 9223372036854775807),
                user_id=current_user.id,
                fav_name=request.form['fav_name'],
                fav_type='project')

            # Add and commit the Favorites record
            db.session.add(new_fav)
            db.session.commit()

        # Refresh the page after favoriting
        return redirect(request.path)

    # Logic for unfavoriting the project
    elif request.method == 'POST' and 'unfav_name' in request.form:

        # Look for the existing Favorites record
        fav = db.session.query(Favorites).filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['unfav_name'],
                 Favorites.fav_type=='project')).first()

        # Delete the Favorite and commit
        db.session.delete(fav)
        db.session.commit()

        # Refresh the page after unfavoriting
        return redirect(request.path)

    # Try to render the page for this project
    try:

        # Retrieve the date for the project page
        proj = Projects.query.filter(Projects.name==projectName).one()
        orgName = Organizations.query.filter(
            Organizations.name==proj.owner).one()
        projs = Projects.query.filter(Projects.owner==orgName.name)
        count = projs.count()

        # Render the page for logged-in users
        try:
            return render_template(
                'project.html',
                project=proj,
                projects=projs,
                count=count,
                title='OSP | ' + projectName,
                favorites=Favorites.query.filter(
                    and_(Favorites.user_id==current_user.id,
                         Favorites.fav_type=='project')) \
                .with_entities(Favorites.fav_name))
        
        # Render the page for anonymous users
        except:
            return render_template(
                'project.html',
                project=proj,
                projects=projs,
                count=count,
                title='OSP | ' + projectName,
                favorites=[])

    # If the project does not exist, render the 404 page
    except:
        return render_template('404.html', title='OSP | 404'), 404

# Route for individual organization pages
@app.route('/org/<orgName>', methods=['GET', 'POST'])
def organization(orgName):

    # Logic for favoriting an org
    if request.method == 'POST' and 'fav_name' in request.form:

        # Look for whether the org exists
        favorite=Favorites.query.filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['fav_name'],
                 Favorites.fav_type=='project')).first()

        # If the favorite does not exist, create it
        if favorite is None:

            # Create the Favorites record
            new_fav = Favorites(
                id=random.randint(-9223372036854775808, 9223372036854775807),
                user_id=current_user.id,
                fav_name=request.form['fav_name'],
                fav_type='org')

            # Add the favorite and commit it
            db.session.add(new_fav)
            db.session.commit()

        # Refresh the page after favoriting
        return redirect(request.path)

    # Logic for unfavoriting the org
    elif request.method == 'POST' and 'unfav_name' in request.form:

        # Look for the existing Favorites record
        fav = db.session.query(Favorites).filter(
            and_(Favorites.user_id==current_user.id,
                 Favorites.fav_name==request.form['unfav_name'],
                 Favorites.fav_type=='org')).first()

        # Delete the favorites record and commit
        db.session.delete(fav)
        db.session.commit()

        # Refresh the page after unfavoriting
        return redirect(request.path)

    # Try to render the page for the org
    try:

        # Retrieve the necessary data
        org = Organizations.query.filter(Organizations.name==orgName).one()
        projs = Projects.query.filter(Projects.owner==orgName)

        # Render the page for logged-in users
        try:
            return render_template(
                'organization.html',
                organization=org,
                projects=projs,
                title='OSP | ' + orgName,
                favorites=Favorites.query.filter(
                    and_(Favorites.user_id==current_user.id,
                         Favorites.fav_type=='org')) \
                .with_entities(Favorites.fav_name))

        # Render the page for anonymous users
        except:
            return render_template(
                'organization.html',
                organization=org,
                projects=projs,
                title='OSP | ' + orgName,
                favorites=[])

    # If page rendering fails, render the 404 page
    except:
        return render_template('404.html', title='OSP | 404'), 404

# Route for profile page
@main.route('/profile')
@login_required
def profile():

    # Render the profile for a logged in user
    return render_template('profile.html',
                           name=current_user.name,
                           title='OSP | Profile',
                           favProjsCount=Favorites.query.filter(
                               and_(Favorites.user_id==current_user.id,
                                    Favorites.fav_type=='project')).count(),
                           favOrgsCount=Favorites.query.filter(
                               and_(Favorites.user_id==current_user.id,
                                    Favorites.fav_type=='org')).count(),
                           favorites=Favorites.query.filter(
                               Favorites.user_id==current_user.id))


# Route for 404 page
@app.errorhandler(404)
def page_not_found(e):

    # Render the 404 page
    return render_template('404.html', title='OSP | 404'), 404
