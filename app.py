from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import forms

app = Flask(__name__)


df = pd.read_excel('data.xlsx')
df2 = pd.read_excel('data2.xlsx')

@app.route('/', methods=['GET', 'POST'])
def index():  # put application's code here
    vereda = df['vereda']
    cultivo = df2['cultivo']
    data = {
        'vereda': vereda.tolist(),
        'cultivo': cultivo.tolist()
    }
    sueloForm = forms.sueloForm(request.form)

    if request.method == 'POST':
        svereda = request.form.get('vereda')
        scultivo = request.form.get('cultivo')
        sueloForm.vereda.data = svereda
        sueloForm.cultivo.data = scultivo
        return redirect (url_for('analisis', vereda = sueloForm.vereda.data, cultivo = sueloForm.cultivo.data))

    return render_template('index.html', **data, form = sueloForm)

@app.route('/analisis/<vereda>/<cultivo>')
def analisis(vereda, cultivo):
    if vereda == 'Barón Gallero':
        indice = 0
    else:
        try:
            indice = df.index[df['vereda'] == vereda].tolist()[0]
        except IndexError:
            print("No se encontro esa vereda")


    if vereda == 'papa':
        indice_C = 0
    else:
        try:
            indice_C = df2.index[df2['cultivo'] == cultivo].tolist()[0]
        except IndexError:
            print("No se encontro el tipo de cultivo")

    message = ""
    val_list = []

    # Compara el ph
    if df.iloc[indice]['ph'] >= df2.iloc[indice_C]['min_ph'] and df.iloc[indice]['ph'] <= df2.iloc[indice_C]['max_ph']:
            val_list.append(1)
    else:
            val_list.append(0)

    # Compara el nitrogeno
    if df.iloc[indice]['nitrogeno'] >= df2.iloc[indice_C]['min_nitrogeno'] and df.iloc[indice]['nitrogeno'] <= df2.iloc[indice_C]['max_nitrogeno']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el fosforo
    if df.iloc[indice]['fosforo'] >= df2.iloc[indice_C]['min_fosforo'] and df.iloc[indice]['fosforo'] <= df2.iloc[indice_C]['max_fosforo']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el potasio
    if df.iloc[indice]['potasio'] >= df2.iloc[indice_C]['min_potasio'] and df.iloc[indice]['potasio'] <= df2.iloc[indice_C]['max_potasio']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el magnesio
    if df.iloc[indice]['magnesio'] >= df2.iloc[indice_C]['min_magnesio'] and df.iloc[indice]['magnesio'] <= df2.iloc[indice_C]['max_magnesio']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el calcio
    if df.iloc[indice]['calcio'] >= df2.iloc[indice_C]['min_calcio'] and df.iloc[indice]['calcio'] <= df2.iloc[indice_C]['max_calcio']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el zinc
    if df.iloc[indice]['zinc'] >= df2.iloc[indice_C]['min_zinc'] and df.iloc[indice]['zinc'] <= df2.iloc[indice_C]['max_zinc']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el cic
    if df.iloc[indice]['cic'] >= df2.iloc[indice_C]['min_cic'] and df.iloc[indice]['cic'] <= df2.iloc[indice_C]['max_cic']:
        val_list.append(1)
    else:
        val_list.append(0)

    # Compara el salinidad
    if df.iloc[indice]['salinidad'] >= df2.iloc[indice_C]['min_salinidad'] and df.iloc[indice]['salinidad'] <= df2.iloc[indice_C]['max_salinidad']:
        val_list.append(1)
    else:
        val_list.append(0)

    compatible = {
        "nutriente" : ['ph','nitrogeno','fosforo','potasio','magnesio','calcio','zinc','cic','salinidad'],
        "val": val_list
    }

    val = 1

    for i in compatible["val"]:
        if i == 0:
            val = 0

    recoment = {}

    if val == 1:
        message = f"En la vereda {vereda} es posible plantar {cultivo}"

    else:
        message = f"En la vereda {vereda} no es posible plantar {cultivo}"
        recoment = {
            'ph': f"El ph de su suelo es {df.iloc[indice]['ph']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_ph']} - {df2.iloc[indice_C]['max_ph']}, deberias suministrar un fertilizante",
            'nitrogeno': f"El nitrogeno de su suelo es {df.iloc[indice]['nitrogeno']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_nitrogeno']} - {df2.iloc[indice_C]['max_nitrogeno']}, deberias suministrar un fertilizante",
            'fosforo': f"El fosforo de su suelo es {df.iloc[indice]['fosforo']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_fosforo']} - {df2.iloc[indice_C]['max_fosforo']}, deberias suministrar un fertilizante",
            'potasio': f"El potasio de su suelo es {df.iloc[indice]['potasio']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_potasio']} - {df2.iloc[indice_C]['max_potasio']}, deberias suministrar un fertilizante",
            'magnesio': f"El magnesio de su suelo es {df.iloc[indice]['magnesio']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_magnesio']} - {df2.iloc[indice_C]['max_magnesio']}, deberias suministrar un fertilizante",
            'calcio': f"El calcio de su suelo es {df.iloc[indice]['calcio']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_calcio']} - {df2.iloc[indice_C]['max_calcio']}, deberias suministrar un fertilizante",
            'zinc': f"El zinc de su suelo es {df.iloc[indice]['zinc']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_zinc']} - {df2.iloc[indice_C]['max_zinc']}, deberias suministrar un fertilizante",
            'cic': f"El cic de su suelo es {df.iloc[indice]['cic']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_cic']} - {df2.iloc[indice_C]['max_cic']}, deberias suministrar un fertilizante",
            'salinidad': f"El salinidad de su suelo es {df.iloc[indice]['salinidad']} y debería estar entre el siguiente rango {df2.iloc[indice_C]['min_salinidad']} - {df2.iloc[indice_C]['max_salinidad']}, deberias suministrar un fertilizante"

        }

    return render_template('analisis.html', message = message, **recoment,comp = compatible)

if __name__ == '__main__':
    app.run(debug=True)
