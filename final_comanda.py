from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
from os import *
import sqlite3
import re



def llamar_base():
    base = sqlite3.connect("base.db")
    return base

def crear_tabla():
    conexion = llamar_base()
    cursor = conexion.cursor()
    sql = "CREATE TABLE comanda(n_ticket INTEGER PRIMARY KEY AUTOINCREMENT, mesa integer, producto text, cantidad integer, subtotal real, iva real, total real)"
    cursor.execute(sql)
    conexion.commit()

  

def valor_total(valores4, valores3):
    total = valores4 + valores4 * valores3 / 100
    return total

def valor_subtotal(a, b):
    total = a * b
    return total

def actualizar(mitree):
    recorrer = mitree.get_children()
    for i in recorrer:
        mitree.delete(i)

    conexion = llamar_base()
    cursor = conexion.cursor()
    sql = "SELECT * FROM comanda ORDER BY n_ticket ASC"
    info = cursor.execute(sql)
    data = info.fetchall()
    for x in data:
        mitree.insert("", 0, text=x[0] ,values=(x[1], x[2], x[3], x[4], x[5], x[6]))



def guardado(mesa, cantidad, producto, valor, iva, tree):
    conexion = llamar_base()
    cursor = conexion.cursor()
    patron = "^[0-9]*$"
    if (re.match(patron, cantidad)):

        cantidades = int(cantidad)
        precio = float(valor)
        iva1 = float(iva)
        subtotal = valor_subtotal(cantidades, precio)
        total = valor_total(subtotal,iva1)
        datos = (mesa, cantidad, producto, subtotal, iva, total)
        sql = "INSERT INTO comanda(mesa, cantidad, producto, subtotal, iva, total) VALUES(?,?,?,?,?,?)"
        cursor.execute(sql, datos)
        conexion.commit()
        actualizar(tree)
    else:
        print("Error en campo cantidad")




def editado(mesa, cantidad, producto, valor, iva, tree):
    conexion = llamar_base()
    cursor = conexion.cursor()
    patron = "^[0-9]*$"
    if (re.match(patron, cantidad)):
        cantidades = int(cantidad)
        precio = float(valor)
        iva1 = float(iva)
        subtotal = valor_subtotal(cantidades, precio)
        total = valor_total(subtotal,iva1)        
        data = tree.selection()
        item = tree.item(data)
        ticket = item["text"]
        sql = "UPDATE comanda SET mesa = ?, cantidad = ?, producto = ?, subtotal = ?, iva = ?, total = ? WHERE n_ticket = ?"
        datos = (mesa, cantidad, producto, subtotal, iva, total, ticket)        
        cursor.execute(sql, datos)
        conexion.commit()
        actualizar(tree)
    else:
        print("No se puede editar")    
    
def eliminado(tree): 
    conexion = llamar_base()
    cursor = conexion.cursor()
    data = tree.selection()
    item = tree.item(data)
    ticket = (item["text"],)
    sql = "DELETE FROM comanda WHERE n_ticket = ?"
    cursor.execute(sql, ticket)
    conexion.commit()
    actualizar(tree)

def colores():
    gama = askcolor(color="#45df21", title="Elige tu color")
    ventana.config(background=gama[1])
      

ventana = Tk()

ventana.title("Bienvenidos a Mundo Comanda")

var_mesa = StringVar()
var_cantidad = StringVar()
var_producto = StringVar()
var_valor = StringVar()
var_iva = StringVar()

mesa = Label(ventana, text="Mesa", bg="gray45", fg="black" )
mesa.grid(row=0, column=0)
cantidad = Label(ventana, text="Cantidad", bg="gray45", fg="black")
cantidad.grid(row=0, column=1)
producto = Label(ventana, text="Descripcion", bg="gray45", fg="black")
producto.grid(row=0, column=2)
valor = Label(ventana, text="Precio",bg="gray45", fg="black" )
valor.grid(row=0, column=3)
iva = Label(ventana, text="Iva", bg="gray45", fg="black" )
iva.grid(row=0, column=4)


entry_mesa = Entry(ventana, textvariable=var_mesa, width=20,bg="wheat1", fg="black" )
entry_mesa.grid(row=1, column=0)
entry_cantidad = Entry(ventana, textvariable=var_cantidad,bg="wheat1", fg="black")
entry_cantidad.grid(row=1, column=1)
entry_producto = Entry(ventana, textvariable=var_producto, width=30,bg="wheat1", fg="black")
entry_producto.grid(row=1, column=2)
entry_valor = Entry(ventana, textvariable=var_valor,bg="wheat1", fg="black")
entry_valor.grid(row=1, column=3)
entry_iva = Entry(ventana,textvariable=var_iva,bg="wheat1", fg="black")
entry_iva.grid(row=1, column=4)



tree = ttk.Treeview(ventana)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6", "col7")
tree.column("#0", width=60, anchor=E)
tree.column("col1", width=60, anchor=E)
tree.column("col2", width=80, anchor=E)
tree.column("col3", width=65, anchor=E)
tree.column("col4", width=80, anchor=E)
tree.column("col5", width=60, anchor=E)
tree.column("col6", width=70, anchor=E)
tree.column("col7", width=80, anchor=E)


tree.grid(row=5, column=0, columnspan= 10)

boton_guardar = Button(ventana, text="Guardar",command=lambda:guardado(var_mesa.get(), var_cantidad.get(), var_producto.get(), var_valor.get(), var_iva.get(), tree), bg="gray25", fg="white", font=("arial", 9, "bold"))
boton_guardar.grid(row=3, column=1)
boton_editar = Button(ventana, text="Editar",command=lambda:editado(var_mesa.get(), var_cantidad.get(), var_producto.get(), var_valor.get(), var_iva.get(), tree), bg="gray25", fg="white", font=("arial", 9, "bold") )
boton_editar.grid(row=3, column=2)
boton_eliminar = Button(ventana, text="Eliminar", command=lambda:eliminado(tree), bg="gray25", fg="white", font=("arial", 9, "bold"))
boton_eliminar.grid(row=3, column=3)
boton_consultar = Button(ventana, text="Consultar", command=lambda:actualizar(tree), bg="gray25", fg="white", font=("arial", 9, "bold"))
boton_consultar.grid(row=3, column=4)

barra = Menu(ventana)

mi_menu = Menu(barra, tearoff=0)
mi_menu.add_command(label="Color", command=lambda:colores())
mi_menu.add_separator()
mi_menu.add_command(label="Salir", command=ventana.quit)
barra.add_cascade(label="Archivo", menu=mi_menu)
ventana.config(menu=barra)
ventana.config(background="#a4a4a4")

ventana.mainloop()