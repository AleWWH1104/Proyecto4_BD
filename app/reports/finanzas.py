# app/reports/finanzas.py

import pandas as pd
from sqlalchemy.orm import Session
from models import VistaFinancieraMensual
from sqlalchemy import and_

def generar_reporte_financiero(
    db: Session,
    meses: list = None,
    ingresos_min: float = None,
    ingresos_max: float = None,
    gastos_max: float = None,
    balance_positivo: bool = None,
    eventos_min: int = None,
    export_csv: str = "reporte_finanzas_mensual.csv"
):
    query = db.query(VistaFinancieraMensual)

    if meses:
        query = query.filter(VistaFinancieraMensual.mes.in_(meses))
    
    if ingresos_min is not None:
        query = query.filter(VistaFinancieraMensual.ingresos_totales >= ingresos_min)
    
    if ingresos_max is not None:
        query = query.filter(VistaFinancieraMensual.ingresos_totales <= ingresos_max)
    
    if gastos_max is not None:
        query = query.filter(VistaFinancieraMensual.gastos_totales <= gastos_max)
    
    if balance_positivo is True:
        query = query.filter(VistaFinancieraMensual.balance_mensual > 0)
    elif balance_positivo is False:
        query = query.filter(VistaFinancieraMensual.balance_mensual <= 0)
    
    registros = query.all()

    data = []
    for r in registros:
        row = {
            "Mes": r.mes,
            "Ingresos por Eventos": r.ingresos_eventos,
            "Ingresos por Ventas": r.ingresos_ventas,
            "Costos de Mantenimiento": r.costos_mantenimiento,
            "Gastos Tratamientos": r.gastos_tratamientos,
            "Costos de Alimentos": r.costos_alimentos,
            "Costos de Salarios": r.costos_salarios,
            "Ingresos Totales": r.ingresos_totales,
            "Gastos Totales": r.gastos_totales,
            "Balance Mensual": r.balance_mensual
        }

        # Campos opcionales (si tu vista los incluye)
        if hasattr(r, "eventos_realizados"):
            row["Eventos Realizados"] = r.eventos_realizados
        if hasattr(r, "ingreso_promedio_evento"):
            row["Ingreso Promedio por Evento"] = r.ingreso_promedio_evento

        data.append(row)

    df = pd.DataFrame(data)

    df.to_csv(export_csv, index=False)
    print(f"\n Reporte financiero exportado a {export_csv}")
    print(df.head(10).to_string(index=False))  # Vista previa

    return df
