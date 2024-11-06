from flask import Flask
from flask import url_for
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from kgmodel import (Foresatt, Barn, Soknad, Barnehage)
from kgcontroller import (form_to_object_soknad, insert_soknad, commit_all, select_alle_barnehager)


app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY' # nødvendig for session

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/barnehager')
def barnehager():
    information = select_alle_barnehager()
    return render_template('barnehager.html', data=information)

@app.route('/behandle', methods=['GET', 'POST'])
def behandle():
    if request.method == 'POST':
        sd = request.form
        application = form_to_object_soknad(sd)
        
        # Determine offer/rejection based on criteria (e.g., available spots, income, priority)
        selected_barnehage = next((b for b in select_alle_barnehager() if b.barnehage_id == int(sd['barnehage_id'])), None)
        
        if selected_barnehage and selected_barnehage.barnehage_ledige_plasser > 0:
            # Here you could add more criteria to decide on "Tilbud" or "Avslag"
            status = 'Tilbud'
        else:
            status = 'Avslag'

        # Insert application into the database and save in session
        insert_soknad(application)
        session['information'] = {**sd, 'status': status}  # Add the status to session data

        return redirect(url_for('svar'))
    else:
        return render_template('soknad.html')


@app.route('/svar')
def svar():
    information = session.get['information']
    return render_template('svar.html', data=information)

@app.route('/commit')
def commit():
    commit_all()
    return render_template('commit.html')

if __name__ == '__main__':
    app.run(debug=True)

"""
Referanser
[1] https://stackoverflow.com/questions/21668481/difference-between-render_template-and-redirect
"""

"""
Søkeuttrykk

"""