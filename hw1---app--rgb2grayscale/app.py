from dash import Dash,html, dcc
from dash.dependencies import Input, Output, State
import cv2
import io
#from sys import argv
import base64
#from os import path, getcwd, listdir
import plotly.express as px
import numpy as np
#--------------------------------------------------------------------------------
#APP PARA CONVERTIR IMAGENES A BLANCO Y NEG
#1) crea un entorno virtual: python3 -m venv venv
#2) activa el entorno virtual: source venv/bin/activate
#3) ejecuta: pip install requirements.txt
#4) ejecuta en terminal: python3 app.py
#--------------------------------------------------------------------------------



app = Dash(__name__)
app.layout = html.Div([
    html.H1("Convertidor Blanco y Negro"),
    html.H2("Cargar imagen"),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Arrastra o suelta',
            html.A('Selecciona una imagen')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Div(id='output-image-upload'),
])

@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename')
)
def convert_to_bw(contents, filename):
    if contents is not None:
        # Leer la imagen subida
        _, content_string = contents.split(',')
        decoded_image = io.BytesIO(base64.b64decode(content_string))
        img = cv2.imdecode(np.frombuffer(decoded_image.read(), np.uint8), -1)

        # Convertir la imagen a blanco y negro
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Codificar la imagen en blanco y negro a base64
        _, buffer = cv2.imencode('.jpg', gray_img)
        encoded_image = base64.b64encode(buffer).decode('utf-8')
        img_src = f'data:image/jpeg;base64,{encoded_image}'

        # Mostrar la imagen convertida
                # Mostrar la imagen convertida
        return html.Div([
            html.H3(f'Imagen cargada: {filename}'),
            html.Div([
                html.Img(src=img_src, style={'width': '100%', 'height': 'auto', 'display': 'block', 'margin': 'auto'}),
            ], style={
                'border': '2px solid #d3d3d3',
                'padding': '10px',
                'borderRadius': '10px',
                'boxShadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
                'textAlign': 'center',
                'maxWidth': '500px',
                'margin': 'auto'
            })
        ])
    else:
        return html.Div('No se ha cargado ninguna imagen')
    



if __name__ == '__main__':
    app.run_server(debug=True)