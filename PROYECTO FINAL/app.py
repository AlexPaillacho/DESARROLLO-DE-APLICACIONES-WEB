from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello, World- Bienvenidos!"


@app.route('/Page1/<StandPage>')
def Page1(StandPage):
    return f'Saludos Bienvenido nesecitas una, {StandPage}!' 


@app.route('/Page2/<LandPage>')
def Page2(LandPage):
    return f'Bienvenido nesecitas una, {LandPage}!'

@app.route('/Page3/<CorporacPage>')
def Page3(CorporacPage):
    return f'Bienvenido a la pagina para tu empresa , {CorporacPage}!'
    

if __name__ == "__main__":
    app.run(debug=True)
