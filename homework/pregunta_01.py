# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def cargar_data():
    df = pd.read_csv('files/input/shipping-data.csv', sep=',', index_col = 0)
    return df
    


def pregunta_01():
    
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    output_dir = 'docs'
    os.makedirs(output_dir, exist_ok=True)
    df = cargar_data()
    visual_warehouse(df, output_dir)
    visual_mode_of_shipping(df, output_dir)
    visual_customer_rating(df, output_dir)
    visual_weight_distribution(df, output_dir)
    crear_html(output_dir)
# VISUAL FOR SHIPPING PER WAREHOUSE
def visual_warehouse(df, output_dir):
    df = df.copy()
    plt.figure()
    counts = df['Warehouse_block'].value_counts()
    counts.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8,
    )
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.savefig(os.path.join(output_dir, 'shipping_per_warehouse.png'))
    plt.savefig('docs/shipping_per_warehouse.png')
    

# VISUAL FOR MODE OF SHIPPING

def visual_mode_of_shipping(df, output_dir):
    df = df.copy()
    plt.figure()
    counts = df['Mode_of_Shipment'].value_counts()
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel='',
        colors=['tab:blue', 'tab:orange', 'tab:green'],
    )
    plt.savefig(os.path.join(output_dir, 'mode_of_shipment.png'))
    
 
# VISUAL FOR AVERAGE CUSTOMER RATING

def visual_customer_rating(df, output_dir):
    df = df.copy()
    plt.figure()
    df = (
        df[['Mode_of_Shipment', 'Customer_rating']].groupby('Mode_of_Shipment').describe()
    )
    df.columns = df.columns.droplevel()
    df = df[['mean', 'min', 'max']]
    plt.barh(
        y=df.index.values,
        width=df['max'].values - 1,
        left=df['min'].values,
        height=0.9,
        color='lightgray',
        alpha=0.8,
    )
    colors = [
        'tab:green' if value >= 3.0 else 'tab:orange' for value in df['mean'].values
        
    ]
    plt.barh(
        y=df.index.values,
        width=df['mean'].values - 1,
        left=df['min'].values,
        color=colors,
        height=0.5,
        alpha=1.0,
    )
    plt.title('Average Customer Rating')
    plt.gca().spines['left'].set_color('gray')
    plt.gca().spines['bottom'].set_color('gray')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.savefig(os.path.join(output_dir, 'average_customer_rating.png'))
    
    
# VISUAL FOR WEIGHT DISTRIBUTION

def visual_weight_distribution(df, output_dir):
    df=df.copy()
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title='Shippen Weight Distribution',
        color='tab:orange',
        edgecolor='white',
    )
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.savefig(os.path.join(output_dir, 'weight_distribution.png'))

def crear_html(output_dir):
    """Crea el archivo index.html que muestra los gráficos."""
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shipping Dashboard</title>
    </head>
    <body>
        <h1>Shipping Dashboard Example</h1>
        <div style="width:45%; float:left;">
            <img src="shipping_per_warehouse.png" alt="Fig 1">
            <img src="mode_of_shipment.png" alt="Fig 2">
        </div>
        <div style="width:45%; float:left;">
            <img src="average_customer_rating.png" alt="Fig 3">
            <img src="weight_distribution.png" alt="Fig 4">
        </div>
    </body>
    </html>
    """
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(html_code)