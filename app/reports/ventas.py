import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from models import VentaProducto, Producto, Visitante

def generar_reporte_ventas(
    db: Session,
    fecha_inicio: str = None,
    fecha_fin: str = None,
    categorias: list = None,
    metodos_pago: list = None,
    producto_id: int = None,
    visitante_id: int = None,
    stock_critico: bool = False,
    export_csv: str = "reporte_ventas.csv"
):
    # Construir query base
    query = db.query(
        VentaProducto,
        Producto,
        Visitante
    ).join(
        Producto,
        VentaProducto.id_producto == Producto.id_producto
    ).join(
        Visitante,
        VentaProducto.id_visitante == Visitante.id_visitante
    )

    # Aplicar filtros
    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            query = query.filter(VentaProducto.fecha_venta >= fecha_inicio)
        except ValueError:
            print("Formato de fecha inicio incorrecto. Usar YYYY-MM-DD")

    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            query = query.filter(VentaProducto.fecha_venta <= fecha_fin)
        except ValueError:
            print("Formato de fecha fin incorrecto. Usar YYYY-MM-DD")

    if categorias:
        query = query.filter(Producto.categoria.in_(categorias))

    if metodos_pago:
        query = query.filter(VentaProducto.metodo_pago.in_(metodos_pago))

    if producto_id:
        query = query.filter(VentaProducto.id_producto == producto_id)

    if visitante_id:
        query = query.filter(VentaProducto.id_visitante == visitante_id)

    if stock_critico:
        query = query.filter(Producto.stock_actual < Producto.stock_minimo)

    # Ejecutar consulta
    resultados = query.all()

    # Procesar resultados
    datos = []
    for venta, producto, visitante in resultados:
        datos.append({
            "Fecha": venta.fecha_venta.strftime("%Y-%m-%d"),
            "Producto": producto.nombre,
            "Categoría": producto.categoria,
            "Visitante": f"{visitante.nombre} {visitante.apellido}",
            "Cantidad": venta.cantidad,
            "Precio Unitario": float(venta.precio_unitario),
            "Total": float(venta.cantidad * venta.precio_unitario),
            "Método Pago": venta.metodo_pago,
            "Stock Actual": producto.stock_actual,
            "Stock Mínimo": producto.stock_minimo
        })

    # Crear DataFrame
    df = pd.DataFrame(datos)
    
    if df.empty:
        print("⚠️ No se encontraron ventas con los filtros aplicados")
        return None

    # Exportar a CSV
    df.to_csv(export_csv, index=False)
    print(f"✅ Reporte exportado a {export_csv}")
    print(df.head())
    
    return df