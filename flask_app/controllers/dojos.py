from crypt import methods
from dataclasses import dataclass
from flask import render_template, request, redirect, session, url_for
from flask_app.models.dojo import Dojo  #change this import line based on your extra .py file for generating OOP instances
from flask_app.models.ninja import Ninja
from flask_app import app


@app.route("/dojos")     # lines 6 through 11 can be changed depending on what we need server.py to do.
def r_all_dojos():
    # call the get all classmethod to get all friends
    dojos = Dojo.get_all()
    return render_template("dojos.html", dojos = dojos)

@app.route('/dojos/<int:id>')
def r_assoc_ninjas(id):
    dojo_id = id
    data = {
        "dojo_id":dojo_id
    }
    students = Ninja.get_some(data)
    return render_template('ninjas.html', dojo_id = dojo_id, students = students)

@app.route('/ninjas')
def r_add_ninja():
    dojos = Dojo.get_all()
    return render_template('addNinjas.html', dojos = dojos)

@app.route('/add/ninja', methods = ['POST'])
def f_add_ninja():
    print(request.form.get('chosen_dojo'))
    if request.form.get('chosen_dojo') == 0:
        return redirect('/ninjas')

    data = {
        'dojo_id': request.form.get('chosen_dojo'),
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'age': request.form['age']
    }
    Ninja.add_ninja(data)
    return redirect(url_for('r_assoc_ninjas', id = request.form.get('chosen_dojo')))

@app.route('/edit/ninja/<int:id>')
def r_edit_ninja(id):
    data = {
        'ninja_id': id
    }
    student = Ninja.get_one(data)
    return render_template('editNinja.html', student = student)

@app.route('/update/ninja/<int:id>', methods = ['POST'])
def f_edit_ninja(id):
    data = {
        'ninja_id': id,
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'age': request.form['age']
    }
    Ninja.update_ninja(data)
    student = Ninja.get_one(data)
    return redirect(url_for('r_assoc_ninjas', id = student[0].dojo_id))

@app.route('/add/dojo', methods = ['POST'])
def f_add_dojo():
    data = {
        "dojo_name": request.form['dojo_name']
    }
    Dojo.add_dojo(data)
    return redirect("/dojos")

@app.route('/delete/ninja/<int:id>')
def rd_delete_ninja(id):
    data = {
        'ninja_id': id
    }
    ninja = Ninja.get_one(data)
    dojo_id = ninja[0].dojo_id
    Ninja.delete_ninja(data)
    return redirect(url_for('r_assoc_ninjas', id = dojo_id))