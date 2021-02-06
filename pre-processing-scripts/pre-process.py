#!/usr/bin/env python

import pandas
import sys
import os
import datetime as dt

# Introducir las claves y valores del diccionario siempre en minusculas.
categories = {
    'traspaso': [	'ajuste', 'separacion fija mensual', 'imantia', 'optimal income', 'abanca r.f', 'ahorro', '304-0522-002815/4', '381-0522-004764/2', 'compensacion', 'cancelacion vto', 'renovacion vto', 'asignar modalidad', 'calderilla'],
'nomina': [	'silenus', 'itelsis', 'oesia', 'deusto', 'coremain', 'zemsania', 'nortempo', 'smtecno', 'plexus', 'servicio publico de empleo estatal'],
'extras': [	'i.r.p.f'],
'seguro coche': [	'a.m.a'],
'reintegros': [	'reintegro'],
'vivienda': [	'candamo'],
'luz': [	'gas natural', 'comercializadora', 'naturgy'],
'telefono': [	'pepephone', 'pepemobile'],
'seguros': [	'metlife'],
'suscripciones': [	'paypal', 'itunes', 'prime', 'evernote', 'cruz roja', 'serviocio', 'apple.com'],
'coche': [	'midas', 'noya', 'citroen', 'itv'],
'combustible': [	'inrola', 'galuresa', 'ckm', 'repsol', 'cepsa', 'alcobendas', 'mararnelas', 'es1808121234', 'tercar', 'compostela\alcobend', 'est. serv', 'e.de servicio', 'estacion servicio'],
'peajes': [	'5020640000192516'],
'seguro casa': [	'mgs'],
'aparcamiento': [	'aparcamiento', 'parking'],
'dietas': [	'catering'],
'ocio': [	'cafeter', 'serviocio', 'restaura'],
'deuda': [	'deuda'],
'otros': [	'serviocio', 'corte ingle', 'amazon', 'juguettos', 'espazio', 'camelot'],
'super': [	'alcampo', 'dia vilag', 'gadis', 'mercadona', 'froiz', 'farmacia', 'supermercado', 'fruter', '767001072783', 'familia'],
'intereses': [	'intereses'],
'comisiones': [	'comision'],
'impuestos': [	'concello de vilagarc', 'espina y delf'],
'internet': [	'movistar', 'telefonica'],
'inversion': [	'7503 0084293 elisa brion rey', '7503 0084300 maria luisa brion r', '7503 0084954 maria del carmen br'],
'educacion': [	'bonecos'],
}

def _get_category(concept):
    for k,v in categories.items():
        for val in v:
            if val in concept.lower():
                return k
    return 'otros'


if len(sys.argv) <= 1:
    print("No se ha proporcionado ruta de ficheros. Fin de procesamiento.")
    sys.exit(0)
path = sys.argv[1]

total_df = pandas.DataFrame()
dataframes = []

for file in os.listdir(path):
    if not file.endswith('.csv'):
        continue

    filename = file.split('.')
    name = filename[0]
    suffix = '.' + filename[1]
    cuenta='Abanca - '+file.split(' ')[0][0].upper()+file.split(' ')[0][1:]

    df = pandas.read_csv(os.path.join(path, file), sep=';', index_col='Fecha ctble')

    df['Importe'] = df['Importe'].str.replace(',', '.').astype(float)
    df['Saldo'] = df['Saldo'].str.replace(',', '.').astype(float)

    if 'plazo' in file.lower():
        df['Fecha valor'] = pandas.to_datetime(df['Fecha valor'], format="%d-%m-%Y")
        df = df.sort_values(by='Fecha valor', ascending=True)
        importe_transformado = []
        fecha_transformada = []
        ultimo_saldo = 0
        for i in range(len(df['Saldo'])):
            importe_transformado.append(df['Saldo'][i]-ultimo_saldo)
            ultimo_saldo = df['Saldo'][i]
            fecha_transformada.append(df['Fecha valor'][i].strftime("%d-%m-%Y"))
        df['Importe'] = importe_transformado
        df['Fecha valor'] = fecha_transformada

    category = []
    for value in df['Concepto']:
        category.append(_get_category(value))
    df['Categoria'] = category


    del df['Saldo']
    del df['Moneda.1']
    df['Cuenta'] = cuenta

    dataframes.append(df)

total_df = pandas.concat(dataframes)
total_df.to_csv(os.path.join(path, 'output'+'_post_proc'+suffix), sep=';', header=None)
