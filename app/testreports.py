from database import get_db
from reports.ventas import generar_reporte_ventas

def test_reporte_ventas():
    db = next(get_db())
    
    print("\nTEST REPORTE VENTAS:")
    generar_reporte_ventas(
        db,
        fecha_inicio="2023-01-01",
        fecha_fin="2023-12-31",
        categorias=["souvenir", "ropa"],
        metodos_pago=["tarjeta"],
        stock_critico=True,
        export_csv="test_ventas.csv"
    )

if __name__ == "__main__":
    test_reporte_ventas()
    
    
#hola