import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
import re
from datetime import datetime, date

from Libros import Libros
from Libros_dao_gui import LibrosDao

class LibrosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Sistema de Gestión de Libros - Versión Premium")
        self.root.geometry("1400x800")
        self.root.configure(bg="#FDFDFD")

        # Configurar tema moderno
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        # Inicializar DAO
        self.libros_dao = LibrosDao()
        ...
        # Lista de géneros literarios
        self.generos_literarios = [
            "Ficción", "No ficción", "Novela", "Cuento", "Poesía",
            "Drama/Teatro", "Ensayo", "Biografía", "Autobiografía", "Historia",
            "Ciencia ficción", "Fantasía", "Misterio/Thriller", "Romance",
            "Terror/Horror", "Aventura", "Realismo mágico", "Distopía",
            "Literatura clásica", "Literatura contemporánea", "Literatura juvenil",
            "Literatura infantil", "Autoayuda", "Filosofía", "Religión/Espiritualidad",
            "Ciencia", "Tecnología", "Arte", "Viajes", "Cocina", "Deportes", "Otros"
        ]
        
        # Variable para el filtro de estado
        self.filtro_estado = tk.StringVar(value="todos")
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.cargar_libros()
    
    def configurar_estilos_personalizados(self):
        """Configura estilos personalizados para una interfaz más atractiva"""
        
        # Estilo para el título principal
        self.style.configure("Title.TLabel", 
                           font=('Segoe UI', 20, 'bold'),
                           foreground="#000000",
                           background='#f8f9fa')
        
        # Estilo para subtítulos
        self.style.configure("Subtitle.TLabel", 
                           font=('Segoe UI', 12, 'bold'),
                           foreground='#34495e',
                           background='#f8f9fa')
        
        # Estilo para campos válidos
        self.style.configure("Valid.TEntry", 
                           fieldbackground="#d4edda",
                           bordercolor="#28a745",
                           focuscolor="#28a745")
        
        # Estilo para campos inválidos
        self.style.configure("Invalid.TEntry", 
                           fieldbackground="#f8d7da",
                           bordercolor="#dc3545",
                           focuscolor="#dc3545")
        
        # Estilo para botones principales
        self.style.configure("Primary.TButton",
                           font=('Segoe UI', 10, 'bold'),
                           foreground='gray',
                           background='#007bff',
                           borderwidth=0,
                           focuscolor='none')
        
        # Estilo para botones secundarios
        self.style.configure("Secondary.TButton",
                           font=('Segoe UI', 9),
                           foreground='#6c757d',
                           background='#e9ecef',
                           borderwidth=0,
                           focuscolor='none')
        
        # Estilo para botones de peligro
        self.style.configure("Danger.TButton",
                           font=('Segoe UI', 10, 'bold'),
                           foreground='gray',
                           background='#dc3545',
                           borderwidth=0,
                           focuscolor='none')
        
        # Estilo para botones de éxito
        self.style.configure("Success.TButton",
                           font=('Segoe UI', 10, 'bold'),
                           foreground='gray',
                           background='#28a745',
                           borderwidth=0,
                           focuscolor='none')
        
        # Estilo para LabelFrames
        self.style.configure("Card.TLabelframe",
                           background='#ffffff',
                           borderwidth=2,
                           relief='solid')
        
        self.style.configure("Card.TLabelframe.Label",
                           font=('Segoe UI', 11, 'bold'),
                           foreground='#495057',
                           background='#ffffff')
        
        # Estilo para el Treeview
        self.style.configure("Modern.Treeview",
                           background="#ffffff",
                           foreground="#212529",
                           rowheight=25,
                           fieldbackground="#ffffff",
                           borderwidth=1,
                           relief="solid")
        
        self.style.configure("Modern.Treeview.Heading",
                           font=('Segoe UI', 10, 'bold'),
                           foreground="#495057",
                           background="#e9ecef",
                           borderwidth=1,
                           relief="solid")
        
        # Configurar colores de selección
        self.style.map("Modern.Treeview",
                      background=[('selected', '#007bff')],
                      foreground=[('selected', 'white')])
    
    def crear_interfaz(self):
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20", style="Card.TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header con título y descripción
        self.crear_header(main_frame)
        
        # Barra de filtros
        self.crear_barra_filtros(main_frame)
        
        # Contenido principal (formulario y tabla)
        self.crear_contenido_principal(main_frame)
        
        # Footer con estadísticas
        self.crear_footer(main_frame)
    
    def crear_header(self, parent):
        """Crea el header de la aplicación"""
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        # Título principal
        titulo = ttk.Label(header_frame, 
                          text="📚 Sistema de Gestión de Libros", 
                          style="Title.TLabel")
        titulo.grid(row=0, column=0, pady=(0, 5))
        
        # Subtítulo
        subtitulo = ttk.Label(header_frame, 
                             text="Organiza tu biblioteca personal de manera elegante y eficiente",
                             font=('Segoe UI', 11),
                             foreground='#6c757d')
        subtitulo.grid(row=1, column=0)
    
    def crear_barra_filtros(self, parent):
        """Crea la barra de filtros superior"""
        filtros_frame = ttk.LabelFrame(parent, text="🔍 Filtros y Búsqueda", 
                                      style="Card.TLabelframe", padding="15")
        filtros_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        filtros_frame.columnconfigure(2, weight=1)
        
        # Filtro por estado
        ttk.Label(filtros_frame, text="Estado:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, padx=(0, 10))
        
        estado_frame = ttk.Frame(filtros_frame)
        estado_frame.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Radiobutton(estado_frame, text="Todos", variable=self.filtro_estado, 
                       value="todos", command=self.aplicar_filtro_estado).grid(row=0, column=0, padx=(0, 10))
        ttk.Radiobutton(estado_frame, text="Leídos", variable=self.filtro_estado, 
                       value="leído", command=self.aplicar_filtro_estado).grid(row=0, column=1, padx=(0, 10))
        ttk.Radiobutton(estado_frame, text="Pendientes", variable=self.filtro_estado, 
                       value="pendiente", command=self.aplicar_filtro_estado).grid(row=0, column=2)
        
        # Búsqueda rápida
        ttk.Label(filtros_frame, text="Búsqueda rápida:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=3, padx=(20, 10))
        
        self.busqueda_var = tk.StringVar()
        busqueda_entry = ttk.Entry(filtros_frame, textvariable=self.busqueda_var, width=20)
        busqueda_entry.grid(row=0, column=4, padx=(0, 10))
        busqueda_entry.bind('<KeyRelease>', self.busqueda_en_tiempo_real)
        
        ttk.Button(filtros_frame, text="🔍 Buscar por Referencia", 
                  command=self.buscar_libro_avanzado, style="Primary.TButton").grid(row=0, column=5, padx=(10, 0))
    
    def crear_contenido_principal(self, parent):
        """Crea el contenido principal con formulario y tabla"""
        # Frame izquierdo para formulario
        form_frame = ttk.LabelFrame(parent, text="📝 Datos del Libro", 
                                   style="Card.TLabelframe", padding="20")
        form_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        
        self.crear_formulario(form_frame)
        
        # Frame derecho para la tabla
        table_frame = ttk.LabelFrame(parent, text="📋 Lista de Libros", 
                                    style="Card.TLabelframe", padding="15")
        table_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        self.crear_tabla(table_frame)
    
    def crear_formulario(self, parent):
        """Crea el formulario de entrada de datos"""
        # Referencia con validación
        ttk.Label(parent, text="Referencia *:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.referencia_var = tk.StringVar()
        self.referencia_entry = ttk.Entry(parent, textvariable=self.referencia_var, width=30, font=('Segoe UI', 10))
        self.referencia_entry.grid(row=0, column=1, pady=(0, 5), padx=(10, 0))
        ttk.Label(parent, text="(3 letras + 3 números, ej: ABC123)", 
                 font=('Segoe UI', 8), foreground='#6c757d').grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        # Validación en tiempo real para referencia
        self.referencia_var.trace('w', self.validar_referencia_tiempo_real)
        
        # Nombre
        ttk.Label(parent, text="Nombre *:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(parent, textvariable=self.nombre_var, width=30, font=('Segoe UI', 10))
        self.nombre_entry.grid(row=1, column=1, pady=(10, 5), padx=(10, 0))
        
        # Autor
        ttk.Label(parent, text="Autor *:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.autor_var = tk.StringVar()
        self.autor_entry = ttk.Entry(parent, textvariable=self.autor_var, width=30, font=('Segoe UI', 10))
        self.autor_entry.grid(row=2, column=1, pady=(10, 5), padx=(10, 0))
        
        # Año con validación mejorada
        ttk.Label(parent, text="Año *:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        self.anio_var = tk.StringVar()
        self.anio_entry = ttk.Entry(parent, textvariable=self.anio_var, width=30, font=('Segoe UI', 10))
        self.anio_entry.grid(row=3, column=1, pady=(10, 5), padx=(10, 0))
        ttk.Label(parent, text="(1 - año actual)", 
                 font=('Segoe UI', 8), foreground='#6c757d').grid(row=3, column=2, sticky=tk.W, padx=(10, 0))
        
        # Validación en tiempo real para anio
        self.anio_var.trace('w', self.validar_anio_tiempo_real)
        
        # Género con selector
        ttk.Label(parent, text="Género *:", font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        self.genero_var = tk.StringVar()
        self.genero_combo = ttk.Combobox(parent, textvariable=self.genero_var, 
                                        values=self.generos_literarios, width=27, 
                                        state="readonly", font=('Segoe UI', 10))
        self.genero_combo.grid(row=4, column=1, pady=(10, 5), padx=(10, 0))
        
        # Estado
        ttk.Label(parent, text="Estado *:", font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        self.estado_var = tk.StringVar(value="pendiente")
        self.estado_combo = ttk.Combobox(parent, textvariable=self.estado_var, 
                                        values=["pendiente", "leído"], width=27, 
                                        state="readonly", font=('Segoe UI', 10))
        self.estado_combo.grid(row=5, column=1, pady=(10, 5), padx=(10, 0))
        
        # Fecha Inicio con selector de calendario
        ttk.Label(parent, text="Fecha Inicio:", font=('Segoe UI', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=(10, 5))
        fecha_inicio_frame = ttk.Frame(parent)
        fecha_inicio_frame.grid(row=6, column=1, pady=(10, 5), padx=(10, 0), sticky=tk.W)
        
        self.fecha_inicio_cal = DateEntry(fecha_inicio_frame, width=20, background='#007bff',
                                         foreground='white', borderwidth=2, 
                                         date_pattern='yyyy-mm-dd', font=('Segoe UI', 10))
        self.fecha_inicio_cal.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(fecha_inicio_frame, text="🗑️", width=3,
                  command=lambda: self.fecha_inicio_cal.set_date(None),
                  style="Secondary.TButton").grid(row=0, column=1)
        
        # Fecha Final con selector de calendario
        ttk.Label(parent, text="Fecha Final:", font=('Segoe UI', 10, 'bold')).grid(row=7, column=0, sticky=tk.W, pady=(10, 5))
        fecha_final_frame = ttk.Frame(parent)
        fecha_final_frame.grid(row=7, column=1, pady=(10, 5), padx=(10, 0), sticky=tk.W)
        
        self.fecha_final_cal = DateEntry(fecha_final_frame, width=20, background='#007bff',
                                        foreground='white', borderwidth=2,
                                        date_pattern='yyyy-mm-dd', font=('Segoe UI', 10))
        self.fecha_final_cal.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(fecha_final_frame, text="🗑️", width=3,
                  command=lambda: self.fecha_final_cal.set_date(None),
                  style="Secondary.TButton").grid(row=0, column=1)
        
        # Etiqueta de campos obligatorios
        ttk.Label(parent, text="* Campos obligatorios", 
                 font=('Segoe UI', 9, 'italic'), foreground='#dc3545').grid(row=8, column=0, columnspan=3, pady=(15, 10))
        
        # Botones de acción
        self.crear_botones_accion(parent)
    
    def crear_botones_accion(self, parent):
        """Crea los botones de acción del formulario"""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.grid(row=9, column=0, columnspan=3, pady=(0, 0))
        
        # Primera fila de botones
        ttk.Button(buttons_frame, text="➕ Agregar", command=self.agregar_libro, 
                  style="Success.TButton", width=12).grid(row=0, column=0, padx=5, pady=1)
        ttk.Button(buttons_frame, text="✏️ Modificar", command=self.modificar_libro, 
                  style="Primary.TButton", width=12).grid(row=0, column=1, padx=5, pady=1)
        ttk.Button(buttons_frame, text="🗑️ Eliminar", command=self.eliminar_libro, 
                  style="Danger.TButton", width=12).grid(row=0, column=2, padx=5, pady=1)
        
        # Segunda fila de botones
        ttk.Button(buttons_frame, text="🧹 Limpiar", command=self.limpiar_campos,
                  style="Secondary.TButton", width=12).grid(row=1, column=0, padx=1, pady=2)
        ttk.Button(buttons_frame, text="🔄 Actualizar", command=self.cargar_libros, 
                  style="Secondary.TButton", width=12).grid(row=1, column=1, padx=1, pady=2)
        ttk.Button(buttons_frame, text="✅ Validar", command=self.validar_todos_campos, 
                  style="Secondary.TButton", width=12).grid(row=1, column=2, padx=1, pady=2)
    
    def crear_tabla(self, parent):
        """Crea la tabla de libros"""
        # Crear Treeview con estilo moderno
        columns = ("Referencia", "Nombre", "Autor", "Año", "Género", "Estado", "F. Inicio", "F. Final")
        self.tree = Treeview(parent, columns=columns, show="headings", height=18, style="Modern.Treeview")
        
        # Configurar columnas
        column_widths = {
            "Referencia": 100,
            "Nombre": 250,
            "Autor": 180,
            "Año": 80,
            "Género": 140,
            "Estado": 100,
            "F. Inicio": 100,
            "F. Final": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor='center' if col in ["Año", "Estado", "F. Inicio", "F. Final"] else 'w')
        
        # Scrollbars con estilo
        v_scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid para tabla y scrollbars
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind para selección en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Configurar colores alternados para las filas
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('leido', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('pendiente', background='#fff3cd', foreground='#856404')
        self.tree.tag_configure('encontrado', background='#cce5ff', foreground='#004085')
    
    def crear_footer(self, parent):
        """Crea el footer con estadísticas"""
        footer_frame = ttk.LabelFrame(parent, text="📊 Estadísticas y Acciones", 
                                     style="Card.TLabelframe", padding="15")
        footer_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Estadísticas en tiempo real
        self.stats_label = ttk.Label(footer_frame, text="", font=('Segoe UI', 10))
        self.stats_label.grid(row=0, column=0, padx=(0, 20))
        
        # Botones de estadísticas
        ttk.Button(footer_frame, text="📈 Ver Estadísticas Detalladas", 
                  command=self.mostrar_estadisticas, style="Primary.TButton").grid(row=0, column=1, padx=10)
        ttk.Button(footer_frame, text="🏷️ Filtrar por Género", 
                  command=self.filtrar_por_genero, style="Primary.TButton").grid(row=0, column=2, padx=10)
        
        # Actualizar estadísticas iniciales
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas en tiempo real"""
        try:
            stats = self.libros_dao.contar_por_estado()
            total = sum(stats.values()) if stats else 0
            leidos = stats.get('leído', 0)
            pendientes = stats.get('pendiente', 0)
            
            texto_stats = f"📚 Total: {total} libros | ✅ Leídos: {leidos} | ⏳ Pendientes: {pendientes}"
            if total > 0:
                porcentaje_leidos = (leidos / total) * 100
                texto_stats += f" | 📊 Progreso: {porcentaje_leidos:.1f}%"
            
            self.stats_label.config(text=texto_stats)
        except:
            self.stats_label.config(text="📚 Estadísticas no disponibles")
    
    def aplicar_filtro_estado(self):
        """Aplica el filtro por estado de lectura"""
        filtro = self.filtro_estado.get()
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar libros según filtro
        libros = self.libros_dao.libros()
        libros_filtrados = []
        
        if filtro == "todos":
            libros_filtrados = libros
        else:
            libros_filtrados = [libro for libro in libros if libro.estado == filtro]
        
        # Mostrar libros filtrados
        for i, libro in enumerate(libros_filtrados):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            if libro.estado == 'leído':
                tag = 'leido'
            elif libro.estado == 'pendiente':
                tag = 'pendiente'
            
            self.tree.insert("", "end", values=(
                libro.referencia,
                libro.nombre,
                libro.autor,
                libro.anio,
                libro.genero or "",
                libro.estado,
                libro.fecha_inicio or "",
                libro.fecha_fin or ""
            ), tags=(tag,))
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def busqueda_en_tiempo_real(self, event):
        """Búsqueda en tiempo real mientras se escribe"""
        termino = self.busqueda_var.get().lower()
        
        if not termino:
            self.aplicar_filtro_estado()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar en todos los campos
        libros = self.libros_dao.libros()
        libros_encontrados = []
        
        for libro in libros:
            if (termino in libro.referencia.lower() or 
                termino in libro.nombre.lower() or 
                termino in libro.autor.lower() or 
                termino in str(libro.anio) or
                (libro.genero and termino in libro.genero.lower())):
                libros_encontrados.append(libro)
        
        # Mostrar resultados
        for i, libro in enumerate(libros_encontrados):
            tag = 'encontrado'
            
            self.tree.insert("", "end", values=(
                libro.referencia,
                libro.nombre,
                libro.autor,
                libro.anio,
                libro.genero or "",
                libro.estado,
                libro.fecha_inicio or "",
                libro.fecha_fin or ""
            ), tags=(tag,))
    
    def buscar_libro_avanzado(self):
        """Búsqueda avanzada por referencia con resaltado"""
        referencia = simpledialog.askstring("🔍 Buscar Libro", 
                                           "Ingrese la referencia del libro (formato AAA111):",
                                           parent=self.root)
        if referencia:
            referencia = referencia.upper().strip()
            if not self.validar_formato_referencia(referencia):
                messagebox.showerror("❌ Error", "La referencia debe tener el formato AAA111")
                return
            
            libro = Libros(referencia=referencia)
            if self.libros_dao.busca_libro(libro):
                # Llenar campos con los datos encontrados
                self.referencia_var.set(libro.referencia)
                self.nombre_var.set(libro.nombre)
                self.autor_var.set(libro.autor)
                self.anio_var.set(libro.anio)
                self.genero_var.set(libro.genero or "")
                self.estado_var.set(libro.estado)
                
                # Manejar fechas
                try:
                    if libro.fecha_inicio:
                        self.fecha_inicio_cal.set_date(libro.fecha_inicio)
                    else:
                        self.fecha_inicio_cal.set_date(None)
                except:
                    self.fecha_inicio_cal.set_date(None)
                
                try:
                    if libro.fecha_fin:
                        self.fecha_final_cal.set_date(libro.fecha_fin)
                    else:
                        self.fecha_final_cal.set_date(None)
                except:
                    self.fecha_final_cal.set_date(None)
                
                # Resaltar en la tabla
                self.resaltar_libro_en_tabla(referencia)
                
                # Mostrar información del libro encontrado
                info_mensaje = f"""📖 Libro Encontrado:
                
📚 Título: {libro.nombre}
✍️ Autor: {libro.autor}
📅 Año: {libro.anio}
🏷️ Género: {libro.genero or 'No especificado'}
📊 Estado: {libro.estado}
📆 Fecha inicio: {libro.fecha_inicio or 'No especificada'}
📆 Fecha final: {libro.fecha_fin or 'No especificada'}"""
                
                messagebox.showinfo("✅ Libro Encontrado", info_mensaje)
            else:
                self.limpiar_campos()
                messagebox.showwarning("⚠️ No Encontrado", 
                                     f"No se encontró ningún libro con la referencia '{referencia}'")
    
    def resaltar_libro_en_tabla(self, referencia):
        """Resalta un libro específico en la tabla"""
        # Primero cargar todos los libros
        self.cargar_libros()
        
        # Buscar y resaltar el libro
        for item in self.tree.get_children():
            valores = self.tree.item(item)['values']
            if valores[0] == referencia:  # Referencia está en la primera columna
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                # Cambiar el tag para resaltado especial
                self.tree.item(item, tags=('encontrado',))
                break
    
    # Métodos de validación (sin cambios significativos)
    def validar_referencia_tiempo_real(self, *args):
        """Validación en tiempo real para el formato de referencia"""
        referencia = self.referencia_var.get().upper()
        if referencia != self.referencia_var.get():
            self.referencia_var.set(referencia)
        
        if len(referencia) == 0:
            self.referencia_entry.configure(style="TEntry")
        elif self.validar_formato_referencia(referencia):
            self.referencia_entry.configure(style="Valid.TEntry")
        else:
            self.referencia_entry.configure(style="Invalid.TEntry")
    
    def validar_anio_tiempo_real(self, *args):
        """Validación en tiempo real para el anio"""
        anio_str = self.anio_var.get()
        
        if len(anio_str) == 0:
            self.anio_entry.configure(style="TEntry")
        elif self.validar_anio(anio_str):
            self.anio_entry.configure(style="Valid.TEntry")
        else:
            self.anio_entry.configure(style="Invalid.TEntry")
    
    def validar_formato_referencia(self, referencia):
        """Valida que la referencia tenga el formato AAA111"""
        patron = r'^[A-Z]{3}[0-9]{3}$'
        return bool(re.match(patron, referencia))
    
    def validar_anio(self, anio_str):
        """Valida que el anio sea un número válido en el rango permitido"""
        try:
            anio = int(anio_str)
            anio_actual = datetime.now().year
            return anio <= anio_actual
        except ValueError:
            return False
    
    def cargar_libros(self):
        """Carga los libros en la tabla con colores alternados"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Cargar libros desde la base de datos
        libros = self.libros_dao.libros()
        for i, libro in enumerate(libros):
            # Determinar el tag según el estado y la fila
            if libro.estado == 'leído':
                tag = 'leido'
            elif libro.estado == 'pendiente':
                tag = 'pendiente'
            else:
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            
            self.tree.insert("", "end", values=(
                libro.referencia,
                libro.nombre,
                libro.autor,
                libro.anio,
                libro.genero or "",
                libro.estado,
                libro.fecha_inicio or "",
                libro.fecha_fin or ""
            ), tags=(tag,))
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def on_select(self, event):
        """Maneja la selección de elementos en la tabla"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Llenar campos con los datos seleccionados
            self.referencia_var.set(values[0])
            self.nombre_var.set(values[1])
            self.autor_var.set(values[2])
            self.anio_var.set(values[3])
            self.genero_var.set(values[4])
            self.estado_var.set(values[5])
            
            # Manejar fechas
            try:
                if values[6]:
                    fecha_inicio = datetime.strptime(str(values[6]), "%Y-%m-%d").date()
                    self.fecha_inicio_cal.set_date(fecha_inicio)
                else:
                    self.fecha_inicio_cal.set_date(None)
            except:
                self.fecha_inicio_cal.set_date(None)
            
            try:
                if values[7]:
                    fecha_final = datetime.strptime(str(values[7]), "%Y-%m-%d").date()
                    self.fecha_final_cal.set_date(fecha_final)
                else:
                    self.fecha_final_cal.set_date(None)
            except:
                self.fecha_final_cal.set_date(None)
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.referencia_var.set("")
        self.nombre_var.set("")
        self.autor_var.set("")
        self.anio_var.set("")
        self.genero_var.set("")
        self.estado_var.set("pendiente")
        self.fecha_inicio_cal.set_date(None)
        self.fecha_final_cal.set_date(None)
        self.busqueda_var.set("")
        
        # Limpiar selección de la tabla
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        # Resetear estilos
        self.referencia_entry.configure(style="TEntry")
        self.anio_entry.configure(style="TEntry")
        
        # Recargar tabla sin filtros
        self.filtro_estado.set("todos")
        self.cargar_libros()
    
    def validar_campos_obligatorios(self):
        """Valida que todos los campos obligatorios estén llenos y sean válidos"""
        errores = []
        
        # Validar referencia
        referencia = self.referencia_var.get().strip()
        if not referencia:
            errores.append("La referencia es obligatoria")
        elif not self.validar_formato_referencia(referencia):
            errores.append("La referencia debe tener el formato AAA111 (3 letras + 3 números)")
        
        # Validar nombre
        if not self.nombre_var.get().strip():
            errores.append("El nombre es obligatorio")
        
        # Validar autor
        if not self.autor_var.get().strip():
            errores.append("El autor es obligatorio")
        
        # Validar anio
        anio_str = self.anio_var.get().strip()
        if not anio_str:
            errores.append("El anio es obligatorio")
        elif not self.validar_anio(anio_str):
            errores.append("El anio debe ser un número válido entre 1000 y el anio actual")
        
        # Validar género
        if not self.genero_var.get():
            errores.append("El género es obligatorio")
        
        # Validar estado
        if not self.estado_var.get():
            errores.append("El estado es obligatorio")
        
        return errores
    
    def validar_fechas(self):
        """Valida que las fechas sean coherentes"""
        errores = []
        
        try:
            fecha_inicio = self.fecha_inicio_cal.get_date()
            fecha_final = self.fecha_final_cal.get_date()
            
            if fecha_inicio and fecha_final:
                if fecha_inicio > fecha_final:
                    errores.append("La fecha de inicio no puede ser posterior a la fecha final")
            

        except:
            pass
        
        return errores
    
    def validar_todos_campos(self):
        """Función para validar todos los campos manualmente"""
        errores = self.validar_campos_obligatorios()
        errores.extend(self.validar_fechas())
        
        if errores:
            mensaje = "❌ Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
            messagebox.showerror("Errores de Validación", mensaje)
        else:
            messagebox.showinfo("✅ Validación", "¡Todos los campos son válidos!")
    
    def crear_libro_desde_campos(self):
        """Crea un objeto Libro desde los campos del formulario"""
        # Validar campos obligatorios
        errores = self.validar_campos_obligatorios()
        errores.extend(self.validar_fechas())
        
        if errores:
            mensaje = "❌ Errores encontrados:\n\n" + "\n".join(f"• {error}" for error in errores)
            messagebox.showerror("Errores de Validación", mensaje)
            return None
        
        # Obtener fechas
        fecha_inicio = None
        fecha_final = None
        
        try:
            fecha_inicio = self.fecha_inicio_cal.get_date()
        except:
            fecha_inicio = None
        
        try:
            fecha_final = self.fecha_final_cal.get_date()
        except:
            fecha_final = None
        
        return Libros(
            anio=int(self.anio_var.get()),
            referencia=self.referencia_var.get().strip().upper(),
            autor=self.autor_var.get().strip(),
            nombre=self.nombre_var.get().strip(),
            genero=self.genero_var.get(),
            estado=self.estado_var.get(),
            fecha_inicio=fecha_inicio,
            fecha_fin=None if self.estado_var.get() == "pendiente" else fecha_final
        )
    
    def agregar_libro(self):
        """Agrega un nuevo libro"""
        libro = self.crear_libro_desde_campos()
        if libro is None:
            return
        
        if self.libros_dao.agregar_libro(libro):
            messagebox.showinfo("✅ Éxito", "¡Libro agregado correctamente!")
            self.cargar_libros()
            self.limpiar_campos()
        else:
            messagebox.showerror("❌ Error", "No se pudo agregar el libro. Verifique que la referencia no exista.")
    
    def modificar_libro(self):
        """Modifica un libro existente"""
        if not self.tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Seleccione un libro de la tabla")
            return
        
        libro = self.crear_libro_desde_campos()
        if libro is None:
            return
        
        if self.libros_dao.modificar_libro(libro):
            messagebox.showinfo("✅ Éxito", "¡Libro modificado correctamente!")
            self.cargar_libros()
            self.limpiar_campos()
        else:
            messagebox.showerror("❌ Error", "No se pudo modificar el libro")
    
    def eliminar_libro(self):
        """Elimina un libro"""
        if not self.tree.selection():
            messagebox.showwarning("⚠️ Advertencia", "Seleccione un libro de la tabla")
            return
        
        if messagebox.askyesno("🗑️ Confirmar Eliminación", 
                              "¿Está seguro de eliminar este libro?\n\nEsta acción no se puede deshacer."):
            libro = Libros(referencia=self.referencia_var.get())
            
            if self.libros_dao.eliminar_libro(libro):
                messagebox.showinfo("✅ Éxito", "¡Libro eliminado correctamente!")
                self.cargar_libros()
                self.limpiar_campos()
            else:
                messagebox.showerror("❌ Error", "No se pudo eliminar el libro")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas"""
        stats = self.libros_dao.contar_por_estado()
        if stats:
            mensaje = "📊 Estadísticas Detalladas de la Biblioteca:\n\n"
            total = sum(stats.values())
            
            for estado, cantidad in stats.items():
                porcentaje = (cantidad / total) * 100
                emoji = "✅" if estado == "leído" else "⏳"
                mensaje += f"{emoji} {estado.capitalize()}: {cantidad} libros ({porcentaje:.1f}%)\n"
            
            mensaje += f"\n📚 Total de libros: {total}"
            
            if total > 0:
                progreso = (stats.get('leído', 0) / total) * 100
                mensaje += f"\n🎯 Progreso de lectura: {progreso:.1f}%"
                
                if progreso >= 80:
                    mensaje += "\n🏆 ¡Excelente progreso de lectura!"
                elif progreso >= 50:
                    mensaje += "\n👍 Buen progreso de lectura"
                else:
                    mensaje += "\n📖 ¡Anímate a leer más libros!"
            
            messagebox.showinfo("📊 Estadísticas de la Biblioteca", mensaje)
        else:
            messagebox.showinfo("📊 Estadísticas", "No hay datos disponibles")
    
    def filtrar_por_genero(self):
        """Filtrar libros por género con ventana mejorada"""
        # Crear ventana de selección de género
        ventana_genero = tk.Toplevel(self.root)
        ventana_genero.title("🏷️ Filtrar por Género")
        ventana_genero.geometry("400x500")
        ventana_genero.transient(self.root)
        ventana_genero.grab_set()
        ventana_genero.configure(bg='#f8f9fa')
        
        # Aplicar tema a la ventana
        style = ThemedStyle(ventana_genero)
        style.set_theme("arc")
        
        # Frame principal
        main_frame = ttk.Frame(ventana_genero, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="🏷️ Seleccione un género:", 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 15))
        
        # Frame para la lista con scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Lista de géneros con scrollbar
        listbox = tk.Listbox(list_frame, height=15, font=('Segoe UI', 10),
                            selectbackground='#007bff', selectforeground='white')
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for genero in self.generos_literarios:
            listbox.insert(tk.END, genero)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        def aplicar_filtro():
            seleccion = listbox.curselection()
            if seleccion:
                genero = listbox.get(seleccion[0])
                libros = self.libros_dao.libros_por_genero(genero)

                # Limpiar tabla
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Mostrar libros filtrados
                for i, libro in enumerate(libros):
                    tag = 'encontrado'
                    
                    self.tree.insert("", "end", values=(
                        libro.referencia,
                        libro.nombre,
                        libro.autor,
                        libro.anio,
                        libro.genero or "",
                        libro.estado,
                        libro.fecha_inicio or "",
                        libro.fecha_fin or ""
                    ), tags=(tag,))

                messagebox.showinfo("🏷️ Filtro Aplicado", 
                                   f"Se encontraron {len(libros)} libros del género '{genero}'")
                ventana_genero.destroy()
            else:
                messagebox.showwarning("⚠️ Advertencia", "Seleccione un género")

        ttk.Button(button_frame, text="✅ Aplicar Filtro", command=aplicar_filtro,
                  style="Success.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Cancelar", command=ventana_genero.destroy,
                  style="Secondary.TButton").pack(side=tk.LEFT)

