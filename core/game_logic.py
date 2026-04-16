# core/game_logic.py
import random

class GameEngine:
    @staticmethod
    def ejecutar_accion(estado, accion):
        """
        Ejecuta una accion y actualiza el estado del jugador.
        Args: estado: objeto Estado, del modelo core.Estado)
              accion: objeto Accion, del modelo core.Accion)
        Returns: 
            dict: Resultado de la accion
        """

        if not estado.esta_vivo:
            return {
                "error": "El jugador ya esta muerto",
                "game_over": True
            }
        
        factor_aleatorio = random.uniform(0.75, 1.25)
        impacto_real = int(accion.impacto_base * factor_aleatorio)

        eventos = []

        if accion.tipo == 'explorar':
            estado.salud += impacto_real
            eventos.append(f" Exploraste: {impacto_real:+d} de salud")

            if random.random() < 0.25:
                comida = random.randint(5, 20)
                estado.hambre -= comida
                eventos.append(f" Encontraste comida -{comida} de hambre")
        
        elif accion.tipo == 'recolectar':
            estado.hambre += impacto_real
            eventos.append(f" Recolectaste: {impacto_real:+d} de hambre")
        
        elif accion.tipo == 'construir':  # Corregido: "construir" no "contruir"
            estado.salud += impacto_real
            eventos.append(f" Construiste un refugio: {impacto_real:+d} de salud")
        
        elif accion.tipo == 'descansar':
            estado.salud += impacto_real
            hambre_perdida = random.randint(5, 15)
            estado.hambre -= hambre_perdida
            eventos.append(f" Descansaste: {impacto_real:+d} salud, -{hambre_perdida} hambre")
        
        # EVENTOS ESPECIALES ALEATORIOS (30% de probabilidad)
        evento_especial = GameEngine._generar_evento_aleatorio()
        if evento_especial:
            estado.hambre += evento_especial['hambre']
            estado.salud += evento_especial['salud']
            eventos.append(evento_especial['mensaje'])
        
        # LIMITAR VALORES (0 a 100)
        estado.hambre = max(0, min(100, estado.hambre))
        estado.salud = max(0, min(100, estado.salud))
        
        # VERIFICAR MUERTE
        game_over = False
        mensaje_fin = None
        
        if estado.hambre <= 0:
            game_over = True
            estado.esta_vivo = False
            mensaje_fin = " ¡Moriste de hambre!"
        elif estado.salud <= 0:
            game_over = True
            estado.esta_vivo = False
            mensaje_fin = " ¡Moriste por las condiciones de la isla!"
        
        # AVANZAR DÍA (si sobrevive)
        if not game_over:
            estado.dia_actual += 1
            # Actualizar días sobrevividos en el usuario
            estado.usuario.dias_sobrevividos = estado.dia_actual - 1
            estado.usuario.save()
        
        # Guardar cambios
        estado.save()
        
        # RETORNAR RESULTADO
        return {
            "accion_realizada": accion.nombre,
            "impacto_base": accion.impacto_base,
            "impacto_real": impacto_real,
            "eventos": eventos,
            "estado_actual": {
                "dia": estado.dia_actual,
                "hambre": estado.hambre,
                "salud": estado.salud,
            },
            "game_over": game_over,
            "mensaje_fin": mensaje_fin
        }
    
    @staticmethod
    def _generar_evento_aleatorio():
        """Genera eventos especiales aleatorios (Bonificación)"""
        if random.random() < 0.3:  # 30% de probabilidad
            eventos_posibles = [
                {"hambre": -15, "salud": 0, "mensaje": "🥥 ¡Encontraste un cocotero! -15 hambre"},
                {"hambre": 10, "salud": -10, "mensaje": "🌊 ¡Una tormenta arrasó tu campamento! +10 hambre, -10 salud"},
                {"hambre": 0, "salud": 15, "mensaje": "🌿 ¡Encontraste plantas medicinales! +15 salud"},
                {"hambre": -8, "salud": -5, "mensaje": "🐗 ¡Un jabalí te robó comida! +8 hambre, -5 salud"},
                {"hambre": 0, "salud": -20, "mensaje": "🕷️ ¡Te picó una araña venenosa! -20 salud"},
                {"hambre": -20, "salud": 0, "mensaje": "🐟 ¡Atrapaste muchos peces! -20 hambre"},
                {"hambre": 5, "salud": -15, "mensaje": "🌋 ¡Erupción volcánica! +5 hambre, -15 salud"},
            ]
            return random.choice(eventos_posibles)
        return None