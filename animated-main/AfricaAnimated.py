from fastapi import FastAPI
import pandas as pd
from fastapi.staticfiles import StaticFiles
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#valor_global = None
df = pd.read_csv("01 renewable-share-energy.csv")

app.mount("/animaciones", StaticFiles(directory="animaciones"), name="animaciones")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pais/{nombre_pais}")
def read_pais(nombre_pais: str):

    valor_global = nombre_pais
    generar_animacion(valor_global)
    return {"animacion_generada_para": valor_global}

def generar_animacion(pais):
    df_filtrado = df[df["Entity"] == pais].sort_values("Year")

    if df_filtrado.empty:
        return

    years = df_filtrado["Year"].values
    valores = df_filtrado["Renewables (% equivalent primary energy)"].values

    fig, ax = plt.subplots()
    ax.set_xlim(years.min(), years.max())
    ax.set_ylim(0, valores.max() + 5)
    ax.set_title(f"Energía Renewables en {pais}")
    ax.set_xlabel("Año")
    ax.set_ylabel("Renewables (% energía primaria)")
    ax.grid(True)

    linea, = ax.plot([], [], lw=2, color='blue', label=pais)
    texto = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    ax.legend()

    def init():
        linea.set_data([], [])
        texto.set_text('')
        return linea, texto

    def update(frame):
        x = years[:frame + 1]
        y = valores[:frame + 1]
        linea.set_data(x, y)
        texto.set_text(f"Año: {x[-1]}")
        return linea, texto

    ani = FuncAnimation(fig, update, frames=len(years), init_func=init, blit=True, interval=150)

    ruta = f"animaciones/{pais}_Renewables.gif"
    ani.save(ruta, writer="pillow", fps=5)
    plt.close(fig)

@app.get("/paises")
def read_paises():  
        df = pd.read_csv("01 renewable-share-energy.csv")
        read_paises = df["Entity"].unique()
        return read_paises.tolist()