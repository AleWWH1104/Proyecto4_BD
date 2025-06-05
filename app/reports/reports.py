# app/reports.py
from sqlalchemy.orm import Session
import models
from utils import export_to_csv
from datetime import date, timedelta

class ReporteControlAnimal:
    def generar(
        self, 
        db: Session,
        especie: str = None,
        estado_salud: list = None,
        habitat: str = None,
        edad_min: int = None,
        edad_max: int = None,
        peso_min: float = None,
        peso_max: float = None,
        ultima_alimentacion_dias: int = None
    ):
        query = db.query(models.VistaControlAnimal)
        
        # Aplicar filtros
        if especie:
            query = query.filter(models.VistaControlAnimal.especie.ilike(f"%{especie}%"))
        if estado_salud:
            query = query.filter(models.VistaControlAnimal.estado_salud.in_(estado_salud))
        if habitat:
            query = query.filter(models.VistaControlAnimal.habitat.ilike(f"%{habitat}%"))
        if edad_min:
            query = query.filter(models.VistaControlAnimal.edad_aproximada >= edad_min)
        if edad_max:
            query = query.filter(models.VistaControlAnimal.edad_aproximada <= edad_max)
        if peso_min:
            query = query.filter(models.VistaControlAnimal.peso_actual >= peso_min)
        if peso_max:
            query = query.filter(models.VistaControlAnimal.peso_actual <= peso_max)
        if ultima_alimentacion_dias:
            fecha_limite = date.today() - timedelta(days=ultima_alimentacion_dias)
            query = query.filter(models.VistaControlAnimal.ultima_alimentacion_fecha <= fecha_limite)
        
        return query.all()

class ReporteConservacion:
    def generar(
        self,
        db: Session,
        estado_conservacion: list = None,
        cantidad_min: int = None,
        cantidad_max: int = None,
        esperanza_vida_min: int = None,
        esperanza_vida_max: int = None,
        cuidadores_min: int = None,
        veterinarios_min: int = None,
        habitat: str = None
    ):
        query = db.query(models.VistaConservacion)
        
        # Aplicar filtros
        if estado_conservacion:
            query = query.filter(models.VistaConservacion.estado_conservacion.in_(estado_conservacion))
        if cantidad_min:
            query = query.filter(models.VistaConservacion.cantidad_en_zoo >= cantidad_min)
        if cantidad_max:
            query = query.filter(models.VistaConservacion.cantidad_en_zoo <= cantidad_max)
        if esperanza_vida_min:
            query = query.filter(models.VistaConservacion.esperanza_vida >= esperanza_vida_min)
        if esperanza_vida_max:
            query = query.filter(models.VistaConservacion.esperanza_vida <= esperanza_vida_max)
        if cuidadores_min:
            query = query.filter(models.VistaConservacion.cuidadores_asignados >= cuidadores_min)
        if veterinarios_min:
            query = query.filter(models.VistaConservacion.veterinarios_especializados >= veterinarios_min)
        if habitat:
            query = query.filter(models.VistaConservacion.habitat_principal.ilike(f"%{habitat}%"))
        
        return query.all()

class ReporteFinanciero:
    def generar(
        self,
        db: Session,
        mes_inicio: str = None,
        mes_fin: str = None,
        ingresos_min: float = None,
        gastos_max: float = None,
        balance_min: float = None,
        ordenar_por: str = "mes",
        orden_desc: bool = False
    ):
        query = db.query(models.VistaFinancieraMensual)
        
        # Aplicar filtros
        if mes_inicio and mes_fin:
            query = query.filter(models.VistaFinancieraMensual.mes.between(mes_inicio, mes_fin))
        elif mes_inicio:
            query = query.filter(models.VistaFinancieraMensual.mes >= mes_inicio)
        elif mes_fin:
            query = query.filter(models.VistaFinancieraMensual.mes <= mes_fin)
            
        if ingresos_min:
            query = query.filter(models.VistaFinancieraMensual.ingresos_totales >= ingresos_min)
        if gastos_max:
            query = query.filter(models.VistaFinancieraMensual.gastos_totales <= gastos_max)
        if balance_min:
            query = query.filter(models.VistaFinancieraMensual.balance_mensual >= balance_min)
        
        # Ordenamiento
        if ordenar_por:
            columna = getattr(models.VistaFinancieraMensual, ordenar_por, None)
            if columna:
                if orden_desc:
                    columna = columna.desc()
                query = query.order_by(columna)
        
        return query.all()