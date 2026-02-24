import ipaddress
import os
import random
from collections import deque

# Funciones de validación
def validar_numero_positivo(mensaje):
    """
    Valida que la entrada sea un número entero positivo
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
                continue
            numero = int(entrada)
            if numero <= 0:
                print("❌ Error: El número debe ser mayor que 0.")
                continue
            return numero
        except ValueError:
            print("❌ Error: Debes introducir un número válido.")
            continue

def validar_numero(mensaje):
    """
    Valida que la entrada sea un número entero (puede ser 0 o negativo)
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
                continue
            return int(entrada)
        except ValueError:
            print("❌ Error: Debes introducir un número válido.")
            continue

def validar_si_no(mensaje):
    """
    Valida que la entrada sea sí o no
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
            continue
        if entrada.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif entrada.lower() in ['n', 'no']:
            return False
        else:
            print("❌ Error: Responde con 's' para sí o 'n' para no.")
            continue

def validar_ip(mensaje):
    """
    Valida que la entrada sea una IP válida
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
            continue
        try:
            ipaddress.IPv4Address(entrada)
            return entrada
        except ipaddress.AddressValueError:
            print("❌ Error: Introduce una dirección IP válida (ej: 192.168.1.0).")
            continue

def validar_mascara(mensaje):
    """
    Valida que la entrada sea una máscara válida
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
                continue
            mascara = int(entrada)
            if not (1 <= mascara <= 30):
                print("❌ Error: La máscara debe estar entre 1 y 30.")
                continue
            return mascara
        except ValueError:
            print("❌ Error: La máscara debe ser un número entre 1 y 30.")
            continue

def validar_area_ospf(mensaje):
    """
    Valida que la entrada sea un área OSPF válida
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
                continue
            area = int(entrada)
            if area < 0:
                print("❌ Error: El área OSPF debe ser un número mayor o igual a 0.")
                continue
            return str(area)
        except ValueError:
            print("❌ Error: El área OSPF debe ser un número válido.")
            continue

def validar_texto(mensaje):
    """
    Valida que la entrada no esté vacía
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print("❌ Error: No puedes dejar este campo vacío. Por favor, introduce un valor.")
            continue
        return entrada

def validar_nombre_archivo(mensaje):
    """
    Valida el nombre del archivo
    """
    while True:
        entrada = input(mensaje).strip()
        
        if not entrada:
            print("❌ Error: El nombre del archivo no puede estar vacío.")
            continue
            
        # Validar caracteres no permitidos en nombres de archivo
        caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        if any(char in entrada for char in caracteres_invalidos):
            print("❌ Error: El nombre del archivo contiene caracteres no válidos.")
            continue
            
        return entrada

def validar_vlan_id(mensaje, vlans_disponibles):
    """
    Valida que el ID de VLAN sea válido y esté disponible
    """
    while True:
        try:
            vlan_id = validar_numero_positivo(mensaje)
            
            if vlan_id < 2:
                print("❌ Error: Las VLANs deben empezar desde el número 2.")
                continue
                
            # Extraer solo los IDs de VLAN de la lista de tuplas (vlan_id, combos)
            vlan_ids_disponibles = [v[0] for v in vlans_disponibles]
            
            if vlan_id not in vlan_ids_disponibles:
                print(f"❌ Error: La VLAN {vlan_id} no está disponible. VLANs disponibles: {vlan_ids_disponibles}")
                continue
                
            return vlan_id
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

def validar_router_destino(mensaje, router_actual, num_routers, conexiones_registradas):
    """
    Valida que el router de destino sea válido
    Incluye validación de límite de interfaces del módulo NM-4E
    """
    while True:
        try:
            hacia_router = validar_numero_positivo(mensaje)
            
            if hacia_router == router_actual:
                print("❌ Error: No puedes conectar un router consigo mismo.")
                continue
                
            if hacia_router > num_routers or hacia_router < 1:
                print(f"❌ Error: El router debe estar entre 1 y {num_routers}.")
                continue
                
            if hacia_router in conexiones_registradas[router_actual]:
                print(f"❌ Error: Ya existe una conexión con el Router {hacia_router}.")
                continue
            
            # Validar límite de interfaces NM-4E para router actual
            if not validar_conexiones_nm4e(router_actual, conexiones_registradas[router_actual], nueva_conexion=hacia_router):
                continue
            
            # Validar límite de interfaces NM-4E para router destino
            if not validar_conexiones_nm4e(hacia_router, conexiones_registradas[hacia_router], nueva_conexion=router_actual):
                continue
                
            return hacia_router
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue

def validar_tipo_ruteo():
    """
    Valida el tipo de ruteo elegido por el usuario
    """
    while True:
        print(f"\n🔄 SELECCIÓN DE TIPO DE RUTEO")
        print("="*40)
        print("1. 🌐 OSPF (Open Shortest Path First)")
        print("2. 📍 Ruteo Estático")
        
        opcion = validar_numero("Selecciona el tipo de ruteo (1-2): ")
        
        if opcion == 1:
            return "ospf"
        elif opcion == 2:
            return "estatico"
        else:
            print("❌ Error: Selecciona 1 para OSPF o 2 para Ruteo Estático.")
            continue

# Función para convertir una dirección IP en un entero
def ip_to_int(ip):
    octetos = ip.split('.')
    return (int(octetos[0]) << 24) + (int(octetos[1]) << 16) + (int(octetos[2]) << 8) + int(octetos[3])

# Función para convertir un entero en una dirección IP
def int_to_ip(ip_int):
    return f'{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}'

# Función para calcular el rango de una subred dado un IP base y una máscara
# con saltos aleatorios de 1 a 5 subredes
def calcular_rango_subred(base_ip, mask, subredes_ocupadas, aleatorio=True):
    base_ip_int = ip_to_int(base_ip)
    mask_bits = (2 ** (32 - mask))  # Cantidad de direcciones en la subred
    
    # Redes candidatas para asignar
    redes_candidatas = []
    
    # Buscar subredes disponibles
    for i in range(1, 1000):  # Intentamos hasta un límite (por ejemplo 1000 redes)
        subnet_start = base_ip_int + i * mask_bits
        subnet_end = subnet_start + mask_bits - 1

        # Verificar si esta subred se solapa con las ocupadas
        rango_ocupado = False
        for ocupada in subredes_ocupadas:
            ocupada_inicio, ocupada_fin = ocupada
            if not (subnet_end < ocupada_inicio or subnet_start > ocupada_fin):
                rango_ocupado = True
                break
        
        if not rango_ocupado:
            # En modo aleatorio, almacenamos la red como candidata
            if aleatorio:
                redes_candidatas.append((subnet_start, subnet_end))
                # Buscamos hasta 10 redes candidatas (suficientes para saltar 1-5)
                if len(redes_candidatas) >= 10:
                    break
            else:
                # En modo no aleatorio, devolvemos la primera red disponible
                subredes_ocupadas.append((subnet_start, subnet_end))
                return (int_to_ip(subnet_start), int_to_ip(subnet_end))
    
    # Si no encontramos candidatas o no estamos en modo aleatorio
    if not redes_candidatas:
        return None
    
    # Seleccionar una red aleatoria con un salto de 1-5 desde el principio
    # (o la última disponible si no hay suficientes)
    salto = random.randint(1, min(5, len(redes_candidatas)))
    red_elegida = redes_candidatas[salto - 1]  # -1 porque los índices empiezan en 0
    
    # Marcar la red como ocupada
    subredes_ocupadas.append(red_elegida)
    
    return (int_to_ip(red_elegida[0]), int_to_ip(red_elegida[1]))

# Función para validar si una IP y máscara son correctas
def validar_ip_y_mascara(network, mask):
    try:
        ipaddress.IPv4Network(f"{network}/{mask}", strict=False)
        return True
    except ValueError:
        return False

# Función para obtener IP usable según el offset
def obtener_ip_usable(network, mask, offset):
    network_obj = ipaddress.IPv4Network(f"{network}/{mask}", strict=False)
    ips = list(network_obj.hosts())
    
    if offset == -1:  # Última IP usable
        return str(ips[-1])
    else:
        return str(ips[offset])

# Función para convertir máscara de prefijo a su representación decimal
def convertir_mascara(mask):
    return str(ipaddress.IPv4Network(f"0.0.0.0/{mask}").netmask)

# Función para convertir máscara decimal a wildcard
def convertir_a_wildcard(mascara_decimal):
    octetos = mascara_decimal.split('.')
    wildcard_octetos = []
    for octeto in octetos:
        wildcard_octeto = 255 - int(octeto)
        wildcard_octetos.append(str(wildcard_octeto))
    return '.'.join(wildcard_octetos)

# Función para configurar las redes entre routers (/30)
def configurar_redes_entre_routers(num_redes, base_ip, subredes_ocupadas, aleatorio=False):
    print(f"\nConfigurando {num_redes} redes entre routers (máscara /30):")
    redes_routers = []
    for _ in range(num_redes):
        combo = calcular_rango_subred(base_ip, 30, subredes_ocupadas, aleatorio)
        if combo:
            ip_inicio = combo[0]
            network = ipaddress.IPv4Network(f"{ip_inicio}/30", strict=False)
            redes_routers.append((str(network.network_address), 30))
        else:
            print("No hay más espacio para redes entre routers.")
            break
    return redes_routers

# Función para configurar combos de VLANs con asignación aleatoria
def configurar_vlans(num_vlans, base_ip, subredes_ocupadas):
    vlans = []
    
    # Tomamos por defecto que SÍ se usa asignación aleatoria para VLANs
    usar_aleatorio = True
    print("\n✅ Usando asignación aleatoria de subredes para VLANs.")
    
    for i in range(num_vlans):
        print(f"\n--- Configurando VLAN {i+2} ---")
        mask_vlan = validar_mascara(f'Introduce la máscara para la VLAN {i+2} (ej: 22, 23, etc.): ')
        num_combos = validar_numero_positivo(f'¿Cuántos combos necesitas para la VLAN {i+2}?: ')
        
        # Crear más combos para elegir si se usa modo aleatorio
        combos = []
        for _ in range(num_combos):
            combo = calcular_rango_subred(base_ip, mask_vlan, subredes_ocupadas, usar_aleatorio)
            if combo:
                ip_inicio = combo[0]
                network = ipaddress.IPv4Network(f"{ip_inicio}/{mask_vlan}", strict=False)
                combos.append((str(network.network_address), mask_vlan))
            else:
                print(f"❌ No hay más espacio para combos en la VLAN {i+2}.")
                break
        
        vlans.append((i+2, combos))  # Guardar número de VLAN y sus combos
    
    return vlans

# ============================================================================
# FUNCIONES PARA RUTEO ESTÁTICO
# ============================================================================

def construir_grafo_topologia(conexiones_mapa, num_routers):
    """
    Construye un grafo de la topología de routers basado en las conexiones
    """
    grafo = {i: [] for i in range(1, num_routers + 1)}
    
    for (r1, r2), (network, mask) in conexiones_mapa.items():
        grafo[r1].append(r2)
        grafo[r2].append(r1)
    
    return grafo

def encontrar_camino_mas_corto(grafo, origen, destino):
    """
    Encuentra el camino más corto entre dos routers usando BFS
    Retorna una lista con el camino [origen, intermedio, ..., destino]
    """
    if origen == destino:
        return [origen]
    
    queue = deque([(origen, [origen])])
    visitados = set([origen])
    
    while queue:
        router_actual, camino = queue.popleft()
        
        for vecino in grafo[router_actual]:
            if vecino == destino:
                return camino + [vecino]
            
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append((vecino, camino + [vecino]))
    
    return None  # No hay camino

def obtener_ip_conexion_entre_routers(router1, router2, conexiones_mapa, es_primer_router_dict):
    """
    Obtiene la IP de la interfaz de router1 hacia router2
    """
    conexion_key = tuple(sorted([router1, router2]))
    if conexion_key not in conexiones_mapa:
        return None
    
    network, mask = conexiones_mapa[conexion_key]
    
    # Determinar si router1 es el "primer router" en esta conexión
    es_primer_router = es_primer_router_dict.get(router1, {}).get(router2, router1 < router2)
    
    # Obtener la IP correspondiente
    ip_offset = 0 if es_primer_router else -1
    ip_router1 = obtener_ip_usable(network, mask, ip_offset)
    
    return ip_router1

def calcular_rutas_estaticas(conexiones_mapa, router_vlans_asignadas, num_routers, routers_con_swc3, swc3_configuraciones):
    """
    Calcula automáticamente todas las rutas estáticas necesarias para cada router
    """
    print(f"\n🔄 CALCULANDO RUTAS ESTÁTICAS AUTOMÁTICAMENTE...")
    print("="*50)
    
    # Construir grafo de topología
    grafo = construir_grafo_topologia(conexiones_mapa, num_routers)
    
    # Diccionario para guardar si un router es el "primer router" en cada conexión
    es_primer_router_dict = {}
    for router_num in range(1, num_routers + 1):
        es_primer_router_dict[router_num] = {}
        for (r1, r2), _ in conexiones_mapa.items():
            if router_num in (r1, r2):
                otro_router = r2 if r1 == router_num else r1
                es_primer_router_dict[router_num][otro_router] = (r1, r2)[0] == router_num
    
    rutas_estaticas = {}
    
    for router_origen in range(1, num_routers + 1):
        rutas_estaticas[router_origen] = []
        
        print(f"🖥️ Calculando rutas para Router {router_origen}...")
        
        # CORRECCIÓN: Agregar rutas hacia las propias VLANs si el router tiene SWC3
        if router_origen in swc3_configuraciones:
            swc3_config = swc3_configuraciones[router_origen]
            swc3_ip = swc3_config['ip_hacia_router']  # IP del SWC3
            
            print(f"   📡 Router {router_origen} tiene SWC3 - agregando rutas hacia VLANs propias")
            
            # Agregar rutas hacia las VLANs propias del router
            if router_origen in router_vlans_asignadas:
                for vlan_id, (network, mask) in router_vlans_asignadas[router_origen].items():
                    mascara_decimal = convertir_mascara(mask)
                    rutas_estaticas[router_origen].append({
                        'red': network,
                        'mascara': mascara_decimal,
                        'next_hop': swc3_ip,
                        'descripcion': f"VLAN {vlan_id} propia via SWC3_R{router_origen}"
                    })
                    print(f"      ✓ Ruta agregada: {network}/{mask} via {swc3_ip}")
        
        # Para cada otro router, calcular rutas a sus redes
        for router_destino in range(1, num_routers + 1):
            if router_origen == router_destino:
                continue
            
            # Encontrar camino más corto
            camino = encontrar_camino_mas_corto(grafo, router_origen, router_destino)
            
            if camino is None or len(camino) < 2:
                print(f"   ⚠️ No hay camino al Router {router_destino}")
                continue
            
            # El next-hop es el segundo router en el camino
            next_hop_router = camino[1]
            
            # Obtener IP del next-hop
            next_hop_ip = obtener_ip_conexion_entre_routers(
                next_hop_router, router_origen, conexiones_mapa, es_primer_router_dict
            )
            
            if next_hop_ip is None:
                print(f"   ❌ No se pudo obtener IP del next-hop hacia Router {router_destino}")
                continue
            
            # Agregar ruta a la red administrativa del router destino
            red_admin = f"192.168.{router_destino}.0"
            mascara_admin = "255.255.255.0"
            rutas_estaticas[router_origen].append({
                'red': red_admin,
                'mascara': mascara_admin,
                'next_hop': next_hop_ip,
                'descripcion': f"Red administrativa Router {router_destino}"
            })
            
            # Agregar rutas a las VLANs del router destino
            if router_destino in router_vlans_asignadas:
                for vlan_id, (network, mask) in router_vlans_asignadas[router_destino].items():
                    mascara_decimal = convertir_mascara(mask)
                    rutas_estaticas[router_origen].append({
                        'red': network,
                        'mascara': mascara_decimal,
                        'next_hop': next_hop_ip,
                        'descripcion': f"VLAN {vlan_id} de Router {router_destino}"
                    })
            
            # Agregar rutas hacia redes de SWC3 del router destino
            if router_destino in swc3_configuraciones:
                swc3_config = swc3_configuraciones[router_destino]
                # Ruta hacia la red administrativa del SWC3
                rutas_estaticas[router_origen].append({
                    'red': f"192.168.{router_destino}.0",
                    'mascara': "255.255.255.0", 
                    'next_hop': next_hop_ip,
                    'descripcion': f"Red administrativa SWC3_R{router_destino}"
                })
        
        # Agregar rutas hacia redes /30 Router-SWC3 (solo si no es directamente conectado)
        for router_swc3, swc3_config in swc3_configuraciones.items():
            if router_origen != router_swc3:
                # Encontrar camino hacia el router que tiene el SWC3
                camino = encontrar_camino_mas_corto(grafo, router_origen, router_swc3)
                
                if camino and len(camino) >= 2:
                    next_hop_router = camino[1]
                    next_hop_ip = obtener_ip_conexion_entre_routers(
                        next_hop_router, router_origen, conexiones_mapa, es_primer_router_dict
                    )
                    
                    if next_hop_ip:
                        # Ruta hacia la red /30 entre Router y SWC3
                        network_router_swc3, mask_router_swc3 = swc3_config['red_conexion']
                        mascara_decimal = convertir_mascara(mask_router_swc3)
                        rutas_estaticas[router_origen].append({
                            'red': network_router_swc3,
                            'mascara': mascara_decimal,
                            'next_hop': next_hop_ip,
                            'descripcion': f"Red /30 entre Router {router_swc3} y SWC3_R{router_swc3}"
                        })
        
        # Agregar rutas a redes /30 entre routers (solo las que no están directamente conectadas)
        for (r1, r2), (network_30, mask_30) in conexiones_mapa.items():
            # Si este router no está en la conexión /30, necesita una ruta para alcanzarla
            if router_origen not in (r1, r2):
                # Encontrar camino a cualquiera de los dos routers de la conexión
                camino_r1 = encontrar_camino_mas_corto(grafo, router_origen, r1)
                camino_r2 = encontrar_camino_mas_corto(grafo, router_origen, r2)
                
                # Elegir el camino más corto
                if camino_r1 and camino_r2:
                    camino = camino_r1 if len(camino_r1) <= len(camino_r2) else camino_r2
                elif camino_r1:
                    camino = camino_r1
                elif camino_r2:
                    camino = camino_r2
                else:
                    continue
                
                if len(camino) >= 2:
                    next_hop_router = camino[1]
                    next_hop_ip = obtener_ip_conexion_entre_routers(
                        next_hop_router, router_origen, conexiones_mapa, es_primer_router_dict
                    )
                    
                    if next_hop_ip:
                        mascara_30_decimal = convertir_mascara(mask_30)
                        rutas_estaticas[router_origen].append({
                            'red': network_30,
                            'mascara': mascara_30_decimal,
                            'next_hop': next_hop_ip,
                            'descripcion': f"Red /30 entre Router {r1} y Router {r2}"
                        })
        
        print(f"   ✅ {len(rutas_estaticas[router_origen])} rutas calculadas")
    
    # Calcular rutas estáticas específicas para cada SWC3
    rutas_estaticas_swc3 = {}
    
    for router_swc3, tiene_swc3 in routers_con_swc3.items():
        if not tiene_swc3:  # Solo procesar routers que SÍ tienen SWC3
            continue
            
        rutas_estaticas_swc3[router_swc3] = []
        swc3_config = swc3_configuraciones[router_swc3]
        router_ip = obtener_ip_usable(swc3_config['red_conexion'][0], swc3_config['red_conexion'][1], 0)  # IP del router
        
        print(f"🔧 Calculando rutas para SWC3_R{router_swc3}...")
        
        # Para cada otro router, calcular rutas a sus redes
        for router_destino in range(1, num_routers + 1):
            if router_swc3 == router_destino:
                continue
            
            # Todas las rutas del SWC3 van via su router asociado
            next_hop_ip = router_ip
            
            # Agregar ruta a la red administrativa del router destino
            red_admin = f"192.168.{router_destino}.0"
            mascara_admin = "255.255.255.0"
            rutas_estaticas_swc3[router_swc3].append({
                'red': red_admin,
                'mascara': mascara_admin,
                'next_hop': next_hop_ip,
                'descripcion': f"Red administrativa Router {router_destino}"
            })
            
            # Agregar rutas a las VLANs del router destino
            if router_destino in router_vlans_asignadas:
                for vlan_id, (network, mask) in router_vlans_asignadas[router_destino].items():
                    mascara_decimal = convertir_mascara(mask)
                    rutas_estaticas_swc3[router_swc3].append({
                        'red': network,
                        'mascara': mascara_decimal,
                        'next_hop': next_hop_ip,
                        'descripcion': f"VLAN {vlan_id} de Router {router_destino}"
                    })
        
        # Agregar rutas hacia redes /30 entre routers (todas via router asociado)
        for (r1, r2), (network_30, mask_30) in conexiones_mapa.items():
            if router_swc3 not in (r1, r2):  # Si el SWC3 no está en la conexión
                mascara_30_decimal = convertir_mascara(mask_30)
                rutas_estaticas_swc3[router_swc3].append({
                    'red': network_30,
                    'mascara': mascara_30_decimal,
                    'next_hop': router_ip,
                    'descripcion': f"Red /30 entre Router {r1} y Router {r2}"
                })
        
        # Agregar rutas hacia otras redes /30 Router-SWC3
        for router_otro_swc3, otro_swc3_config in swc3_configuraciones.items():
            if router_swc3 != router_otro_swc3:
                network_router_swc3, mask_router_swc3 = otro_swc3_config['red_conexion']
                mascara_decimal = convertir_mascara(mask_router_swc3)
                rutas_estaticas_swc3[router_swc3].append({
                    'red': network_router_swc3,
                    'mascara': mascara_decimal,
                    'next_hop': router_ip,
                    'descripcion': f"Red /30 entre Router {router_otro_swc3} y SWC3_R{router_otro_swc3}"
                })
        
        print(f"   ✅ {len(rutas_estaticas_swc3[router_swc3])} rutas calculadas para SWC3_R{router_swc3}")
    
    print("✅ Cálculo de rutas estáticas completado\n")
    return rutas_estaticas, rutas_estaticas_swc3

def generar_comandos_rutas_estaticas(rutas_estaticas):
    """
    Genera los comandos de configuración para rutas estáticas
    """
    comandos = []
    
    if not rutas_estaticas:
        return comandos
    
    comandos.append("! -- CONFIGURACIÓN DE RUTAS ESTÁTICAS --")
    
    for ruta in rutas_estaticas:
        red = ruta['red']
        mascara = ruta['mascara']
        next_hop = ruta['next_hop']
        descripcion = ruta['descripcion']
        
        comandos.append(f"! {descripcion}")
        comandos.append(f"ip route {red} {mascara} {next_hop}")
    
    return comandos

# ============================================================================

# Función para generar comandos de configuración de interfaz
def configurar_interface(interface, ip, mascara):
    return [
        f"int {interface}",
        f"ip add {ip} {mascara}",
        "no shut"
    ]

# Función para generar comandos de configuración de switch
def generar_comandos_switch(router_num, todas_vlans):
    comandos = [
        "en",
        "conf t",
        f"hostname SWITCH{router_num}",
        "ip domain-name cisco",
        "crypto key generate rsa general-keys modulus 512",
        "line vty 0 5",
        "transport input ssh",
        "login local",
        "exit",
        "username admin privilege 15 password cisco",
        "enable secret cisco"
    ]
    
    # Comandos para crear VLANs
    for vlan_id, _ in todas_vlans:
        vlan_name = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez"}.get(vlan_id, f"vlan{vlan_id}")
        comandos.append(f"VLAN {vlan_id}")
        comandos.append(f"name {vlan_name}")
    
    # Configuraciones de puertos
    comandos.extend([
        "int fa0/1",
        "switchport mode trunk",
        "int fa0/2",
        "switchport mode access",
        "switchport access vlan " if len(todas_vlans) >= 2 else "switchport access vlan 2",
        "int fa0/3",
        "switchport mode access",
        "switchport access vlan " if len(todas_vlans) >= 2 else "switchport access vlan 2",
        "int fa0/4",
        "switchport mode access",
        "switchport access vlan ",
        "exit"
    ])
    
    # Configurar IP administrativa
    comandos.extend([
        "int vlan 1",
        f"ip add 192.168.{router_num}.2 255.255.255.0",
        "no shut"
    ])
    
    return comandos

# Función para generar comandos para un router, incluyendo OSPF o Ruteo Estático
def generar_comandos_router(router_num, vlans_asignadas, conexiones_routers, area_ospf, conexiones_ospf, router_id, tipo_ruteo="ospf", rutas_estaticas=None):
    # Configuración básica con SSH y seguridad
    comandos = [
        "en", 
        "conf t", 
        f"hostname Router{router_num}",
        "ip domain-name cisco",
        "crypto key generate rsa general-keys modulus 512",
        "line vty 0 5",
        "transport input ssh",
        "login local",
        "exit",
        "username admin privilege 15 password cisco",
        "enable secret cisco",
        "int fa0/0", 
        "no shut",
        "int fa0/0.1",
        "encapsulation dot1Q 1",
        f"ip add 192.168.{router_num}.1 255.255.255.0"
    ]

    # Comandos por VLAN
    for vlan_num, (network, mask) in vlans_asignadas.items():
        ip_usable = obtener_ip_usable(network, mask, -1)  # Última IP usable
        mascara_decimal = convertir_mascara(mask)
        comandos.append(f"int fa0/0.{vlan_num}")
        comandos.append(f"encapsulation dot1Q {vlan_num}")
        comandos.append(f"ip add {ip_usable} {mascara_decimal}")
        comandos.append("no shut")

    # Comandos para conexiones entre routers - Usando interfaces del módulo NM-4E
    conexiones_ordenadas = sorted(conexiones_routers.items(), key=lambda x: x[0])
    for idx, (hacia_router, (network, mask, es_primer_router)) in enumerate(conexiones_ordenadas):
        interface = f"Ethernet1/{idx}"  # Usar interfaces del módulo NM-4E: Ethernet1/0, Ethernet1/1, etc.
        # Si este router es el "primer router" en la conexión, usa primera IP usable, sino usa la última
        ip_offset = 0 if es_primer_router else -1
        ip_usable = obtener_ip_usable(network, mask, ip_offset)
        mascara_decimal = convertir_mascara(mask)
        comandos.extend(configurar_interface(interface, ip_usable, mascara_decimal))

    # Comandos DHCP para cada VLAN
    for vlan_num, (network, mask) in vlans_asignadas.items():
        default_router_ip = obtener_ip_usable(network, mask, -1)  # Última IP usable
        mascara_decimal = convertir_mascara(mask)
        comandos.extend([
            f"ip dhcp pool {vlan_num}",
            f"default-router {default_router_ip}",
            f"network {network} {mascara_decimal}"
        ])

    # Configuración de ruteo según el tipo elegido
    if tipo_ruteo == "ospf":
        # Configuración OSPF
        comandos.append(f"router ospf 1")
        comandos.append(f"router-id {router_id}")
        
        # Agregar la VLAN administrativa (VLAN 1) al área OSPF
        comandos.append(f"network 192.168.{router_num}.0 0.0.0.255 area {area_ospf}")
        
        # Agregar redes de VLANs al área del router
        for vlan_num, (network, mask) in vlans_asignadas.items():
            wildcard = convertir_a_wildcard(convertir_mascara(mask))
            comandos.append(f"network {network} {wildcard} area {area_ospf}")
        
        # Agregar redes entre routers al área correspondiente - Ordenados
        conexiones_ospf_ordenadas = sorted(conexiones_ospf.items(), key=lambda x: x[0])
        for hacia_router, (network, mask, es_primer_router, area) in conexiones_ospf_ordenadas:
            wildcard = convertir_a_wildcard(convertir_mascara(mask))
            comandos.append(f"network {network} {wildcard} area {area}")
    
    elif tipo_ruteo == "estatico":
        # Configuración de rutas estáticas
        if rutas_estaticas:
            comandos_rutas = generar_comandos_rutas_estaticas(rutas_estaticas)
            comandos.extend(comandos_rutas)

    return comandos

# Función para generar un router-id según el área y contador
def generar_router_id(area, contador):
    # Convertir el área a un número entero y sumar 1
    area_num = int(area) + 1
    return f"{area_num}.{area_num}.{area_num}.{contador}"

# Función para detectar conexiones ya configuradas para un router
def detectar_conexiones_previas(router_actual, conexiones_mapa, areas_ospf, configuracion_orden):
    conexiones_previas = {}
    conexiones_ospf_previas = {}
    
    # Buscar todas las conexiones donde este router está involucrado
    for conexion_key, (network, mask) in conexiones_mapa.items():
        r1, r2 = conexion_key
        
        # Si este router es parte de la conexión
        if router_actual in conexion_key:
            # El otro router en la conexión
            otro_router = r2 if r1 == router_actual else r1
            
            # Si el otro router ya fue configurado
            if otro_router in configuracion_orden:
                # Determinar si este router es el "primer router" en la conexión
                es_primer_router = conexion_key[0] == router_actual
                
                # Determinar el área de la conexión (la del router ya configurado)
                area_red = areas_ospf[otro_router]
                
                # Guardar la conexión
                conexiones_previas[otro_router] = (network, mask, es_primer_router)
                conexiones_ospf_previas[otro_router] = (network, mask, es_primer_router, area_red)
    
    return conexiones_previas, conexiones_ospf_previas

# Funciones para modificar la configuración del router
def mostrar_configuracion_router(router_num, vlans_router, conexiones_router):
    """
    Muestra la configuración actual del router
    """
    print(f"\n📋 CONFIGURACIÓN ACTUAL DEL ROUTER {router_num}:")
    print("="*50)
    
    # Mostrar VLANs
    if vlans_router:
        print("🏷️ VLANs configuradas:")
        for vlan_id, (network, mask) in vlans_router.items():
            print(f"   VLAN {vlan_id}: {network}/{mask}")
    else:
        print("🏷️ VLANs: Ninguna configurada")
    
    # Mostrar conexiones
    if conexiones_router:
        print("\n🔗 Conexiones configuradas:")
        for hacia_router, (network, mask, es_primer_router) in conexiones_router.items():
            ip_offset = 0 if es_primer_router else -1
            ip_usable = obtener_ip_usable(network, mask, ip_offset)
            print(f"   Router {router_num} ↔ Router {hacia_router}: {network}/{mask} (IP: {ip_usable})")
    else:
        print("🔗 Conexiones: Ninguna configurada")

def modificar_vlans_router(router_num, vlans_router, vlans_combos, router_vlans_asignadas):
    """
    Permite modificar las VLANs del router actual
    """
    while True:
        print(f"\n🔧 MODIFICAR VLANs DEL ROUTER {router_num}")
        print("="*40)
        print("1. ➕ Agregar VLAN")
        print("2. ➖ Quitar VLAN")
        print("3. 👁️ Ver VLANs actuales")
        print("4. ✅ Terminar modificación")
        
        opcion = validar_numero("Selecciona una opción (1-4): ")
        
        if opcion == 1:  # Agregar VLAN
            print("\n--- Agregando nueva VLAN ---")
            vlan_id = validar_vlan_id(f"Número de VLAN a agregar: ", vlans_combos)
            
            # Verificar si ya está asignada a este router
            if vlan_id in vlans_router:
                print(f"❌ La VLAN {vlan_id} ya está asignada a este router.")
                continue
            
            # Buscar un combo disponible
            for v_id, combos in vlans_combos:
                if v_id == vlan_id:
                    combo_usado = False
                    for network, mask in combos:
                        # Verificar si está asignado a otros routers
                        combo_asignado = False
                        for r, router_vlans in router_vlans_asignadas.items():
                            if r != router_num and (network, mask) in router_vlans.values():
                                combo_asignado = True
                                break
                        
                        if not combo_asignado:
                            vlans_router[vlan_id] = (network, mask)
                            combo_usado = True
                            print(f"✅ VLAN {vlan_id} agregada: {network}/{mask}")
                            break
                    
                    if not combo_usado:
                        print(f"❌ No hay combos disponibles para la VLAN {vlan_id}")
                    break
                    
        elif opcion == 2:  # Quitar VLAN
            if not vlans_router:
                print("❌ No hay VLANs configuradas para quitar.")
                continue
                
            print("\n--- Quitando VLAN ---")
            print("VLANs actuales:")
            for vlan_id in vlans_router.keys():
                print(f"  - VLAN {vlan_id}")
            
            vlan_a_quitar = validar_numero_positivo("Número de VLAN a quitar: ")
            
            if vlan_a_quitar in vlans_router:
                network, mask = vlans_router[vlan_a_quitar]
                del vlans_router[vlan_a_quitar]
                print(f"✅ VLAN {vlan_a_quitar} eliminada ({network}/{mask})")
            else:
                print(f"❌ La VLAN {vlan_a_quitar} no está configurada en este router.")
                
        elif opcion == 3:  # Ver VLANs actuales
            if vlans_router:
                print("\n🏷️ VLANs actuales:")
                for vlan_id, (network, mask) in vlans_router.items():
                    print(f"   VLAN {vlan_id}: {network}/{mask}")
            else:
                print("🏷️ No hay VLANs configuradas.")
                
        elif opcion == 4:  # Terminar
            break
        else:
            print("❌ Opción no válida. Selecciona 1, 2, 3 o 4.")

def modificar_conexiones_router(router_num, conexiones_router, conexiones_ospf, num_routers, 
                              conexiones_registradas, redes_routers, conexiones_mapa, area_ospf):
    """
    Permite modificar las conexiones del router actual
    """
    while True:
        print(f"\n🔧 MODIFICAR CONEXIONES DEL ROUTER {router_num}")
        print("="*45)
        print("1. ➕ Agregar conexión")
        print("2. ➖ Quitar conexión")
        print("3. 👁️ Ver conexiones actuales")
        print("4. ✅ Terminar modificación")
        
        opcion = validar_numero("Selecciona una opción (1-4): ")
        
        if opcion == 1:  # Agregar conexión
            # Mostrar routers disponibles
            routers_disponibles = [i for i in range(1, num_routers + 1) 
                                  if i != router_num and i not in conexiones_registradas[router_num]]
            
            if not routers_disponibles:
                print("❌ No hay routers disponibles para nuevas conexiones.")
                continue
                
            print(f"\n--- Agregando nueva conexión ---")
            print(f"🖥️ Routers disponibles: {routers_disponibles}")
            hacia_router = validar_router_destino(f"¿Hacia qué router crear la conexión?: ", 
                                                router_num, num_routers, conexiones_registradas)
            
            # Asignar una red de la lista de redes entre routers
            if redes_routers:
                network, mask = redes_routers.pop(0)
                conexion_key = tuple(sorted([router_num, hacia_router]))
                conexiones_mapa[conexion_key] = (network, mask)
                
                # Si este router tiene el número más bajo, es el "primer router"
                es_primer_router = router_num < hacia_router
                area_red = area_ospf
                
                # Guardar información sobre la conexión
                conexiones_router[hacia_router] = (network, mask, es_primer_router)
                conexiones_ospf[hacia_router] = (network, mask, es_primer_router, area_red)
                
                # Registrar esta conexión
                conexiones_registradas[router_num].append(hacia_router)
                
                # Mostrar la asignación de IPs
                ip_primer_router = obtener_ip_usable(network, mask, 0)
                ip_segundo_router = obtener_ip_usable(network, mask, -1)
                mascara_decimal = convertir_mascara(mask)
                
                if es_primer_router:
                    print(f"✅ Conexión agregada:")
                    print(f"   Router {router_num}: {ip_primer_router} ({mascara_decimal})")
                    print(f"   Router {hacia_router}: {ip_segundo_router} ({mascara_decimal})")
                else:
                    print(f"✅ Conexión agregada:")
                    print(f"   Router {router_num}: {ip_segundo_router} ({mascara_decimal})")
                    print(f"   Router {hacia_router}: {ip_primer_router} ({mascara_decimal})")
            else:
                print("❌ No hay más redes /30 disponibles para conexiones.")
                
        elif opcion == 2:  # Quitar conexión
            if not conexiones_router:
                print("❌ No hay conexiones configuradas para quitar.")
                continue
                
            print("\n--- Quitando conexión ---")
            print("Conexiones actuales:")
            for hacia_router in conexiones_router.keys():
                print(f"  - Conexión con Router {hacia_router}")
            
            router_a_desconectar = validar_numero_positivo("Número del router a desconectar: ")
            
            if router_a_desconectar in conexiones_router:
                # Obtener información de la conexión
                network, mask, es_primer_router = conexiones_router[router_a_desconectar]
                
                # Eliminar de todas las estructuras
                del conexiones_router[router_a_desconectar]
                if router_a_desconectar in conexiones_ospf:
                    del conexiones_ospf[router_a_desconectar]
                
                # Quitar de conexiones registradas
                if router_a_desconectar in conexiones_registradas[router_num]:
                    conexiones_registradas[router_num].remove(router_a_desconectar)
                
                # Devolver la red a la lista de disponibles
                redes_routers.append((network, mask))
                
                # Eliminar del mapa de conexiones
                conexion_key = tuple(sorted([router_num, router_a_desconectar]))
                if conexion_key in conexiones_mapa:
                    del conexiones_mapa[conexion_key]
                
                print(f"✅ Conexión con Router {router_a_desconectar} eliminada ({network}/{mask})")
            else:
                print(f"❌ No hay conexión configurada con Router {router_a_desconectar}.")
                
        elif opcion == 3:  # Ver conexiones actuales
            if conexiones_router:
                print("\n🔗 Conexiones actuales:")
                for hacia_router, (network, mask, es_primer_router) in conexiones_router.items():
                    ip_offset = 0 if es_primer_router else -1
                    ip_usable = obtener_ip_usable(network, mask, ip_offset)
                    print(f"   Router {router_num} ↔ Router {hacia_router}: {network}/{mask} (IP: {ip_usable})")
            else:
                print("🔗 No hay conexiones configuradas.")
                
        elif opcion == 4:  # Terminar
            break
        else:
            print("❌ Opción no válida. Selecciona 1, 2, 3 o 4.")

def confirmar_o_modificar_router(router_num, vlans_router, conexiones_router, conexiones_ospf, 
                               vlans_combos, router_vlans_asignadas, num_routers, 
                               conexiones_registradas, redes_routers, conexiones_mapa, area_ospf):
    """
    Permite al usuario confirmar o modificar la configuración del router actual
    """
    while True:
        # Mostrar configuración actual
        mostrar_configuracion_router(router_num, vlans_router, conexiones_router)
        
        print(f"\n🤔 ¿La configuración del Router {router_num} es correcta?")
        print("1. ✅ Sí, continuar")
        print("2. 🏷️ Modificar VLANs")
        print("3. 🔗 Modificar conexiones")
        print("4. 👁️ Ver configuración nuevamente")
        
        opcion = validar_numero("Selecciona una opción (1-4): ")
        
        if opcion == 1:  # Confirmar y continuar
            print(f"✅ Router {router_num} confirmado.")
            break
        elif opcion == 2:  # Modificar VLANs
            modificar_vlans_router(router_num, vlans_router, vlans_combos, router_vlans_asignadas)
        elif opcion == 3:  # Modificar conexiones
            modificar_conexiones_router(router_num, conexiones_router, conexiones_ospf, 
                                      num_routers, conexiones_registradas, redes_routers, 
                                      conexiones_mapa, area_ospf)
        elif opcion == 4:  # Ver configuración
            continue  # El bucle mostrará la configuración nuevamente
        else:
            print("❌ Opción no válida. Selecciona 1, 2, 3 o 4.")

# Funciones para SWC3 (Switch Capa 3 funcionando como router)

def generar_router_id_swc3(area, contador_base):
    """
    Genera router-id para SWC3 basado en el router asociado
    Patrón: Si router es 1.1.1.1, SWC3 será 1.1.1.2
    El contador_base es el SIGUIENTE número disponible en esa área
    """
    area_num = int(area) + 1
    return f"{area_num}.{area_num}.{area_num}.{contador_base}"

def generar_comandos_swc3(router_num, vlans_asignadas, area_ospf, router_id_swc3, ip_hacia_router, ip_admin_swc3, tipo_ruteo="ospf", rutas_estaticas=None):
    """
    Genera comandos de configuración para Switch Capa 3
    """
    comandos = [
        "en",
        "conf t", 
        f"hostname SWC3_R{router_num}",
        "ip domain-name cisco",
        "crypto key generate rsa general-keys modulus 512",
        "line vty 0 5",
        "transport input ssh",
        "login local",
        "exit",
        "username admin privilege 15 password cisco",
        "enable secret cisco",
        "ip routing",  # Comando clave para habilitar routing
        
        # Interfaz hacia el router (sin switchport)
        "int gi1/0/1",
        "no switchport",
        f"ip add {ip_hacia_router} {convertir_mascara(30)}",
        "no shut",
        
        # VLAN administrativa
        "int vlan 1",
        f"ip add {ip_admin_swc3} 255.255.255.0",
        "no shut"
    ]
    
    # Configurar VLANs como interfaces separadas (no subinterfaces)
    for vlan_num, (network, mask) in vlans_asignadas.items():
        ip_usable = obtener_ip_usable(network, mask, -2)  # Penúltima IP (SWC3 toma penúltima, router toma última)
        mascara_decimal = convertir_mascara(mask)
        comandos.extend([
            f"int vlan {vlan_num}",
            f"ip add {ip_usable} {mascara_decimal}",
            "no shut"
        ])
    
    # Configurar DHCP para cada VLAN
    for vlan_num, (network, mask) in vlans_asignadas.items():
        default_router_ip = obtener_ip_usable(network, mask, -2)  # Penúltima IP
        mascara_decimal = convertir_mascara(mask)
        comandos.extend([
            f"ip dhcp pool {vlan_num}",
            f"default-router {default_router_ip}",
            f"network {network} {mascara_decimal}"
        ])
    
    # Crear VLANs físicamente
    for vlan_num in vlans_asignadas.keys():
        vlan_name = {2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez"}.get(vlan_num, f"vlan{vlan_num}")
        comandos.extend([
            f"vlan {vlan_num}",
            f"name {vlan_name}"
        ])
    
    # Crear VLAN 1
    comandos.extend([
        "vlan 1",
        "name uno"
    ])
    
    # Interfaz hacia el switch normal (con switchport trunk)
    comandos.extend([
        "int gi1/0/2",
        "switchport mode trunk",
        "exit"
    ])
    
    # Configuración de ruteo según el tipo elegido
    if tipo_ruteo == "ospf":
        # Configuración OSPF
        comandos.extend([
            "router ospf 1",
            f"router-id {router_id_swc3}",
            # Red administrativa
            f"network 192.168.{router_num}.0 0.0.0.255 area {area_ospf}",
            # Red hacia el router
            f"network {obtener_network_from_ip(ip_hacia_router, 30)} 0.0.0.3 area {area_ospf}"
        ])
        
        # Agregar redes de VLANs al área del router
        for vlan_num, (network, mask) in vlans_asignadas.items():
            wildcard = convertir_a_wildcard(convertir_mascara(mask))
            comandos.append(f"network {network} {wildcard} area {area_ospf}")
    
    elif tipo_ruteo == "estatico":
        # Configuración de rutas estáticas
        if rutas_estaticas:
            comandos_rutas = generar_comandos_rutas_estaticas(rutas_estaticas)
            comandos.extend(comandos_rutas)
    
    return comandos

def obtener_network_from_ip(ip, mask):
    """
    Obtiene la dirección de red a partir de una IP y máscara
    """
    import ipaddress
    network_obj = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
    return str(network_obj.network_address)

def asignar_swc3_a_router(router_num, num_swc3_asignados, routers_con_swc3):
    """
    Determina si un router específico debe tener SWC3
    """
    if num_swc3_asignados == 0:
        return False
    
    # Si ya está definido, usar esa configuración
    if router_num in routers_con_swc3:
        return routers_con_swc3[router_num]
    
    # Preguntar al usuario
    tiene_swc3 = validar_si_no(f"🔌 ¿El Router {router_num} tiene Switch Capa 3 (SWC3)? (s/n): ")
    routers_con_swc3[router_num] = tiene_swc3
    
    return tiene_swc3

# Función para generar código PTBuilder
def calcular_posicionamiento_inteligente(num_routers, routers_con_swc3):
    """
    Calcula posiciones automáticas para todos los dispositivos
    Distribución horizontal inteligente evitando solapamientos
    """
    posiciones = {}
    
    # Configuración de espaciado
    inicio_x = 100
    inicio_y = 100
    espaciado_routers = 400
    offset_swc3_y = 200
    offset_switch_y = 200
    
    for r in range(1, num_routers + 1):
        # Posición del router (distribución horizontal)
        router_x = inicio_x + (r - 1) * espaciado_routers
        router_y = inicio_y
        posiciones[f"Router{r}"] = (router_x, router_y)
        
        # Si tiene SWC3, posicionarlo debajo del router
        if routers_con_swc3.get(r, False):
            swc3_x = router_x
            swc3_y = router_y + offset_swc3_y
            posiciones[f"SWC3_R{r}"] = (swc3_x, swc3_y)
            
            # Switch debajo del SWC3
            switch_x = router_x
            switch_y = swc3_y + offset_switch_y
            posiciones[f"SWITCH{r}"] = (switch_x, switch_y)
        else:
            # Switch directamente debajo del router
            switch_x = router_x
            switch_y = router_y + offset_switch_y
            posiciones[f"SWITCH{r}"] = (switch_x, switch_y)
    
    return posiciones

def extraer_interfaces_del_cisco(archivo_cisco):
    """
    Extrae las interfaces utilizadas del archivo .CISCO generado
    para usar las mismas en PTBuilder
    """
    interfaces_por_dispositivo = {}
    
    try:
        with open(archivo_cisco, 'r') as f:
            contenido = f.read()
            lineas = contenido.split('\n')
            
            dispositivo_actual = None
            
            for linea in lineas:
                linea = linea.strip()
                
                # Detectar cambio de dispositivo
                if linea.startswith('hostname '):
                    dispositivo_actual = linea.replace('hostname ', '')
                    interfaces_por_dispositivo[dispositivo_actual] = []
                
                # Detectar interfaces
                if linea.startswith('int ') and dispositivo_actual:
                    interfaz = linea.replace('int ', '')
                    if interfaz not in interfaces_por_dispositivo[dispositivo_actual]:
                        interfaces_por_dispositivo[dispositivo_actual].append(interfaz)
    
    except Exception as e:
        print(f"⚠️ No se pudieron extraer interfaces del archivo CISCO: {e}")
        # Usar interfaces por defecto
        return {}
    
    return interfaces_por_dispositivo

def mapear_interfaces_conexiones(conexiones_mapa, interfaces_cisco, routers_con_swc3):
    """
    Mapea las conexiones con sus interfaces específicas basadas en el archivo CISCO
    """
    conexiones_con_interfaces = {}
    
    for conexion_key, (network, mask) in conexiones_mapa.items():
        r1, r2 = conexion_key
        
        # Buscar interfaces en el archivo CISCO
        hostname_r1 = f"Router{r1}"
        hostname_r2 = f"Router{r2}"
        
        # Interfaces por defecto (fallback)
        interface_r1 = "GigabitEthernet0/1/0"
        interface_r2 = "GigabitEthernet0/1/0"
        
        # Si tenemos interfaces del CISCO, usarlas
        if hostname_r1 in interfaces_cisco:
            # Buscar interfaces GigabitEthernet (no subinterfaces)
            interfaces_r1 = [i for i in interfaces_cisco[hostname_r1] if 'GigabitEthernet0/' in i and i.endswith('/0')]
            if interfaces_r1:
                interface_r1 = interfaces_r1[0]  # Usar la primera disponible
        
        if hostname_r2 in interfaces_cisco:
            interfaces_r2 = [i for i in interfaces_cisco[hostname_r2] if 'GigabitEthernet0/' in i and i.endswith('/0')]
            if interfaces_r2:
                interface_r2 = interfaces_r2[0]
        
        conexiones_con_interfaces[conexion_key] = {
            'network': network,
            'mask': mask,
            'r1_interface': interface_r1,
            'r2_interface': interface_r2,
            'link_type': 'cross'  # Router-Router siempre cross
        }
    
    return conexiones_con_interfaces

def generar_codigo_ptbuilder(datos_red, mapa_interfaces_dinamico):
    """Generar código JavaScript para PTBuilderV2 con interfaces dinámicas"""
    codigo_js = []
    
    # SISTEMA DE POSICIONAMIENTO INTELIGENTE
    # Separar dispositivos por router y agruparlos lógicamente
    routers_data = {}
    
    # Primero, organizar dispositivos por router
    for dispositivo in datos_red:
        nombre = dispositivo['nombre']
        tipo = dispositivo['tipo']
        
        if tipo == 'R':
            # Extraer número del router (ej: Router1 -> 1)
            router_num = int(nombre.replace('Router', ''))
            routers_data[router_num] = {
                'router': dispositivo,
                'swc3': None,
                'switch': None
            }
    
    # Buscar SWC3 y Switches correspondientes
    for dispositivo in datos_red:
        nombre = dispositivo['nombre']
        tipo = dispositivo['tipo']
        
        if tipo == 'SWC3':
            # SWC3_R1 corresponde a Router1 - extraer el número después de 'R'
            if '_R' in nombre:
                router_num = int(nombre.split('_R')[1])
            else:
                router_num = int(nombre.replace('SWC3_', ''))
            if router_num in routers_data:
                routers_data[router_num]['swc3'] = dispositivo
        elif tipo == 'SW':
            # SWITCH1 corresponde a Router1
            router_num = int(nombre.replace('SWITCH', ''))
            if router_num in routers_data:
                routers_data[router_num]['switch'] = dispositivo
    
    # CONFIGURACIÓN DE ESPACIADO Y DISTRIBUCIÓN
    ESPACIADO_HORIZONTAL = 250    # Distancia entre grupos de router
    ESPACIADO_VERTICAL = 200      # Distancia entre filas
    ESPACIADO_DISPOSITIVOS = 80   # Distancia entre dispositivos del mismo grupo
    ROUTERS_POR_FILA = 3          # Número de routers por fila
    
    # Posiciones base para cada fila
    X_INICIAL = 50
    Y_INICIAL = 50
    
    # Calcular posiciones para cada dispositivo
    posiciones = {}
    
    for i, (router_num, devices) in enumerate(sorted(routers_data.items())):
        # Calcular fila y posición en la fila
        fila = i // ROUTERS_POR_FILA
        posicion_en_fila = i % ROUTERS_POR_FILA
        
        # Coordenadas base del grupo
        x_base = X_INICIAL + (posicion_en_fila * ESPACIADO_HORIZONTAL)
        y_base = Y_INICIAL + (fila * ESPACIADO_VERTICAL)
        
        # Posicionar Router (centro del grupo)
        router_device = devices['router']
        posiciones[router_device['nombre']] = (x_base + ESPACIADO_DISPOSITIVOS, y_base)
        
        # Posicionar SWC3 (arriba del router, si existe)
        if devices['swc3']:
            swc3_device = devices['swc3']
            posiciones[swc3_device['nombre']] = (x_base + ESPACIADO_DISPOSITIVOS, y_base - ESPACIADO_DISPOSITIVOS)
        
        # Posicionar Switch (abajo del router)
        if devices['switch']:
            switch_device = devices['switch']
            # Si hay SWC3, el switch va abajo del SWC3; si no, va abajo del router
            y_switch = y_base + ESPACIADO_DISPOSITIVOS
            posiciones[switch_device['nombre']] = (x_base + ESPACIADO_DISPOSITIVOS, y_switch)
            
            # Posicionar PCs alrededor del switch (3 PCs por switch)
            pc_positions = [
                (x_base, y_switch + ESPACIADO_DISPOSITIVOS),           # PC1 - izquierda abajo
                (x_base + ESPACIADO_DISPOSITIVOS, y_switch + ESPACIADO_DISPOSITIVOS + 20), # PC2 - centro abajo
                (x_base + ESPACIADO_DISPOSITIVOS * 2, y_switch + ESPACIADO_DISPOSITIVOS)   # PC3 - derecha abajo
            ]
            for pc_num in range(1, 4):
                pc_name = f'PC{router_num}_{pc_num}'
                posiciones[pc_name] = pc_positions[pc_num - 1]
    
    # Paso 1: Crear dispositivos
    codigo_js.append('console.log("Ejecutando Paso 1: Creando dispositivos...");')
    
    # Crear dispositivos agrupados por router para mejor organización visual
    for i, (router_num, devices) in enumerate(sorted(routers_data.items())):
        # Crear router
        router_device = devices['router']
        x, y = posiciones[router_device['nombre']]
        codigo_js.append(f'addDevice("{router_device["nombre"]}", "2811", {x}, {y});')
        
        # Crear SWC3 si existe
        if devices['swc3']:
            swc3_device = devices['swc3']
            x, y = posiciones[swc3_device['nombre']]
            codigo_js.append(f'addDevice("{swc3_device["nombre"]}", "3650-24PS", {x}, {y});')
        
        # Crear Switch
        if devices['switch']:
            switch_device = devices['switch']
            x, y = posiciones[switch_device['nombre']]
            codigo_js.append(f'addDevice("{switch_device["nombre"]}", "2960-24TT", {x}, {y});')
            
            # Crear PCs conectadas al switch
            for pc_num in range(1, 4):
                pc_name = f'PC{router_num}_{pc_num}'
                pc_x, pc_y = posiciones[pc_name]
                codigo_js.append(f'addDevice("{pc_name}", "PC-PT", {pc_x}, {pc_y});')
    codigo_js.append('console.log("Paso 1 completado.");')
    codigo_js.append('')
    
    # Paso 2: Agregar módulos
    codigo_js.append('console.log("Ejecutando Paso 2: Agregando módulos...");')
    for dispositivo in datos_red:
        nombre = dispositivo['nombre']
        tipo = dispositivo['tipo']
        
        # Agregar módulos según el tipo
        if tipo == 'R':  # Router
            # Instalar módulo NM-4E en slot especial 1
            codigo_js.append(f'addModuleFixed("{nombre}", 1, "NM-4E");')
            # Instalar módulos HWIC en slots restantes
            for slot in [0, 2, 3]:  # Slots 0, 2, 3 (slot 1 usado por NM-4E)
                codigo_js.append(f'addModuleFixed("{nombre}", {slot}, "HWIC-1GE-SFP");')
    codigo_js.append('console.log("Paso 2 completado.");')
    codigo_js.append('')
    
    # Paso 3: Crear conexiones
    codigo_js.append('console.log("Ejecutando Paso 3: Creando conexiones...");')
    
    # Procesar todas las conexiones del mapa dinámico
    for conexion_key, conexion_data in mapa_interfaces_dinamico.items():
        
        # CONEXIONES ROUTER ↔ ROUTER (formato: (r1, r2))
        if isinstance(conexion_key, tuple) and len(conexion_key) == 2:
            r1, r2 = conexion_key
            device1 = f'Router{r1}'
            device2 = f'Router{r2}'
            interface1 = conexion_data['r1_interface']
            interface2 = conexion_data['r2_interface']
            cable_type = conexion_data['link_type']
            
            codigo_js.append(f'addLink("{device1}", "{interface1}", "{device2}", "{interface2}", "{cable_type}");')
        
        # CONEXIONES ROUTER ↔ SWC3, SWC3 ↔ SWITCH, ROUTER ↔ SWITCH (formato: string)
        elif isinstance(conexion_key, str):
            device1 = conexion_data['device1']
            device2 = conexion_data['device2']
            interface1 = conexion_data['interface1']
            interface2 = conexion_data['interface2']
            cable_type = conexion_data['link_type']
            
            codigo_js.append(f'addLink("{device1}", "{interface1}", "{device2}", "{interface2}", "{cable_type}");')
    
    codigo_js.append('console.log("Paso 3 completado.");')
    codigo_js.append('')
    
    # Paso 4: Configurar DHCP en las PCs
    codigo_js.append('console.log("Ejecutando Paso 4: Configurando DHCP en PCs...");')
    
    # Configurar DHCP en todas las PCs
    for i, (router_num, devices) in enumerate(sorted(routers_data.items())):
        if devices['switch']:
            for pc_num in range(1, 4):
                pc_name = f'PC{router_num}_{pc_num}'
                codigo_js.append(f'configurePcIp("{pc_name}", true);')
    
    codigo_js.append('console.log("Paso 4 completado. Topología lista!");')
    
    return '\n'.join(codigo_js)

def guardar_codigo_ptbuilder(filename_base, codigo_js):
    """
    Guarda el código JavaScript en un archivo separado
    """
    filename_js = f"{filename_base}_PTBuilder.js"
    
    try:
        with open(filename_js, 'w') as f:
            f.write(codigo_js)
        return filename_js
    except Exception as e:
        print(f"❌ Error al guardar código PTBuilder: {e}")
        return None

def mostrar_resumen_ptbuilder(filename_js, num_routers, num_swc3):
    """
    Muestra resumen de lo generado para PTBuilder con módulo NM-4E, distribución inteligente y PCs con DHCP
    """
    num_pcs = num_routers * 3  # 3 PCs por router/switch
    print(f"\n" + "="*60)
    print("🚀 CÓDIGO PTBUILDER V5.0 GENERADO")
    print("="*60)
    print(f"📁 Archivo JavaScript: {filename_js}")
    print(f"🖥️ Routers 2811 creados: {num_routers}")
    print(f"🔧 Módulos NM-4E instalados: {num_routers}")
    print(f"🔌 SWC3 creados: {num_swc3}")
    print(f"🔄 Switches creados: {num_routers}")
    print(f"💻 PCs creadas: {num_pcs} (3 por switch)")
    print(f"\n🎯 DISTRIBUCIÓN INTELIGENTE:")
    print(f"   • Dispositivos agrupados por router")
    print(f"   • 3 routers por fila (espaciado optimizado)")
    print(f"   • SWC3 arriba, Router centro, Switch abajo")
    print(f"   • PCs distribuidas alrededor de cada switch")
    print(f"   • Distancias reducidas entre dispositivos relacionados")
    print(f"\n💻 CONFIGURACIÓN DE PCs:")
    print(f"   • Modelo: PC-PT estándar")
    print(f"   • DHCP habilitado automáticamente")
    print(f"   • Interfaces: FastEthernet0/2, FastEthernet0/3, FastEthernet0/4")
    print(f"   • Conexiones straight a switch")
    print(f"\n🔧 CARACTERÍSTICAS DE LOS ROUTERS:")
    print(f"   • Modelo: Cisco 2811")
    print(f"   • Módulo NM-4E en slot 1")
    print(f"   • Interfaces NM-4E: Ethernet1/0, Ethernet1/1, Ethernet1/2, Ethernet1/3")
    print(f"   • Módulos HWIC-1GE-SFP en slots 0, 2, 3")
    print(f"\n📋 INSTRUCCIONES DE USO:")
    print(f"1. Abre PTBuilderV2 en Packet Tracer")
    print(f"2. Copia el contenido de {filename_js}")
    print(f"3. Pega en el editor de PTBuilderV2")
    print(f"4. Haz clic en 'Ejecutar'")
    print(f"5. ¡Tu topología completa con PCs se creará automáticamente!")
    print("="*60)

# Función principal
def main():
    print("=" * 70)
    print("🚀 GENERADOR DE REDES CISCO CON VALIDACIONES (V5.0)")
    print("=" * 70)
    print("✨ Incluye configuración de SSH, Seguridad, Switches y Validaciones")
    print("🔧 NUEVA FUNCIONALIDAD: Routers 2811 con módulo NM-4E")
    print("🔌 Interfaces: Ethernet1/0, Ethernet1/1, Ethernet1/2, Ethernet1/3")
    print("🔄 NOVEDAD V5.0: Soporte para OSPF y Ruteo Estático Automático")
    print("=" * 70)
    
    # Validaciones de entrada básicas
    filename = validar_nombre_archivo("📁 Introduce el nombre del archivo de salida (sin extensión): ")
    filename = f"{filename}.CISCO"
    
    base_ip = validar_ip("🌐 Introduce la IP base (se usará para todo): ")
    num_vlans = validar_numero_positivo("🏷️ Introduce el número de VLANs: ")
    
    subredes_ocupadas = []  # Para llevar el control de las subredes ya asignadas
    
    # Configurar VLANs y generar combos
    print("\n" + "="*50)
    print("🏷️ CONFIGURACIÓN DE VLANs")
    print("="*50)
    vlans_combos = configurar_vlans(num_vlans, base_ip, subredes_ocupadas)
    
    # NUEVA FUNCIONALIDAD: Selección de tipo de ruteo
    tipo_ruteo = validar_tipo_ruteo()
    print(f"✅ Tipo de ruteo seleccionado: {'OSPF' if tipo_ruteo == 'ospf' else 'Ruteo Estático'}")
    
    # Pedir número de routers y combos de /30
    num_routers = validar_numero_positivo("🖥️ Introduce el número de routers: ")
    
    # Preguntar cuántos routers tendrán SWC3
    print(f"\n🔌 CONFIGURACIÓN DE SWITCHES CAPA 3 (SWC3)")
    print("="*50)
    print("ℹ️ Los SWC3 van entre Router → SWC3 → Switch")
    num_swc3 = 0
    if num_routers > 0:
        num_swc3 = validar_numero(f"🔌 ¿Cuántos de los {num_routers} routers tendrán Switch Capa 3 (SWC3)? (0-{num_routers}): ")
        if num_swc3 > num_routers:
            print(f"❌ Error: No puedes tener más SWC3 ({num_swc3}) que routers ({num_routers})")
            num_swc3 = min(num_swc3, num_routers)
    
    # Calcular automáticamente el número de redes /30
    # Fórmula: (num_routers × 2) + num_swc3
    num_combos_30_calculado = (num_routers * 2) + num_swc3
    print(f"\n🔢 CÁLCULO AUTOMÁTICO DE REDES /30:")
    print(f"   📊 Routers: {num_routers} × 2 = {num_routers * 2} redes")
    print(f"   🔌 SWC3: {num_swc3} × 1 = {num_swc3} redes")
    print(f"   🎯 Total calculado: {num_combos_30_calculado} redes /30")
    
    # Permitir override manual si es necesario
    usar_calculo_automatico = validar_si_no(f"¿Usar el cálculo automático ({num_combos_30_calculado} redes /30)? (s/n): ")
    
    if usar_calculo_automatico:
        num_combos_30 = num_combos_30_calculado
        print(f"✅ Usando {num_combos_30} redes /30 automáticamente")
    else:
        num_combos_30 = validar_numero_positivo("🔗 Introduce manualmente cuántos combos de redes /30 necesitas: ")
    
    # Preguntar si desea usar asignación aleatoria para redes entre routers
    print(f"\n🔀 CONFIGURACIÓN DE REDES ENTRE ROUTERS")
    print("="*50)
    usar_aleatorio_routers = validar_si_no("¿Deseas usar asignación aleatoria para redes entre routers? (s/n): ")
    
    # Configurar redes entre routers
    redes_routers = configurar_redes_entre_routers(num_combos_30, base_ip, subredes_ocupadas, usar_aleatorio_routers)
    
    # Mapa de conexiones entre routers (para no duplicar)
    conexiones_mapa = {}
    router_vlans_asignadas = {}
    areas_ospf = {}  # Para guardar el área OSPF de cada router
    configuracion_orden = []  # Para llevar el orden de configuración de los routers
    
    # Estructuras para SWC3
    routers_con_swc3 = {}  # {router_num: True/False}
    swc3_configuraciones = {}  # {router_num: configuracion_swc3}
    
    # Contadores por área para los router-ids
    contadores_areas = {}
    router_ids = {}  # Para guardar los router-ids asignados
    swc3_router_ids = {}  # Para guardar los router-ids de SWC3
    
    # Mapa para rastrear las conexiones ya registradas para cada router
    conexiones_registradas = {i: [] for i in range(1, num_routers + 1)}
    
    # Para cada router, asignar VLANs y conexiones
    try:
        with open(filename, 'w') as f:
            f.write("! COMBOS GENERADOS CON VALIDACIONES (V5.0)\n")
            f.write("! Incluye SSH, Seguridad, configuración de Switches y Validaciones\n")
            f.write("! NUEVA FUNCIONALIDAD: Routers 2811 con módulo NM-4E\n")
            f.write("! Interfaces NM-4E: Ethernet1/0, Ethernet1/1, Ethernet1/2, Ethernet1/3\n")
            f.write(f"! TIPO DE RUTEO: {'OSPF' if tipo_ruteo == 'ospf' else 'RUTEO ESTÁTICO'}\n\n")
            
            # Imprimir combos generados
            f.write("! Redes entre routers (/30):\n")
            for idx, (network, mask) in enumerate(redes_routers):
                mascara_decimal = convertir_mascara(mask)
                f.write(f"! Red {idx+1}: {network}/{mask} ({mascara_decimal})\n")
            
            f.write("\n! Combos generados para cada VLAN:\n")
            for vlan_num, combos in vlans_combos:
                f.write(f"\n! VLAN {vlan_num}:\n")
                for idx, (network, mask) in enumerate(combos):
                    mascara_decimal = convertir_mascara(mask)
                    f.write(f"! Combo {idx+1}: {network}/{mask} ({mascara_decimal})\n")
            
            f.write("\n\n! CONFIGURACIÓN DE ROUTERS Y SWITCHES\n")
            
            # Pedir datos para configurar cada router
            for r in range(1, num_routers + 1):
                f.write(f"\n! ---- ROUTER {r} ----\n")
                print(f"\n" + "="*50)
                print(f"🖥️ CONFIGURANDO ROUTER {r}")
                print("="*50)
                
                # Solo pedir área OSPF si el tipo de ruteo es OSPF
                area_ospf = "0"  # Valor por defecto
                if tipo_ruteo == "ospf":
                    area_ospf = validar_area_ospf(f"🌐 ¿A qué área OSPF pertenece el router {r}? (0, 1, 2, etc.): ")
                
                areas_ospf[r] = area_ospf
                configuracion_orden.append(r)  # Registrar el orden de configuración
                
                # Asignar router-id (solo para OSPF, pero lo generamos siempre para compatibilidad)
                if area_ospf not in contadores_areas:
                    contadores_areas[area_ospf] = 1
                else:
                    contadores_areas[area_ospf] += 1
                    
                router_id = generar_router_id(area_ospf, contadores_areas[area_ospf])
                router_ids[r] = router_id
                
                f.write(f"! Router-ID: {router_id}\n")
                if tipo_ruteo == "ospf":
                    print(f"✅ Router-ID asignado: {router_id}")
                
                # Verificar si este router tiene SWC3
                tiene_swc3 = False
                if num_swc3 > 0:
                    swc3_asignados_hasta_ahora = sum(1 for asignado in routers_con_swc3.values() if asignado)
                    if swc3_asignados_hasta_ahora < num_swc3:
                        tiene_swc3 = asignar_swc3_a_router(r, num_swc3, routers_con_swc3)
                
                # Configurar SWC3 si es necesario
                swc3_config = None
                if tiene_swc3:
                    # Incrementar contador para SWC3 (siguiente número disponible en el área)
                    contadores_areas[area_ospf] += 1
                    swc3_router_id = generar_router_id_swc3(area_ospf, contadores_areas[area_ospf])
                    swc3_router_ids[r] = swc3_router_id
                    
                    # Asignar IPs para la conexión Router ↔ SWC3
                    if redes_routers:
                        red_router_swc3 = redes_routers.pop(0)  # Tomar una red /30
                        network_r_swc3, mask_r_swc3 = red_router_swc3
                        
                        # Router toma primera IP, SWC3 toma segunda IP
                        ip_router_hacia_swc3 = obtener_ip_usable(network_r_swc3, mask_r_swc3, 0)
                        ip_swc3_hacia_router = obtener_ip_usable(network_r_swc3, mask_r_swc3, 1)
                        
                        # IP administrativa del SWC3 (similar al router pero .3)
                        ip_admin_swc3 = f"192.168.{r}.3"
                        
                        swc3_config = {
                            'router_id': swc3_router_id,
                            'ip_hacia_router': ip_swc3_hacia_router,
                            'ip_admin': ip_admin_swc3,
                            'red_conexion': (network_r_swc3, mask_r_swc3)
                        }
                        
                        swc3_configuraciones[r] = swc3_config
                        
                        print(f"🔌 SWC3_R{r} configurado:")
                        if tipo_ruteo == "ospf":
                            print(f"   📊 Router-ID: {swc3_router_id}")
                        print(f"   🔗 Conexión: {network_r_swc3}/{mask_r_swc3}")
                        print(f"   📍 IP Router: {ip_router_hacia_swc3}")
                        print(f"   📍 IP SWC3: {ip_swc3_hacia_router}")
                        print(f"   🏠 IP Admin: {ip_admin_swc3}")
                        
                        f.write(f"! SWC3 Router-ID: {swc3_router_id}\n")
                        f.write(f"! Conexión Router-SWC3: {network_r_swc3}/{mask_r_swc3}\n")
                    else:
                        print("❌ No hay redes /30 disponibles para SWC3")
                        tiene_swc3 = False
                
                # Asignar VLANs al router
                vlans_router = {}
                num_vlans_router = validar_numero_positivo(f"🏷️ ¿Cuántas VLANs tiene el router {r}?: ")
                
                for i in range(num_vlans_router):
                    print(f"\n--- Asignando VLAN {i+1} de {num_vlans_router} ---")
                    vlan_id = validar_vlan_id(f"Número de VLAN a asignar (empezando desde 2): ", vlans_combos)
                    
                    # Buscar la VLAN en los combos generados
                    vlan_found = False
                    for v_id, combos in vlans_combos:
                        if v_id == vlan_id:
                            vlan_found = True
                            # Buscar un combo disponible
                            combo_usado = False
                            for network, mask in combos:
                                combo_asignado = False
                                for router_vlans in router_vlans_asignadas.values():
                                    if (network, mask) in router_vlans.values():
                                        combo_asignado = True
                                        break
                                
                                if not combo_asignado:
                                    vlans_router[vlan_id] = (network, mask)
                                    combo_usado = True
                                    print(f"✅ VLAN {vlan_id} asignada: {network}/{mask}")
                                    break
                            
                            if not combo_usado:
                                print(f"❌ No hay combos disponibles para la VLAN {vlan_id}")
                    
                    if not vlan_found:
                        print(f"❌ No se encontró la VLAN {vlan_id}")
                
                router_vlans_asignadas[r] = vlans_router
                
                # Primero, detectar conexiones ya configuradas con otros routers
                conexiones_previas, conexiones_ospf_previas = detectar_conexiones_previas(
                    r, conexiones_mapa, areas_ospf, configuracion_orden)
                
                # Mostrar las conexiones ya configuradas
                if conexiones_previas:
                    print(f"\n🔗 Conexiones ya configuradas para el Router {r}:")
                    for hacia_router, (network, mask, es_primer_router) in sorted(conexiones_previas.items()):
                        mascara_decimal = convertir_mascara(mask)
                        ip_offset = 0 if es_primer_router else -1
                        ip_usable = obtener_ip_usable(network, mask, ip_offset)
                        
                        # Registrar esta conexión
                        conexiones_registradas[r].append(hacia_router)
                        
                        print(f"  ✅ Router {r} ↔ Router {hacia_router}")
                        print(f"     Network: {network}/{mask} ({mascara_decimal})")
                        print(f"     IP de Router {r}: {ip_usable}")
                
                # Preguntar por nuevas conexiones
                nuevas_conexiones = validar_numero(f"\n🔗 ¿Cuántas conexiones NUEVAS tiene el router {r}? (No incluyas las ya detectadas): ")
                
                # Conexiones con otros routers
                conexiones_router = dict(conexiones_previas)  # Comenzar con las conexiones previas
                conexiones_ospf = dict(conexiones_ospf_previas)  # Conexiones OSPF previas
                
                for j in range(nuevas_conexiones):
                    print(f"\n--- Configurando conexión {j+1} de {nuevas_conexiones} ---")
                    
                    # Mostrar los routers que aún no están conectados a este router
                    routers_disponibles = [i for i in range(1, num_routers + 1) 
                                          if i != r and i not in conexiones_registradas[r]]
                    
                    if not routers_disponibles:
                        print(f"✅ El Router {r} ya está conectado a todos los demás routers.")
                        break
                    
                    print(f"🖥️ Routers disponibles para conexión: {routers_disponibles}")
                    hacia_router = validar_router_destino(f"¿Hacia qué router va la conexión {j+1} del router {r}?: ", r, num_routers, conexiones_registradas)
                    
                    # Verificar si ya existe una conexión entre estos routers
                    conexion_key = tuple(sorted([r, hacia_router]))
                    if conexion_key in conexiones_mapa:
                        network, mask = conexiones_mapa[conexion_key]
                        # Determinar si este router es el "primer router" en la conexión
                        es_primer_router = conexion_key[0] == r
                        
                        # Determinar a qué área pertenece esta red
                        # Si el router destino ya está configurado, usar su área
                        if hacia_router in configuracion_orden and configuracion_orden.index(hacia_router) < configuracion_orden.index(r):
                            area_red = areas_ospf[hacia_router]
                        else:
                            area_red = area_ospf
                    else:
                        # Asignar una red de la lista de redes entre routers
                        if redes_routers:
                            network, mask = redes_routers.pop(0)
                            conexiones_mapa[conexion_key] = (network, mask)
                            # Si este router tiene el número más bajo, es el "primer router" en la conexión
                            es_primer_router = r < hacia_router
                            # La red pertenece al área de este router ya que se está configurando primero
                            area_red = area_ospf
                        else:
                            print("❌ No hay más redes disponibles para conexiones entre routers")
                            continue
                    
                    # Guardar información sobre la conexión
                    conexiones_router[hacia_router] = (network, mask, es_primer_router)
                    conexiones_ospf[hacia_router] = (network, mask, es_primer_router, area_red)
                    
                    # Registrar esta conexión
                    conexiones_registradas[r].append(hacia_router)
                    
                    # Mostrar la asignación de IPs para los routers
                    ip_primer_router = obtener_ip_usable(network, mask, 0)  # Primera IP usable
                    ip_segundo_router = obtener_ip_usable(network, mask, -1)  # Última IP usable
                    mascara_decimal = convertir_mascara(mask)
                    
                    if es_primer_router:
                        area_text = f", Área OSPF: {area_red}" if tipo_ruteo == "ospf" else ""
                        print(f"✅ Router {r} tendrá la IP {ip_primer_router} (Máscara: {mascara_decimal}{area_text})")
                        print(f"✅ Router {hacia_router} tendrá la IP {ip_segundo_router} (Máscara: {mascara_decimal}{area_text})")
                    else:
                        area_text = f", Área OSPF: {area_red}" if tipo_ruteo == "ospf" else ""
                        print(f"✅ Router {r} tendrá la IP {ip_segundo_router} (Máscara: {mascara_decimal}{area_text})")
                        print(f"✅ Router {hacia_router} tendrá la IP {ip_primer_router} (Máscara: {mascara_decimal}{area_text})")
                
                # Permitir al usuario confirmar o modificar la configuración del router
                confirmar_o_modificar_router(r, vlans_router, conexiones_router, conexiones_ospf, 
                                           vlans_combos, router_vlans_asignadas, num_routers, 
                                           conexiones_registradas, redes_routers, conexiones_mapa, area_ospf)
                
                # Generar comandos para este router
                rutas_estaticas_router = None
                
                # Si es ruteo estático, calcular rutas después de configurar todos los routers
                # Por ahora, generar comandos básicos
                if tiene_swc3 and swc3_config:
                    # Router se conecta al SWC3, no directamente al switch
                    comandos_router = generar_comandos_router_con_swc3(r, vlans_router, conexiones_router, area_ospf, conexiones_ospf, router_id, tipo_ruteo, rutas_estaticas_router, swc3_config)
                else:
                    # Router normal (sin SWC3)
                    comandos_router = generar_comandos_router(r, vlans_router, conexiones_router, area_ospf, conexiones_ospf, router_id, tipo_ruteo, rutas_estaticas_router)
                
                # Escribir comandos del router en el archivo
                f.write("\n! -- CONFIGURACIÓN DE ROUTER --\n")
                for comando in comandos_router:
                    f.write(f"{comando}\n")
                
                # Si tiene SWC3, escribir también su configuración
                if tiene_swc3 and swc3_config:
                    f.write(f"\n! -- CONFIGURACIÓN DEL SWC3_R{r} --\n")
                    comandos_swc3 = generar_comandos_swc3(r, vlans_router, area_ospf, swc3_config['router_id'], 
                                                        swc3_config['ip_hacia_router'], swc3_config['ip_admin'], 
                                                        tipo_ruteo, rutas_estaticas_router)
                    for comando in comandos_swc3:
                        f.write(f"{comando}\n")
                
                # Generar y escribir comandos para el switch asociado
                f.write(f"\n! -- CONFIGURACIÓN DEL SWITCH{r} --\n")
                comandos_switch = generar_comandos_switch(r, vlans_combos)
                for comando in comandos_switch:
                    f.write(f"{comando}\n")
                
                print(f"✅ Router {r} configurado correctamente")
            
            # NUEVA FUNCIONALIDAD: Calcular y agregar rutas estáticas si es necesario
            if tipo_ruteo == "estatico":
                print(f"\n" + "="*70)
                print("🔄 CALCULANDO Y AGREGANDO RUTAS ESTÁTICAS")
                print("="*70)
                
                # Calcular rutas estáticas para todos los routers
                rutas_estaticas_por_router, rutas_estaticas_por_swc3 = calcular_rutas_estaticas(
                    conexiones_mapa, router_vlans_asignadas, num_routers, 
                    routers_con_swc3, swc3_configuraciones
                )
                
                # Agregar las rutas estáticas al final del archivo
                f.write(f"\n\n! ======================================\n")
                f.write(f"! RUTAS ESTÁTICAS CALCULADAS AUTOMÁTICAMENTE\n")
                f.write(f"! ======================================\n\n")
                
                for router_num in range(1, num_routers + 1):
                    if router_num in rutas_estaticas_por_router and rutas_estaticas_por_router[router_num]:
                        f.write(f"! ---- RUTAS ESTÁTICAS PARA ROUTER {router_num} ----\n")
                        f.write(f"! Configurar en Router{router_num}:\n")
                        
                        comandos_rutas = generar_comandos_rutas_estaticas(rutas_estaticas_por_router[router_num])
                        for comando in comandos_rutas:
                            f.write(f"{comando}\n")
                        f.write(f"\n")
                        
                        # También agregar rutas para SWC3 si existe - USAR RUTAS ESPECÍFICAS
                        if router_num in routers_con_swc3 and routers_con_swc3[router_num]:
                            f.write(f"! ---- RUTAS ESTÁTICAS PARA SWC3_R{router_num} ----\n")
                            f.write(f"! Configurar en SWC3_R{router_num}:\n")
                            
                            # Usar las rutas específicas del SWC3, no las del router
                            if router_num in rutas_estaticas_por_swc3:
                                comandos_rutas_swc3 = generar_comandos_rutas_estaticas(rutas_estaticas_por_swc3[router_num])
                                for comando in comandos_rutas_swc3:
                                    f.write(f"{comando}\n")
                            f.write(f"\n")
        
        print(f"\n🎉 ¡Configuraciones guardadas exitosamente en {filename}!")
        
        # ==========================================
        # GENERAR CÓDIGO PTBUILDER V2
        # ==========================================
        
        # Crear mapa dinámico de interfaces basado en la configuración real
        mapa_interfaces_dinamico = crear_mapa_interfaces_dinamico(conexiones_mapa, router_vlans_asignadas, routers_con_swc3)
        
        # Mostrar el mapa de interfaces generado
        mostrar_mapa_interfaces(mapa_interfaces_dinamico)
        
        # Preparar datos de red para PTBuilder
        datos_red = []
        
        # Agregar routers
        for r in range(1, num_routers + 1):
            datos_red.append({'nombre': f'Router{r}', 'tipo': 'R'})
        
        # Agregar SWC3
        for r in range(1, num_routers + 1):
            if routers_con_swc3.get(r, False):
                datos_red.append({'nombre': f'SWC3_R{r}', 'tipo': 'SWC3'})
        
        # Agregar switches
        for r in range(1, num_routers + 1):
            datos_red.append({'nombre': f'SWITCH{r}', 'tipo': 'SW'})
        
        # Agregar PCs (3 PCs por switch)
        for r in range(1, num_routers + 1):
            for pc_num in range(1, 4):  # PC1, PC2, PC3 por cada switch
                datos_red.append({'nombre': f'PC{r}_{pc_num}', 'tipo': 'PC', 'switch': r})
        
        # Generar código JavaScript para PTBuilder
        codigo_js = generar_codigo_ptbuilder(datos_red, mapa_interfaces_dinamico)
        
        # Guardar archivo JavaScript
        filename_base = filename.replace('.CISCO', '')
        filename_js = guardar_codigo_ptbuilder(filename_base, codigo_js)
        
        if filename_js:
            # Mostrar resumen de PTBuilder
            num_swc3_creados = sum(1 for asignado in routers_con_swc3.values() if asignado)
            mostrar_resumen_ptbuilder(filename_js, num_routers, num_swc3_creados)
        
        # Mostrar resumen de los router-IDs asignados por área (solo para OSPF)
        if tipo_ruteo == "ospf":
            print(f"\n" + "="*50)
            print("📋 RESUMEN DE ROUTER-IDS ASIGNADOS")
            print("="*50)
            for area, contador in contadores_areas.items():
                print(f"🌐 Área {area}:")
                for r, rid in router_ids.items():
                    if areas_ospf[r] == area:
                        print(f"   🖥️ Router {r}: {rid}")
                        # Mostrar SWC3 si existe
                        if r in swc3_router_ids:
                            print(f"   🔌 SWC3_R{r}: {swc3_router_ids[r]}")
        
        # Mostrar resumen de conexiones entre routers
        print(f"\n" + "="*50)
        print("🔗 RESUMEN DE CONEXIONES ENTRE ROUTERS")
        print("="*50)
        for r in range(1, num_routers + 1):
            conexiones = sorted(conexiones_registradas[r])
            if conexiones:
                print(f"🖥️ Router {r} está conectado a: {conexiones}")
            else:
                print(f"🖥️ Router {r}: Sin conexiones adicionales")
        
        # Mostrar resumen de SWC3
        if any(routers_con_swc3.values()):
            print(f"\n" + "="*50)
            print("🔌 RESUMEN DE SWITCHES CAPA 3 (SWC3)")
            print("="*50)
            for r in range(1, num_routers + 1):
                if routers_con_swc3.get(r, False):
                    swc3_config = swc3_configuraciones.get(r)
                    if swc3_config:
                        print(f"🔌 SWC3_R{r}:")
                        print(f"   🏠 IP Admin: {swc3_config['ip_admin']}")
                        print(f"   📍 IP hacia Router: {swc3_config['ip_hacia_router']}")
                        print(f"   🔗 Red conexión: {swc3_config['red_conexion'][0]}/{swc3_config['red_conexion'][1]}")
        
        # Mostrar resumen específico del tipo de ruteo
        print(f"\n" + "="*50)
        print(f"🔄 RESUMEN DE CONFIGURACIÓN DE RUTEO")
        print("="*50)
        print(f"📊 Tipo de ruteo utilizado: {'OSPF' if tipo_ruteo == 'ospf' else 'Ruteo Estático'}")
        
        if tipo_ruteo == "estatico":
            total_rutas = sum(len(rutas) for rutas in rutas_estaticas_por_router.values())
            print(f"📍 Total de rutas estáticas calculadas: {total_rutas}")
            print(f"🤖 Rutas calculadas automáticamente por algoritmo BFS")
            print(f"✅ Todas las redes son alcanzables entre routers")
        else:
            areas_unicas = set(areas_ospf.values())
            print(f"🌐 Áreas OSPF configuradas: {sorted(areas_unicas)}")
            print(f"🔄 Protocolo de ruteo dinámico activado")
            print(f"📊 Router-IDs asignados automáticamente")
        
        print(f"\n" + "="*50)
        print("🌐 RESUMEN DE DIRECCIONES IP DE ADMINISTRACIÓN")
        print("="*50)
        for r in range(1, num_routers + 1):
            print(f"🖥️ Router {r}: 192.168.{r}.1")
            if routers_con_swc3.get(r, False):
                swc3_config = swc3_configuraciones.get(r)
                if swc3_config:
                    print(f"🔌 SWC3_R{r}: {swc3_config['ip_admin']}")
            print(f"🔄 Switch {r}: 192.168.{r}.2")
            
    except Exception as e:
        print(f"❌ Error al generar el archivo: {str(e)}")
        print("🔧 Por favor, verifica los datos introducidos e intenta nuevamente.")

# Función para generar comandos para un router CON SWC3
def generar_comandos_router_con_swc3(router_num, vlans_asignadas, conexiones_routers, area_ospf, conexiones_ospf, router_id, tipo_ruteo="ospf", rutas_estaticas=None, swc3_config=None):
    """
    Genera comandos para un router que tiene SWC3 intermedio
    El router NO configura VLANs directamente, se conecta al SWC3
    """
    # Configuración básica con SSH y seguridad
    comandos = [
        "en", 
        "conf t", 
        f"hostname Router{router_num}",
        "ip domain-name cisco",
        "crypto key generate rsa general-keys modulus 512",
        "line vty 0 5",
        "transport input ssh",
        "login local",
        "exit",
        "username admin privilege 15 password cisco"
    ]
    
    # Interfaz hacia el SWC3 - Configurar IP correcta
    if swc3_config:
        # Calcular la IP del router hacia el SWC3 (primera IP usable de la red /30)
        network, mask = swc3_config['red_conexion']
        ip_router_hacia_swc3 = obtener_ip_usable(network, mask, 0)  # Primera IP
        mascara_decimal = convertir_mascara(mask)
        
        comandos.extend([
            "int fa0/0",
            f"ip add {ip_router_hacia_swc3} {mascara_decimal}",
            "no shut"
        ])
    else:
        # Fallback si no hay configuración SWC3
        comandos.extend([
            "int fa0/0",
            "! Configuración hacia SWC3 - IP será configurada según la red asignada",
            "no shut"
        ])

    # Comandos para conexiones entre routers - Usando interfaces del módulo NM-4E
    conexiones_ordenadas = sorted(conexiones_routers.items(), key=lambda x: x[0])
    interface_idx = 0  # Comenzar desde Ethernet1/0 (fa0/0 se usa para SWC3)
    for hacia_router, (network, mask, es_primer_router) in conexiones_ordenadas:
        interface = f"Ethernet1/{interface_idx}"  # Usar interfaces del módulo NM-4E
        # Si este router es el "primer router" en la conexión, usa primera IP usable, sino usa la última
        ip_offset = 0 if es_primer_router else -1
        ip_usable = obtener_ip_usable(network, mask, ip_offset)
        mascara_decimal = convertir_mascara(mask)
        comandos.extend(configurar_interface(interface, ip_usable, mascara_decimal))
        interface_idx += 1

    # Configuración de ruteo según el tipo elegido
    if tipo_ruteo == "ospf":
        # Configuración OSPF
        comandos.extend([
            f"router ospf 1",
            f"router-id {router_id}"
        ])
        
        # Agregar red hacia SWC3 si está configurada
        if swc3_config:
            network, mask = swc3_config['red_conexion']
            wildcard = convertir_a_wildcard(convertir_mascara(mask))
            comandos.append(f"network {network} {wildcard} area {area_ospf}")
        
        # Agregar redes entre routers al área correspondiente - Ordenados
        conexiones_ospf_ordenadas = sorted(conexiones_ospf.items(), key=lambda x: x[0])
        for hacia_router, (network, mask, es_primer_router, area) in conexiones_ospf_ordenadas:
            wildcard = convertir_a_wildcard(convertir_mascara(mask))
            comandos.append(f"network {network} {wildcard} area {area}")
    
    elif tipo_ruteo == "estatico":
        # Configuración de rutas estáticas
        if rutas_estaticas:
            comandos_rutas = generar_comandos_rutas_estaticas(rutas_estaticas)
            comandos.extend(comandos_rutas)

    return comandos

def crear_mapa_interfaces_dinamico(conexiones_mapa, router_vlans_asignadas, routers_con_swc3):
    """
    Crea un mapa dinámico de interfaces basado en:
    1. Conexiones entre routers (GigabitEthernet0/X/0 secuencial)
    2. Conexiones Router-SWC3 (Router: FastEthernet0/0, SWC3: GigabitEthernet1/0/1)
    3. Conexiones SWC3-Switch (SWC3: GigabitEthernet1/0/2, Switch: GigabitEthernet0/1)
    """
    mapa_interfaces = {}
    
    # 1. MAPEAR CONEXIONES ROUTER ↔ ROUTER
    for conexion_key, (network, mask) in conexiones_mapa.items():
        r1, r2 = conexion_key
        
        # Para router-router, usar Ethernet1/X del módulo NM-4E secuencialmente
        # El índice depende del orden de las conexiones para cada router
        
        # Contar cuántas conexiones ya tiene cada router
        conexiones_r1 = [c for c in conexiones_mapa.keys() if r1 in c]
        conexiones_r2 = [c for c in conexiones_mapa.keys() if r2 in c]
        
        # Ordenar para ser consistente
        conexiones_r1_ordenadas = sorted(conexiones_r1, key=lambda x: (x[0], x[1]))
        conexiones_r2_ordenadas = sorted(conexiones_r2, key=lambda x: (x[0], x[1]))
        
        # Encontrar el índice de esta conexión para cada router
        idx_r1 = conexiones_r1_ordenadas.index(conexion_key)  # Empezar desde 0 para Ethernet1/0
        idx_r2 = conexiones_r2_ordenadas.index(conexion_key)
        
        interface_r1 = f"Ethernet1/{idx_r1}"  # Usar interfaces del módulo NM-4E
        interface_r2 = f"Ethernet1/{idx_r2}"
        
        mapa_interfaces[conexion_key] = {
            'network': network,
            'mask': mask,
            'r1_interface': interface_r1,
            'r2_interface': interface_r2,
            'link_type': 'cross'  # Router-Router siempre cross
        }
    
    # 2. AGREGAR CONEXIONES ROUTER ↔ SWC3
    for router_num in router_vlans_asignadas.keys():
        if routers_con_swc3.get(router_num, False):
            # Conexión Router → SWC3
            router_swc3_key = f"Router{router_num}_SWC3_R{router_num}"
            mapa_interfaces[router_swc3_key] = {
                'device1': f"Router{router_num}",
                'device2': f"SWC3_R{router_num}",
                'interface1': "FastEthernet0/0",  # Router usa fa0/0 para SWC3
                'interface2': "GigabitEthernet1/0/1",  # SWC3 usa gi1/0/1 para router
                'link_type': 'straight'
            }
            
            # Conexión SWC3 → Switch
            swc3_switch_key = f"SWC3_R{router_num}_SWITCH{router_num}"
            mapa_interfaces[swc3_switch_key] = {
                'device1': f"SWC3_R{router_num}",
                'device2': f"SWITCH{router_num}",
                'interface1': "GigabitEthernet1/0/2",  # SWC3 usa gi1/0/2 para switch
                'interface2': "FastEthernet0/1",  # Switch usa fa0/1 (consistente con .CISCO)
                'link_type': 'cross'  # SWC3 a Switch requiere cable cross
            }
        else:
            # Conexión directa Router → Switch (sin SWC3)
            router_switch_key = f"Router{router_num}_SWITCH{router_num}"
            mapa_interfaces[router_switch_key] = {
                'device1': f"Router{router_num}",
                'device2': f"SWITCH{router_num}",
                'interface1': "FastEthernet0/0",  # Router usa fa0/0 para switch
                'interface2': "FastEthernet0/1",  # Switch usa fa0/1 (consistente con .CISCO)
                'link_type': 'straight'
            }
    
    # 3. AGREGAR CONEXIONES PARA ROUTERS SIN SWC3 (si no se procesaron arriba)
    for router_num in router_vlans_asignadas.keys():
        if not routers_con_swc3.get(router_num, False):
            router_switch_key = f"Router{router_num}_SWITCH{router_num}"
            if router_switch_key not in mapa_interfaces:  # Evitar duplicados
                mapa_interfaces[router_switch_key] = {
                    'device1': f"Router{router_num}",
                    'device2': f"SWITCH{router_num}",
                    'interface1': "FastEthernet0/0",  # Router usa fa0/0 para switch
                    'interface2': "FastEthernet0/1",  # Switch usa fa0/1 (consistente con .CISCO)
                    'link_type': 'straight'
                }
    
    # 4. AGREGAR CONEXIONES PC ↔ SWITCH (3 PCs por switch)
    for router_num in router_vlans_asignadas.keys():
        switch_interfaces = ["FastEthernet0/2", "FastEthernet0/3", "FastEthernet0/4"]
        for pc_num in range(1, 4):  # PC 1, 2, 3
            pc_switch_key = f"PC{router_num}_{pc_num}_SWITCH{router_num}"
            mapa_interfaces[pc_switch_key] = {
                'device1': f"PC{router_num}_{pc_num}",
                'device2': f"SWITCH{router_num}",
                'interface1': "FastEthernet0",  # PC siempre usa FastEthernet0
                'interface2': switch_interfaces[pc_num - 1],  # fa0/2, fa0/3, fa0/4
                'link_type': 'straight'  # PC a Switch siempre straight
            }
    
    return mapa_interfaces

def mostrar_mapa_interfaces(mapa_interfaces_dinamico):
    """
    Muestra el mapa de interfaces dinámico generado para verificación
    """
    print(f"\n" + "="*60)
    print("🔗 MAPA DE INTERFACES DINÁMICO GENERADO")
    print("="*60)
    
    # Separar por tipos de conexión
    conexiones_router_router = []
    conexiones_infraestructura = []
    
    for key, data in mapa_interfaces_dinamico.items():
        if isinstance(key, tuple):
            conexiones_router_router.append((key, data))
        else:
            conexiones_infraestructura.append((key, data))
    
    # Mostrar conexiones Router ↔ Router
    if conexiones_router_router:
        print("🖥️ CONEXIONES ROUTER ↔ ROUTER:")
        for (r1, r2), data in sorted(conexiones_router_router):
            print(f"   Router{r1}[{data['r1_interface']}] ↔ Router{r2}[{data['r2_interface']}] ({data['link_type']})")
    
    # Mostrar conexiones de infraestructura
    if conexiones_infraestructura:
        print("\n🔌 CONEXIONES DE INFRAESTRUCTURA:")
        
        # Separar conexiones por tipo para mejor organización
        conexiones_router_switch = []
        conexiones_swc3 = []
        conexiones_pc_switch = []
        
        for key, data in sorted(conexiones_infraestructura):
            device1 = data['device1']
            device2 = data['device2']
            interface1 = data['interface1']
            interface2 = data['interface2']
            link_type = data['link_type']
            
            if 'PC' in device1:
                conexiones_pc_switch.append(f"   {device1}[{interface1}] ↔ {device2}[{interface2}] ({link_type})")
            elif 'SWC3' in device1 or 'SWC3' in device2:
                conexiones_swc3.append(f"   {device1}[{interface1}] ↔ {device2}[{interface2}] ({link_type})")
            else:
                conexiones_router_switch.append(f"   {device1}[{interface1}] ↔ {device2}[{interface2}] ({link_type})")
        
        # Mostrar conexiones organizadas
        if conexiones_router_switch:
            for conexion in conexiones_router_switch:
                print(conexion)
        if conexiones_swc3:
            for conexion in conexiones_swc3:
                print(conexion)
        if conexiones_pc_switch:
            print("\n💻 CONEXIONES PC ↔ SWITCH:")
            for conexion in conexiones_pc_switch:
                print(conexion)
    
    print("="*60)

def validar_conexiones_nm4e(router_num, conexiones_existentes, nueva_conexion=None):
    """
    Valida que un router no exceda las 4 interfaces disponibles del módulo NM-4E
    """
    MAX_INTERFACES_NM4E = 4
    num_conexiones = len(conexiones_existentes)
    
    if nueva_conexion:
        num_conexiones += 1
    
    if num_conexiones > MAX_INTERFACES_NM4E:
        print(f"❌ Error: El Router {router_num} no puede tener más de {MAX_INTERFACES_NM4E} conexiones.")
        print(f"   Conexiones actuales: {len(conexiones_existentes)}")
        print(f"   Interfaces disponibles en módulo NM-4E: Ethernet1/0, Ethernet1/1, Ethernet1/2, Ethernet1/3")
        return False
    
    return True

if __name__ == "__main__":
    main()
