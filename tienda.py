import pygame
from billetera import Billetera
from pocion_vida import PocionVida

class Tienda:
    def __init__(self, ancho_pantalla, alto_pantalla, jugador):
        # 🧱 CONFIGURACIÓN INICIAL DEL BOTÓN
        self.ancho = 120
        self.alto = 40
        self.jugador = jugador
        self.mostrar = False
        self.fuente = pygame.font.SysFont("Arial", 20)
        
        # Encargado de interpretar el mantener presionado el click izquierdo como una sola accion
        self.click_realizado = False 

        # Marca interna para Espada Cazadora de Demonios
        if not hasattr(self.jugador, 'has_demon_sword'):
            self.jugador.has_demon_sword = False

        # 📌 POSICIONAMIENTO DEL BOTÓN
        pos_x = ancho_pantalla - self.ancho - 20
        pos_y = (alto_pantalla // 2) - (self.alto // 2)
        self.rect = pygame.Rect(pos_x, pos_y, self.ancho, self.alto)

        # 🔢 LISTA DE ITEMS (clave y precio)
        self.items = [
            {"key": "chickeLive", "label": "Muslo Pollo", "precio": 100},
            {"key": "lvlUpSword1", "label": "Espada Cazadora de Demonios", "precio": 1300},
            {"key": "shield1", "label": "Proteccion Basica", "precio": 200},
            {"key": "shield2", "label": "Proteccion Avanzada", "precio": 600},
        ]

    def dibujar_boton(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        texto = self.fuente.render("TIENDA", True, (255, 255, 255))
        screen.blit(texto, texto.get_rect(center=self.rect.center))
        texto_press_x = self.fuente.render("Presiona X", True, (255, 255, 255))
        screen.blit(texto_press_x, (self.rect.centerx - texto_press_x.get_width()/2, self.rect.bottom + 10))

    def dibujar_tienda(self, screen):
        if not self.mostrar:
            return
        tienda_rect = pygame.Rect(150, 100, 500, 300)
        pygame.draw.rect(screen, (80, 80, 120), tienda_rect)
        pygame.draw.rect(screen, (255, 255, 255), tienda_rect, 3)
        texto = self.fuente.render("TIENDA ABIERTA", True, (255, 255, 255))
        screen.blit(texto, (tienda_rect.x + 20, tienda_rect.y + 20))

        # Cálculo centrado de slots
        slot_w, slot_h, espacio = 100, 100, 20
        num = len(self.items)
        total_w = num * slot_w + (num - 1) * espacio
        start_x = tienda_rect.x + (tienda_rect.width - total_w) // 2
        y_slots = tienda_rect.y + 80

        imagen_moneda = pygame.image.load("assets/img/scene/money/shuriken_money.png").convert_alpha()
        imagen_moneda = pygame.transform.scale(imagen_moneda, (16, 16))
        mouse_pos, mouse_pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        for i, item in enumerate(self.items):
            x = start_x + i * (slot_w + espacio)
            slot_rect = pygame.Rect(x, y_slots, slot_w, slot_h)
            pygame.draw.rect(screen, (200, 200, 200), slot_rect)
            pygame.draw.rect(screen, (255, 255, 255), slot_rect, 2)

            # Icono
            icon = pygame.image.load(f"assets/img/scene/items/{item['key']}.png").convert_alpha()
            icon = pygame.transform.scale(icon, (64, 64))
            screen.blit(icon, (x + 18, y_slots + 10))

            # Precio
            screen.blit(imagen_moneda, (x + 10, y_slots + 75))
            price_txt = self.fuente.render(str(item['precio']), True, (255, 255, 0))
            screen.blit(price_txt, (x + 35, y_slots + 75))

            # Clic de compra
            if slot_rect.collidepoint(mouse_pos):
                if mouse_pressed[0]:
                    if not self.click_realizado:
                        self.intentar_compra(item)
                        self.click_realizado = True
                else:
                    self.click_realizado = False

    def intentar_compra(self, item):
        key, label, precio = item['key'], item['label'], item['precio']
        j = self.jugador

        # Recarga de escudo básico
        if key == 'shield1':
            # Si tienes escudo avanzado, solo restaura 25 puntos; si básico, restaura completo
            if j.escudo < j.escudo_max:
                if j.dinero >= precio:
                    j.dinero -= precio
                    restore_amount = 25 if j.escudo_max > 25 else j.escudo_max
                    j.escudo = min(j.escudo + restore_amount, j.escudo_max)
                    print(f"🛡️ Escudo restaurado {restore_amount} puntos ({j.escudo}/{j.escudo_max})")
                else:
                    print(f"❌ No tienes dinero para recarga ({precio} requerido)")
            else:
                print("⚠️ Tu escudo ya está al máximo.")
            return

        # Espada de demonios solo una compra
        if key == 'lvlUpSword1' and j.has_demon_sword:
            print("⚔️ Ya tienes la Espada Cazadora de Demonios.")
            return

                # shield2 (Protección Avanzada): solo si no está ya lleno
        if key == 'shield2':
            if j.escudo_max >= 50 and j.escudo == j.escudo_max:
                print("⚠️ Tu escudo avanzado ya está al máximo. No es necesaria la compra.")
                return
            if j.dinero < precio:
                print(f"❌ No tienes dinero para {label} ({precio} req.)")
                return
            # Descuento y equipar/recargar
            j.dinero -= precio
            if j.escudo_max < 50:
                j.escudo_max = 50
            j.escudo = j.escudo_max
            print("🛡️ Escudo avanzado equipado/recargado.")
            return

        # Ahora sí verificamos fondos para el resto
        if j.dinero < precio:
            print(f"❌ No tienes suficiente dinero para {label} ({precio} req.)")
            return
        j.dinero -= precio
        print(f"✅ Compraste: {label} por {precio} monedas")

        # Poción: verificar espacio en inventario
        if key == 'chickeLive':
            if len(j.inventario) >= 4:
                print("📦 Inventario lleno. No puedes comprar más Pociones.")
                return

        if key == 'chickeLive':
            pocion = PocionVida()
            pocion.es_consumible = True
            j.inventario.append(pocion)
            print("🧪 Poción de vida añadida al inventario.")

        elif key == 'shield2':
            # Si ya tienes escudo avanzado y está al máximo, no compras
            if j.escudo_max >= 50 and j.escudo == j.escudo_max:
                print("⚠️ Tu escudo avanzado ya está al máximo. No es necesaria la compra.")
                return
            # Si no tienes aún escudo avanzado, lo equipas
            if j.escudo_max < 50:
                j.escudo_max = 50
            # En ambos casos (equipar o recargar) llevas escudo al máximo
            j.escudo = j.escudo_max
            print("🛡️ Escudo avanzado equipado/recargado.")
            return

        elif key == 'lvlUpSword1':
            j.attack_frames = [
                pygame.image.load(f"assets/img/player/attack2/Attack{i}.png").convert()
                for i in range(1, 6)
            ]
            j.has_demon_sword = True
            print("⚔️ Espada Cazadora de Demonios equipada. Tus ataques básicos dañarán a todo a su paso")
