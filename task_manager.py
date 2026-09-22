"""
Gestor de tareas en consola
----------------------------
Aplicación de línea de comandos para gestionar una lista de tareas
con persistencia en un archivo JSON.

Autor: Leonard Carrión Morales
Uso:
    python task_manager.py
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.json")

PRIORIDADES = {"1": "Alta", "2": "Media", "3": "Baja"}


# ---------------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------------

def cargar_tareas():
    """Lee las tareas guardadas en el archivo JSON. Si no existe, devuelve una lista vacía."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Aviso: el archivo de tareas estaba dañado o vacío. Se empieza desde cero.")
        return []


def guardar_tareas(tareas):
    """Escribe la lista de tareas en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Operaciones sobre tareas
# ---------------------------------------------------------------------------

def siguiente_id(tareas):
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1


def agregar_tarea(tareas):
    descripcion = input("Descripción de la tarea: ").strip()
    if not descripcion:
        print("La descripción no puede estar vacía.\n")
        return

    print("Prioridad -> 1) Alta  2) Media  3) Baja")
    prioridad_input = input("Elige una opción [2]: ").strip() or "2"
    prioridad = PRIORIDADES.get(prioridad_input, "Media")

    tarea = {
        "id": siguiente_id(tareas),
        "descripcion": descripcion,
        "prioridad": prioridad,
        "completada": False,
        "creada": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tareas.append(tarea)
    guardar_tareas(tareas)
    print(f"Tarea #{tarea['id']} añadida.\n")


def listar_tareas(tareas, solo_pendientes=False):
    if not tareas:
        print("No hay tareas registradas.\n")
        return

    vista = [t for t in tareas if not t["completada"]] if solo_pendientes else tareas
    if not vista:
        print("No hay tareas pendientes. ¡Todo al día!\n")
        return

    orden_prioridad = {"Alta": 0, "Media": 1, "Baja": 2}
    vista = sorted(vista, key=lambda t: (t["completada"], orden_prioridad.get(t["prioridad"], 1)))

    print("\n{:<4} {:<8} {:<10} {:<40} {}".format("ID", "Estado", "Prioridad", "Descripción", "Creada"))
    print("-" * 80)
    for t in vista:
        estado = "[X]" if t["completada"] else "[ ]"
        print("{:<4} {:<8} {:<10} {:<40} {}".format(
            t["id"], estado, t["prioridad"], t["descripcion"][:38], t["creada"]
        ))
    print()


def completar_tarea(tareas):
    listar_tareas(tareas, solo_pendientes=True)
    id_texto = input("ID de la tarea a marcar como completada: ").strip()
    if not id_texto.isdigit():
        print("ID no válido.\n")
        return

    tarea = buscar_tarea(tareas, int(id_texto))
    if tarea is None:
        print("No existe ninguna tarea con ese ID.\n")
        return

    tarea["completada"] = True
    guardar_tareas(tareas)
    print(f"Tarea #{tarea['id']} marcada como completada.\n")


def eliminar_tarea(tareas):
    listar_tareas(tareas)
    id_texto = input("ID de la tarea a eliminar: ").strip()
    if not id_texto.isdigit():
        print("ID no válido.\n")
        return

    tarea = buscar_tarea(tareas, int(id_texto))
    if tarea is None:
        print("No existe ninguna tarea con ese ID.\n")
        return

    confirmacion = input(f"¿Eliminar '{tarea['descripcion']}'? (s/n): ").strip().lower()
    if confirmacion == "s":
        tareas.remove(tarea)
        guardar_tareas(tareas)
        print("Tarea eliminada.\n")
    else:
        print("Operación cancelada.\n")


def buscar_tarea(tareas, tarea_id):
    for t in tareas:
        if t["id"] == tarea_id:
            return t
    return None


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def mostrar_menu():
    print("=" * 40)
    print("        GESTOR DE TAREAS")
    print("=" * 40)
    print("1. Añadir tarea")
    print("2. Ver todas las tareas")
    print("3. Ver tareas pendientes")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")


def main():
    tareas = cargar_tareas()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            agregar_tarea(tareas)
        elif opcion == "2":
            listar_tareas(tareas)
        elif opcion == "3":
            listar_tareas(tareas, solo_pendientes=True)
        elif opcion == "4":
            completar_tarea(tareas)
        elif opcion == "5":
            eliminar_tarea(tareas)
        elif opcion == "6":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida, prueba de nuevo.\n")


if __name__ == "__main__":
    main()
