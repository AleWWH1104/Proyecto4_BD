# app/reports_tests.py
from reports import reports
from database import SessionLocal
from models import VistaControlAnimal, VistaConservacion, VistaFinancieraMensual
from datetime import date, timedelta

def test_reporte_control_animal():
    """Prueba el reporte de control animal con múltiples filtros"""
    print("\n=== Probando Reporte de Control Animal ===")
    db = SessionLocal()
    reporte = reports.ReporteControlAnimal()
    
    # Filtros significativos
    resultados = reporte.generar(
        db,
        especie="Panthera tigris",
        estado_salud=["excelente"],
        habitat="Jungla de Asia",
        edad_min=2,
        edad_max=10,
        peso_min=50,
        peso_max=200,
        ultima_alimentacion_dias=3
    )
    
    print(f"Encontrados {len(resultados)} animales que cumplen los criterios")
    
    # Exportar a CSV
    fieldnames = [
        'id_animal', 'nombre_animal', 'especie', 'estado_conservacion', 
        'habitat', 'estado_salud', 'peso_actual', 'fecha_nacimiento',
        'edad_aproximada', 'cuidador_principal', 'ultima_alimentacion_fecha'
    ]
    reports.export_to_csv(
        [r.__dict__ for r in resultados],
        fieldnames,
        "reporte_control_animal.csv"
    )
    print("Reporte exportado a: reporte_control_animal.csv")

def test_reporte_conservacion():
    """Prueba el reporte de estado de conservación"""
    print("\n=== Probando Reporte de Conservación ===")
    db = SessionLocal()
    reporte = reports.ReporteConservacion()
    
    # Filtros significativos
    resultados = reporte.generar(
        db,
        estado_conservacion=["vulnerable", "peligro"],
        cantidad_min=1,
        cantidad_max=10,
        esperanza_vida_min=5,
        esperanza_vida_max=30,
        cuidadores_min=2,
        veterinarios_min=1,
        habitat="Selva"
    )
    
    print(f"Encontradas {len(resultados)} especies que cumplen los criterios")
    
    # Exportar a CSV
    fieldnames = [
        'id_especie', 'nombre_cientifico', 'nombre_comun', 
        'estado_conservacion', 'cantidad_en_zoo', 'habitat_principal',
        'rango_temperatura', 'rango_humedad', 'cuidadores_asignados',
        'veterinarios_especializados'
    ]
    reports.export_to_csv(
        [r.__dict__ for r in resultados],
        fieldnames,
        "reporte_conservacion.csv"
    )
    print("Reporte exportado a: reporte_conservacion.csv")

def test_reporte_financiero():
    """Prueba el reporte financiero mensual"""
    print("\n=== Probando Reporte Financiero ===")
    db = SessionLocal()
    reporte = reports.ReporteFinanciero()
    
    # Filtros significativos
    resultados = reporte.generar(
        db,
        mes_inicio="2024-01",
        mes_fin="2024-06",
        ingresos_min=5000,
        gastos_max=3000,
        balance_min=1000,
        ordenar_por="ingresos_totales",
        orden_desc=True
    )
    
    print(f"Encontrados {len(resultados)} meses que cumplen los criterios")
    
    # Exportar a CSV
    fieldnames = [
        'mes', 'ingresos_eventos', 'ingresos_ventas', 'costos_mantenimiento',
        'gastos_tratamientos', 'costos_alimentos', 'costos_salarios',
        'ingresos_totales', 'gastos_totales', 'balance_mensual'
    ]
    reports.export_to_csv(
        [r.__dict__ for r in resultados],
        fieldnames,
        "reporte_financiero.csv"
    )
    print("Reporte exportado a: reporte_financiero.csv")

# Ejecutar todas las pruebas
if __name__ == "__main__":
    test_reporte_control_animal()
    test_reporte_conservacion()
    test_reporte_financiero()
    print("\n¡Todas las pruebas completadas exitosamente!")