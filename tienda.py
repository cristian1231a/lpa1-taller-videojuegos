import pygame

from billetera import Billetera

class Tienda:
    def __init__(self, ancho_pantalla, alto_pantalla, jugador):
        # 🧱 CONFIGURACIÓN INICIAL DEL BOTÓN
        self.ancho = 120
        self.alto = 40
        self.jugador = jugador
        self.mostrar = False
        self.fuente = pygame.font.Font(None, 24)

        # 📌 POSICIONAMIENTO EN EL LADO DERECHO CENTRADO VERTICALMENTE
        pos_x = ancho_pantalla - self.ancho - 20  # 20px desde el borde derecho
        pos_y = (alto_pantalla // 2) - (self.alto // 2)  # Centrado vertical

        self.rect = pygame.Rect(pos_x, pos_y, self.ancho, self.alto)
        self.fuente = pygame.font.SysFont("Arial", 20)
        self.mostrar = False

        

       


    def dibujar_boton(self, screen):
        # 🎨 DIBUJAR EL BOTÓN DE TIENDA EN PANTALLA
        pygame.draw.rect(screen, (50, 50, 50), self.rect)  # Fondo del botón
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)  # Borde
        texto = self.fuente.render("SHOP", True, (255, 255, 255))  # Texto del botón
        texto_rect = texto.get_rect(center=self.rect.center)
        screen.blit(texto, texto_rect)


        # Texto adicional debajo (Press H)
        texto_press_h = self.fuente.render("Press (H)", True, (255, 255, 255))  # Texto adicional
        texto_press_h_rect = texto_press_h.get_rect(center=(self.rect.centerx, self.rect.bottom + 10))  # Ajustar posición
        screen.blit(texto_press_h, texto_press_h_rect)

 

    def dibujar_tienda(self, screen):
        if self.mostrar:
            # 📦 DIMENSIONES DEL CUADRO DE TIENDA
            tienda_rect = pygame.Rect(150, 100, 500, 300)
            pygame.draw.rect(screen, (80, 80, 120), tienda_rect)  # Fondo
            pygame.draw.rect(screen, (255, 255, 255), tienda_rect, 3)  # Borde

            # 🛍️ TÍTULO
            texto = self.fuente.render("TIENDA ABIERTA", True, (255, 255, 255))
            screen.blit(texto, (tienda_rect.x + 20, tienda_rect.y + 20))

            # 🔢 DATOS DE LOS ITEMS
            nombres_items = ["chickeLive", "lvlUpSword1", "shield1", "shield2"]
            precios = [2, 3, 1, 4]

            # 💰 IMAGEN MONEDA
            imagen_moneda = pygame.image.load("assets/img/scene/money/shuriken_money.png").convert_alpha()
            imagen_moneda = pygame.transform.scale(imagen_moneda, (16, 16))  # Cambiar tamaño aquí

            # 📐 DIMENSIONES Y POSICIÓN DE LOS SLOTS
            slot_ancho = 100
            slot_alto = 100
            espacio_entre_slots = 20
            inicio_x = tienda_rect.x + 40
            y_slots = tienda_rect.y + 80

            # 🖱️ DETECCIÓN DE CLIC
            mouse_pressed = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            for i, nombre in enumerate(nombres_items):
                # 🔳 DIBUJAR SLOT
                slot_rect = pygame.Rect(inicio_x + i * (slot_ancho + espacio_entre_slots), y_slots, slot_ancho, slot_alto)
                pygame.draw.rect(screen, (200, 200, 200), slot_rect)  # Fondo slot
                pygame.draw.rect(screen, (255, 255, 255), slot_rect, 2)  # Borde slot

                # 🖼️ DIBUJAR IMAGEN DEL ITEM
                item_path = f"assets/img/scene/items/{nombre}.png"
                imagen_item = pygame.image.load(item_path).convert_alpha()
                imagen_item = pygame.transform.scale(imagen_item, (64, 64))
                screen.blit(imagen_item, (slot_rect.x + 18, slot_rect.y + 10))

                # 💰 DIBUJAR PRECIO CON MONEDA
                screen.blit(imagen_moneda, (slot_rect.x + 10, slot_rect.y + 75))
                precio_texto = self.fuente.render(str(precios[i]), True, (255, 255, 0))
                screen.blit(precio_texto, (slot_rect.x + 35, slot_rect.y + 75))

                # 🖱️ DETECTAR CLIC Y COMPRAR
                if slot_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
                    self.intentar_compra(nombre, precios[i])

            # ─ 🛈 Dibujar ícono de información visible y atractivo
                radio_info = 12
                centro_info = (slot_rect.centerx, slot_rect.top - 10)
                pygame.draw.circle(screen, (0, 150, 255), centro_info, radio_info)  # Fondo azul
                pygame.draw.circle(screen, (255, 255, 255), centro_info, radio_info, 2)  # Borde blanco

                fuente_info = pygame.font.SysFont("arial", 16, bold=True)
                info_text = fuente_info.render("i", True, (255, 255, 255))  # Texto blanco
                text_rect = info_text.get_rect(center=centro_info)
                screen.blit(info_text, text_rect)

                info_rect = pygame.Rect(centro_info[0] - radio_info, centro_info[1] - radio_info, radio_info * 2, radio_info * 2)


    def intentar_compra(self, nombre_item, precio):
        

        if self.jugador.dinero >= precio:
            self.jugador.dinero -= precio
            
            print(f"✅ Compraste: {nombre_item} por {precio} monedas")
            # Aquí podrías agregar el ítem al inventario si quieres
            # Verificar si el ítem es el escudo avanzado y actualizar
            if nombre_item == "shield2":
                if self.jugador.escudo_max < 50:  # Solo actualizar si no tienes ya el escudo avanzado
                    self.jugador.escudo_max = 50
                    self.jugador.escudo = 50
                    print("🛡️ Escudo avanzado equipado.")

                    # Verificar si el ítem es la espada mejorada (lvlUpSword1)
            elif nombre_item == "lvlUpSword1":
                # Cambiar la animación de ataque del jugador
                self.jugador.attack_frames = [
                    pygame.image.load(f"assets/img/player/attack2/Attack{i}.png").convert()
                    for i in range(1, 6)  # Se cambian las imágenes de 1 a 5
                ]
                print("⚔️ ¡Espada mejorada equipada! La animación de ataque ha cambiado.")


        else:
            print(f"❌ No tienes suficiente dinero para {nombre_item} (Precio: {precio}, Tienes: {self.jugador.dinero})")