from flask import Flask,render_template,url_for,Markup,request
import pandas as pd
import folium
import os
import numpy as np

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


#@app.route('/', methods=['POST'])
#def my_form_post():
#    text = request.form['action']
#    return text

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/map', methods=['GET', 'POST'])
def my_form_post():
    bezp = int(request.values.get('bezpieczenstwo')) # Your form's
    kult = int(request.values.get('kultura')) # input names
    return map(bezp,kult)

@app.route("/map")
def map(bezp,kult):
    geo='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/poland.geojson'
    data = pd.read_excel(r'C:\Users\arek\Desktop\Data Science\projekty\map_folium_flask\data\data.xlsx')
    m = folium.Map(location=[52,19], zoom_start=6)
    data['wypadki']=(data['wypadki']-np.min(data['wypadki']))/(np.max(data['wypadki'])-np.min(data['wypadki']))
    data['kultura']=(data['kultura']-np.min(data['kultura']))/(np.max(data['kultura'])-np.min(data['kultura']))
    data['wspolczynnik']=data['wypadki']*bezp+data['kultura']*kult
    m.choropleth(
        geo_data=geo,
        name='choropleth',
        data=data,
        columns=['wojewodztwo','wspolczynnik'],
        key_on='properties.name',
        fill_color='YlGn',
        fill_opacity=0.8,
        line_opacity=0.2,
    )


    folium.LayerControl().add_to(m)

    html_string = Markup(m._repr_html_())
    return render_template('map.html',title='Map',map=html_string)

if __name__=='__main__':
    app.run(debug=True)
