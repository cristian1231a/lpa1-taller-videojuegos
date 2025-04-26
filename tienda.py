# tienda.py
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
        self.click_realizado = False

        # Marca interna para Espada Cazadora de Demonios
        if not hasattr(self.jugador, 'has_demon_sword'):
            self.jugador.has_demon_sword = False

        # 📌 POSICIONAMIENTO DEL BOTÓN
        pos_x = ancho_pantalla - self.ancho - 20
        pos_y = (alto_pantalla // 2) - (self.alto // 2)
        self.rect = pygame.Rect(pos_x, pos_y, self.ancho, self.alto)

        # 🔢 LISTA DE ITEMS (clave, etiqueta, precio, nivel mínimo)
        self.items = [
            {"key": "chickeLive",  "label": "Muslo Pollo",                 "precio": 100,  "nivel_req": 2},
            {"key": "lvlUpSword1", "label": "Espada Cazadora de Demonios", "precio": 1300, "nivel_req": 7},
            {"key": "shield1",     "label": "Protección Básica",         "precio": 200,  "nivel_req": 3},
            {"key": "shield2",     "label": "Protección Avanzada",       "precio": 600,  "nivel_req": 5},
        ]

    def dibujar_boton(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)
        txt = self.fuente.render("TIENDA", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))
        txt2 = self.fuente.render("Presiona X", True, (255, 255, 255))
        screen.blit(txt2, (self.rect.centerx - txt2.get_width()/2, self.rect.bottom + 10))

    def dibujar_tienda(self, screen):
        if not self.mostrar:
            return
        t_rect = pygame.Rect(150, 100, 500, 300)
        pygame.draw.rect(screen, (80, 80, 120), t_rect)
        pygame.draw.rect(screen, (255, 255, 255), t_rect, 3)
        
        # Título
        title = self.fuente.render("TIENDA ABIERTA", True, (255,255,255))
        screen.blit(title, (t_rect.x + 20, t_rect.y + 20))

        # >>> Instrucción de uso del ratón --> Comprar <-- <<<
        hint = self.fuente.render("(Usa el MOUSE *Clic Izquierdo* para comprar en la tienda)", True, (255,255,255))
        screen.blit(hint, (t_rect.x + 20, t_rect.y + 50))
        
        # >>> Instrucción de uso del ratón --> Vender <-- <<<
        # Primera línea
        hint2a = self.fuente.render("Para vender un Muslo de Pollo del inventario:", True, (219,204,0))
        screen.blit(hint2a, (t_rect.centerx - hint2a.get_width()//2, t_rect.bottom - 50))

        # Segunda línea
        hint2b = self.fuente.render("Haz doble *Clic Izquierdo* en el slot del inventario", True, (219,204,0))
        screen.blit(hint2b, (t_rect.centerx - hint2b.get_width()//2, t_rect.bottom - 30))

        # Slots centrados
        slot_w, slot_h, esp = 100, 100, 20
        n = len(self.items)
        total_w = n*slot_w + (n-1)*esp
        start_x = t_rect.x + (t_rect.width - total_w)//2
        y0 = t_rect.y + 80

        coin = pygame.image.load("assets/img/scene/money/shuriken_money.png").convert_alpha()
        coin = pygame.transform.scale(coin, (16,16))
        mpos, mpress = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        for i, itm in enumerate(self.items):
            x = start_x + i*(slot_w+esp)
            s_rect = pygame.Rect(x, y0, slot_w, slot_h)

            # Verificar nivel
            nivel_actual = self.jugador.nivel_xp.nivel
            if nivel_actual >= itm['nivel_req']:
                bg_color = (132, 132, 132)
            else:
                bg_color = (60, 60, 60)
            pygame.draw.rect(screen, bg_color, s_rect)
            pygame.draw.rect(screen, (255,255,255), s_rect, 2)

            # Icono
            icon = pygame.image.load(f"assets/img/scene/items/{itm['key']}.png").convert_alpha()
            icon = pygame.transform.scale(icon, (64,64))
            screen.blit(icon, (x+18, y0+10))

            # Precio
            screen.blit(coin, (x+10, y0+75))
            ptxt = self.fuente.render(str(itm['precio']), True, (255,255,0))
            screen.blit(ptxt, (x+35, y0+75))

            # Nivel requerido si no cumple
            if nivel_actual < itm['nivel_req']:
                req_txt = self.fuente.render(f"Nivel req: {itm['nivel_req']}", True, (255,180,0))
                screen.blit(req_txt, (x + (slot_w - req_txt.get_width())//2, y0 + slot_h + 4))

            # Click único
            if s_rect.collidepoint(mpos):
                if mpress[0]:
                    if not self.click_realizado:
                        self.intentar_compra(itm)
                        self.click_realizado = True
                else:
                    self.click_realizado = False

    def intentar_compra(self, itm):
        j = self.jugador
        nivel_actual = j.nivel_xp.nivel
        key = itm['key']
        lbl = itm['label']
        precio = itm['precio']
        lvl_req = itm['nivel_req']

        # Nivel mínimo
        if nivel_actual < lvl_req:
            print(f"🔒 Necesitas ser nivel {lvl_req} para comprar '{lbl}'.")
            return

        # Shield1: prevenir si ya al máximo
        if key == 'shield1' and j.escudo >= j.escudo_max:
            print("⚠️ Tu escudo ya está al máximo. No es necesaria la recarga.")
            return

        # Shield2: prevenir si ya al máximo avanzado
        if key == 'shield2' and j.escudo_max >= 50 and j.escudo == j.escudo_max:
            print("⚠️ Tu escudo avanzado ya está al máximo.")
            return

        # Muslo de Pollo: inventario lleno
        if key == 'chickeLive' and len(j.inventario) >= 4:
            print("📦 Inventario lleno. No puedes comprar más Muslo de Pollo.")
            return

        # Espada demoníaca: recompra
        if key == 'lvlUpSword1' and j.has_demon_sword:
            print("⚔️ Ya tienes la Espada Cazadora de Demonios.")
            return

        # Fondos
        if j.dinero < precio:
            print(f"❌ No tienes suficientes monedas ({precio} req.) para '{lbl}'.")
            return

        # Deducción de dinero
        j.dinero -= precio

        # Lógica de compra
        if key == 'shield1':
            restore = 25 if j.escudo_max > 25 else j.escudo_max
            j.escudo = min(j.escudo + restore, j.escudo_max)
            print(f"🛡️ Escudo restaurado {restore} puntos ({j.escudo}/{j.escudo_max})")
            return

        if key == 'shield2':
            j.escudo_max = 50
            j.escudo = 50
            print("🛡️ Escudo Avanzado equipado y recargado al 100%.")
            return

        if key == 'chickeLive':
            poc = PocionVida(); poc.es_consumible = True
            j.inventario.append(poc)
            print("🍗 Muslo de Pollo añadida al inventario.")
            return

        if key == 'lvlUpSword1':
            j.attack_frames = [
                pygame.image.load(f"assets/img/player/attack2/Attack{i}.png").convert()
                for i in range(1, 6)
            ]
            j.has_demon_sword = True
            print("⚔️ Espada Cazadora de Demonios equipada. Tus ataques básicos dañarán a todo a su paso.")
            return
        
