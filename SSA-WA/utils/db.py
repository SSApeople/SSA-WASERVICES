from flask import jsonify
from decouple import config
from utils.Respuestas import Respuesta
from utils.getdbconnection import DBConnection

class Acceso:
    def __init__(self, Funcion=None, Params=None, db_type="sqlserver"):
        self.Funcion_ = Funcion
        self.Params_ = Params
        self.db_type = db_type
    
    def EjecutaVista(self, condiciones=None, instruccion=None, columnas=None, joins=None, settings=None):
        if settings:
            condiciones = settings.get("condiciones", condiciones)
            instruccion = settings.get("instruccion", instruccion)
            columnas = settings.get("columnas", columnas)
            joins = settings.get("joins", joins)
            self.Funcion_ = settings.get("Funcion_", getattr(self, "Funcion_", None))
            self.Params_ = settings.get("Params", getattr(self, "Params_", None))
            self.db_type = settings.get("db_type", getattr(self, "db_type", None))
        conn = DBConnection(self.db_type).get()
        try:
            cur = conn.cursor()
            values = []
            
            where_clause = self._construct_where_clause(condiciones, values)
            instruccion_clause = self._construct_instruction_clause(instruccion)
            columnas_seleccion = self._construct_columns_clause(columnas)
            join_clause = self._construct_joins_clause(joins)
            
            query = f'SELECT {instruccion_clause} {columnas_seleccion} FROM {self.Funcion_} {join_clause} {where_clause}'
            
            cur.execute(query, values)
            return self._fetch_results(cur)
        finally:
            cur.close()
            conn.close()
    
    def _construct_where_clause(self, condiciones, values):
        if not condiciones:
            return ""
        
        where_parts = []
        param_placeholder = "?" if self.db_type == "sqlserver" else "%s"
        
        for columna, (operador, valor) in condiciones.items():
            if operador.upper() in ['IN', 'NOT IN']:
                placeholders = ', '.join([param_placeholder] * len(valor))
                where_parts.append(f"{columna} {operador} ({placeholders})")
                values.extend(valor)
            else:
                where_parts.append(f"{columna} {operador} {param_placeholder}")
                values.append(valor)
        
        return "WHERE " + " AND ".join(where_parts)
    
    def _construct_instruction_clause(self, instruccion):
        agregados_permitidos = {"distinct", "sum", "max", "min", "len"}
        return instruccion.upper() if instruccion and instruccion.lower() in agregados_permitidos else ""
    
    def _construct_columns_clause(self, columnas):
        if not columnas:
            return "*"
        
        columnas_permitidas = {"sum", "max", "min", "len", "replace"}
        return ", ".join(
            f"{col[0].upper()}({col[1]})" if isinstance(col, tuple) and col[0].lower() in columnas_permitidas else col
            for col in columnas
        )
    
    def _construct_joins_clause(self, joins):
        if not joins:
            return ""
        
        join_types = {"INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "OUTER JOIN"}
        return " ".join(
            f"{join[0]} {join[1]} ON {join[2]}" for join in joins if isinstance(join, tuple) and join[0].upper() in join_types
        )
    
    def _fetch_results(self, cursor):
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    
    def EjecutaStoredProcedure(self, procedimiento, parametros=None):
        conn = DBConnection(self.db_type).get()
        try:
            cur = conn.cursor()
            
            if parametros:
                if self.db_type == "sqlserver":
                    placeholders = ', '.join(['?' for _ in parametros])  # Usa '?' en lugar de '%s'
                else:
                    placeholders = ', '.join(['%s'] * len(parametros))
            else:
                placeholders = ''
            
            if self.db_type == "sqlserver":
                query = f"EXEC {procedimiento} {placeholders}" if placeholders else f"EXEC {procedimiento}"
            elif self.db_type in {"mysql", "mariadb"}:
                query = f"CALL {procedimiento}({placeholders})" if placeholders else f"CALL {procedimiento}()"
            elif self.db_type == "postgres":
                query = f"SELECT * FROM {procedimiento}({placeholders})" if placeholders else f"SELECT * FROM {procedimiento}()"
            else:
                raise ValueError("Tipo de base de datos no soportado para procedimientos almacenados")

            cur.execute(query, parametros or [])  # Se pasan los parámetros correctamente
            return self._fetch_results(cur)
        finally:
            conn.commit()
            cur.close()
            conn.close()