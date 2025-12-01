import mysql.connector
import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Query

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Contraseña302;",
        database="tienda"
    )

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://192.168.56.1:8081",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]

)

@app.get("/precios")
def get_precios():
    try:
        conn = get_connection()
        mycursor = conn.cursor()

        mycursor.execute("SELECT Precio FROM productos WHERE ProductoID = 1")

        myresult = mycursor.fetchall()

        precios = [precio[0] for precio in myresult]
        return JSONResponse(content={"precios": precios})
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
        

@app.get("/comprar")
def buy_disc(producto_id: int = Query(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Cantidad FROM productos WHERE ProductoID = %s", (producto_id,))
    cantidad = cursor.fetchone()[0]

    if cantidad > 0:
        cursor.execute("UPDATE productos SET Cantidad = Cantidad - 1 WHERE ProductoID = %s", (producto_id,))
        conn.commit()
        conn.close()
        return JSONResponse(content={"status": "Compra realizada"})
    else:
        conn.close()
        return JSONResponse(content={"status": "Sin stock disponible"}, status_code=400)
    

@app.get("/stock")
def get_stock(producto_id: int = Query(...)):
    
    try:
        conn = get_connection()

        mycursor = conn.cursor()

        mycursor.execute("SELECT Cantidad FROM productos WHERE ProductoID = %s", (producto_id,))

        myresult = mycursor.fetchall()

        quants = [quant[0] for quant in myresult]
        return JSONResponse(content={"cantidad": quants})
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    

@app.get("/productos/random")
def get_random_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Productos")
    all_products = cursor.fetchall()
    conn.close()

    # Pick 3 random products (or fewer if not enough)
    sample = random.sample(all_products, min(3, len(all_products)))
    return JSONResponse(content={"productos": sample})
