import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess
import traceback

# Importações condicionais
try:
    import cv2
    OPENCV_AVAILABLE = True
    print("🔧 [DEBUG] OpenCV carregado com sucesso")
except ImportError:
    OPENCV_AVAILABLE = False
    print("⚠️  [DEBUG] OpenCV não disponível")

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
    print("🔧 [DEBUG] tkinterdnd2 carregado com sucesso")
except ImportError:
    DND_AVAILABLE = False
    print("⚠️  [DEBUG] tkinterdnd2 não disponível")

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
    print("🔧 [DEBUG] Pillow carregado com sucesso")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  [DEBUG] Pillow não disponível")

from video_converter import VideoConverter

class VideoConverterGUILite:
    def __init__(self):
        print("🚀 [DEBUG] Iniciando VideoConverterGUILite...")
        
        # SEMPRE usar tkinter padrão primeiro
        print("🔧 [DEBUG] Criando janela tkinter padrão...")
        self.root = tk.Tk()
        print(f"🔧 [DEBUG] Janela tkinter criada: {type(self.root)}")
        
        self.dnd_enabled = False
        
        # Tentar atualizar para TkinterDnD apenas se disponível
        if DND_AVAILABLE:
            try:
                print("🔧 [DEBUG] Tentando inicializar TkinterDnD...")
                # Destruir a janela tk padrão
                self.root.destroy()
                print("🔧 [DEBUG] Janela tkinter padrão destruída")
                
                # Criar nova janela com TkinterDnD
                self.root = TkinterDnD.Tk()
                print(f"🔧 [DEBUG] Janela TkinterDnD criada: {type(self.root)}")
                
                self.dnd_enabled = True
                print("✅ [DEBUG] TkinterDnD inicializado com sucesso")
            except Exception as e:
                print(f"❌ [DEBUG] Erro ao inicializar TkinterDnD: {e}")
                print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
                print("🔄 [DEBUG] Voltando para tkinter padrão...")
                # Recriar janela padrão se TkinterDnD falhar
                self.root = tk.Tk()
                self.dnd_enabled = False
                print(f"🔧 [DEBUG] Janela tkinter padrão recriada: {type(self.root)}")
        
        print(f"🔧 [DEBUG] Estado final - dnd_enabled: {self.dnd_enabled}")
        
        self.root.title("Conversor de Vídeo Universal - Ultra Debug v3.0")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Configurar estilo
        print("🔧 [DEBUG] Configurando estilos...")
        self.setup_styles()
        
        # Variáveis
        print("🔧 [DEBUG] Inicializando VideoConverter...")
        self.converter = VideoConverter()
        print(f"🔧 [DEBUG] VideoConverter criado: {type(self.converter)}")
        
        self.input_files = []
        print("🔧 [DEBUG] Lista de arquivos inicializada")
        
        # ✅ CORREÇÃO: Passar self.root explicitamente como master
        print("🔧 [DEBUG] Criando variáveis tkinter...")
        try:
            self.output_directory = tk.StringVar(master=self.root)
            print(f"🔧 [DEBUG] output_directory criada: {type(self.output_directory)}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao criar output_directory: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            raise
        
        self.is_converting = False
        print("🔧 [DEBUG] is_converting inicializado")
        
        # ✅ CORREÇÃO: Configurações com master explícito
        print("🔧 [DEBUG] Criando configurações...")
        try:
            self.settings = {
                'output_format': tk.StringVar(master=self.root, value='mp4'),
                'quality': tk.StringVar(master=self.root, value='medium'),
                'audio_only': tk.BooleanVar(master=self.root, value=False),
                'overwrite': tk.BooleanVar(master=self.root, value=True)
            }
            print("🔧 [DEBUG] Configurações criadas com sucesso")
            for key, var in self.settings.items():
                print(f"🔧 [DEBUG] {key}: {type(var)} = {var.get()}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao criar configurações: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            raise
        
        # Criar interface
        print("🔧 [DEBUG] Criando widgets...")
        self.create_widgets()
        
        print("🔧 [DEBUG] Carregando configurações...")
        self.load_settings()
        
        # Configurar drag-drop apenas se habilitado
        print(f"🔧 [DEBUG] Verificando drag-drop: dnd_enabled={self.dnd_enabled}, hasattr(drop_area)={hasattr(self, 'drop_area')}")
        if self.dnd_enabled and hasattr(self, 'drop_area'):
            print("🔧 [DEBUG] Configurando drag-drop...")
            self.setup_drag_drop()
        else:
            print("⚠️  [DEBUG] Drag-drop não configurado")
        
        # Verificar FFmpeg
        print("🔧 [DEBUG] Verificando FFmpeg...")
        self.check_ffmpeg_on_startup()
        
        print("✅ [DEBUG] Inicialização concluída com sucesso!")
    
    def setup_styles(self):
        """Configurar estilos básicos"""
        try:
            print("🔧 [DEBUG] Aplicando tema clam...")
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
            print("✅ [DEBUG] Estilos configurados com sucesso")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao configurar estilos: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        print("🔧 [DEBUG] Iniciando criação de widgets...")
        
        # Frame principal
        print("🔧 [DEBUG] Criando frame principal...")
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Seções
        print("🔧 [DEBUG] Criando seções...")
        self.create_input_section(main_frame)
        self.create_settings_section(main_frame)
        self.create_output_section(main_frame)
        self.create_conversion_section(main_frame)
        self.create_status_section(main_frame)
        
        print("✅ [DEBUG] Widgets criados com sucesso")
    
    def create_input_section(self, parent):
        """Criar seção de entrada de arquivos"""
        print("🔧 [DEBUG] Criando seção de entrada...")
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(parent, text="📁 Arquivos de Entrada", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # ✅ CORREÇÃO: Usar relief válido
        print("🔧 [DEBUG] Criando área de drop...")
        try:
            if self.dnd_enabled:
                print("🔧 [DEBUG] Criando drop_area com DnD habilitado...")
                # ✅ CORREÇÃO: Usar 'ridge' em vez de 'dashed'
                self.drop_area = tk.Frame(input_frame, bg='#ecf0f1', relief='ridge', bd=2, height=80)
                self.drop_area.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                self.drop_area.grid_propagate(False)
                
                drop_label = tk.Label(self.drop_area, text="🎬 Arraste arquivos de vídeo aqui ou clique para selecionar",
                                    bg='#ecf0f1', font=('Arial', 10))
                drop_label.place(relx=0.5, rely=0.5, anchor='center')
                drop_label.bind('<Button-1>', lambda e: self.select_input_file())
                self.drop_area.bind('<Button-1>', lambda e: self.select_input_file())
                print("✅ [DEBUG] Drop area criada com sucesso (DnD habilitado)")
            else:
                print("🔧 [DEBUG] Criando drop_area sem DnD...")
                # ✅ CORREÇÃO: Usar 'ridge' em vez de 'dashed'
                self.drop_area = tk.Frame(input_frame, bg='#f8f9fa', relief='ridge', bd=2, height=80)
                self.drop_area.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                self.drop_area.grid_propagate(False)
                
                drop_label = tk.Label(self.drop_area, text="🎬 Clique para selecionar arquivos de vídeo\n(Drag & Drop não disponível)",
                                    bg='#f8f9fa', font=('Arial', 10))
                drop_label.place(relx=0.5, rely=0.5, anchor='center')
                drop_label.bind('<Button-1>', lambda e: self.select_input_file())
                self.drop_area.bind('<Button-1>', lambda e: self.select_input_file())
                print("✅ [DEBUG] Drop area criada com sucesso (DnD desabilitado)")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao criar área de drop: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            # Fallback: criar botão simples
            print("🔧 [DEBUG] Criando fallback button...")
            select_btn = ttk.Button(input_frame, text="Selecionar Arquivos", command=self.select_input_file)
            select_btn.grid(row=0, column=0, pady=(0, 10))
        
        # Lista de arquivos
        print("🔧 [DEBUG] Criando lista de arquivos...")
        list_frame = ttk.Frame(input_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, height=6)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botões
        print("🔧 [DEBUG] Criando botões de entrada...")
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, pady=(10, 0))
        
        ttk.Button(btn_frame, text="➕ Adicionar Arquivos", command=self.select_input_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="📁 Adicionar Pasta", command=self.select_input_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Limpar Lista", command=self.clear_input).pack(side=tk.LEFT)
        
        print("✅ [DEBUG] Seção de entrada criada com sucesso")
    
    def create_settings_section(self, parent):
        """Criar seção de configurações"""
        print("🔧 [DEBUG] Criando seção de configurações...")
        
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Formato de saída
        ttk.Label(settings_frame, text="Formato:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        format_combo = ttk.Combobox(settings_frame, textvariable=self.settings['output_format'],
                                   values=['mp4', 'avi', 'mkv', 'mov', 'mp3', 'wav', 'aac'], width=10)
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Qualidade
        ttk.Label(settings_frame, text="Qualidade:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.settings['quality'],
                                    values=['low', 'medium', 'high', 'best'], width=10)
        quality_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Opções
        ttk.Checkbutton(settings_frame, text="Apenas áudio", variable=self.settings['audio_only']).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        ttk.Checkbutton(settings_frame, text="Sobrescrever arquivos", variable=self.settings['overwrite']).grid(row=1, column=2, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        print("✅ [DEBUG] Seção de configurações criada")
    
    def create_output_section(self, parent):
        """Criar seção de saída"""
        print("🔧 [DEBUG] Criando seção de saída...")
        
        output_frame = ttk.LabelFrame(parent, text="📤 Pasta de Saída", padding="10")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10), padx=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        
        # Entrada de diretório
        dir_frame = ttk.Frame(output_frame)
        dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        dir_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(dir_frame, textvariable=self.output_directory)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(dir_frame, text="📁", command=self.select_output_directory, width=3).grid(row=0, column=1)
        
        # Definir diretório padrão
        self.output_directory.set(os.path.expanduser("~/Desktop"))
        
        print("✅ [DEBUG] Seção de saída criada")
    
    def create_conversion_section(self, parent):
        """Criar seção de conversão"""
        print("🔧 [DEBUG] Criando seção de conversão...")
        
        conversion_frame = ttk.LabelFrame(parent, text="🔄 Conversão", padding="10")
        conversion_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        conversion_frame.columnconfigure(0, weight=1)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar(master=self.root)
        self.progress_bar = ttk.Progressbar(conversion_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botões
        btn_frame = ttk.Frame(conversion_frame)
        btn_frame.grid(row=1, column=0)
        
        self.convert_btn = ttk.Button(btn_frame, text="🚀 Iniciar Conversão", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹️ Parar", command=self.stop_conversion, state='disabled')
        self.stop_btn.pack(side=tk.LEFT)
        
        print("✅ [DEBUG] Seção de conversão criada")
    
    def create_status_section(self, parent):
        """Criar seção de status"""
        print("🔧 [DEBUG] Criando seção de status...")
        
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Área de texto para logs
        text_frame = ttk.Frame(status_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.status_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        status_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.status_text.yview)
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        # Status inicial
        self.update_status("✅ Interface carregada. Selecione arquivos para converter.")
        
        print("✅ [DEBUG] Seção de status criada")
    
    def setup_drag_drop(self):
        """Configurar funcionalidade de drag and drop"""
        print("🔧 [DEBUG] Configurando drag and drop...")
        
        try:
            if self.dnd_enabled and hasattr(self, 'drop_area'):
                print(f"🔧 [DEBUG] drop_area type: {type(self.drop_area)}")
                
                self.drop_area.drop_target_register(DND_FILES)
                self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
                
                print("✅ [DEBUG] Drag and drop configurado com sucesso")
            else:
                print("⚠️  [DEBUG] Drag and drop não pode ser configurado")
                print(f"🔧 [DEBUG] dnd_enabled: {self.dnd_enabled}")
                print(f"🔧 [DEBUG] hasattr drop_area: {hasattr(self, 'drop_area')}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao configurar drag and drop: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def on_drop(self, event):
        """Processar arquivos arrastados"""
        print(f"🔧 [DEBUG] Arquivos arrastados: {event.data}")
        
        try:
            files = self.root.tk.splitlist(event.data)
            print(f"🔧 [DEBUG] Arquivos processados: {files}")
            
            for file_path in files:
                if os.path.isfile(file_path):
                    self.add_file(file_path)
                    print(f"✅ [DEBUG] Arquivo adicionado: {file_path}")
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao processar drop: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def select_input_file(self):
        """Selecionar arquivos de entrada"""
        print("🔧 [DEBUG] Abrindo seletor de arquivos...")
        
        try:
            files = filedialog.askopenfilenames(
                title="Selecionar arquivos de vídeo",
                filetypes=[
                    ("Vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ts *.m2ts"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            
            print(f"🔧 [DEBUG] Arquivos selecionados: {files}")
            
            for file_path in files:
                self.add_file(file_path)
                print(f"✅ [DEBUG] Arquivo adicionado: {file_path}")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao selecionar arquivos: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def select_input_folder(self):
        """Selecionar pasta de entrada"""
        print("🔧 [DEBUG] Abrindo seletor de pasta...")
        
        try:
            folder = filedialog.askdirectory(title="Selecionar pasta com vídeos")
            
            if folder:
                print(f"🔧 [DEBUG] Pasta selecionada: {folder}")
                
                video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.ts', '.m2ts']
                
                for file_path in Path(folder).iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                        self.add_file(str(file_path))
                        print(f"✅ [DEBUG] Arquivo da pasta adicionado: {file_path}")
                        
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao selecionar pasta: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def add_file(self, file_path):
        """Adicionar arquivo à lista"""
        print(f"🔧 [DEBUG] Adicionando arquivo: {file_path}")
        
        try:
            if file_path not in self.input_files:
                self.input_files.append(file_path)
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
                self.update_status(f"📁 Arquivo adicionado: {os.path.basename(file_path)}")
                print(f"✅ [DEBUG] Arquivo adicionado à lista: {file_path}")
            else:
                print(f"⚠️  [DEBUG] Arquivo já existe na lista: {file_path}")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao adicionar arquivo: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def clear_input(self):
        """Limpar lista de arquivos"""
        print("🔧 [DEBUG] Limpando lista de arquivos...")
        
        try:
            self.input_files.clear()
            self.file_listbox.delete(0, tk.END)
            self.update_status("🗑️ Lista de arquivos limpa")
            print("✅ [DEBUG] Lista limpa com sucesso")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao limpar lista: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def select_output_directory(self):
        """Selecionar diretório de saída"""
        print("🔧 [DEBUG] Abrindo seletor de diretório...")
        
        try:
            directory = filedialog.askdirectory(title="Selecionar pasta de saída")
            
            if directory:
                self.output_directory.set(directory)
                self.update_status(f"📤 Pasta de saída: {directory}")
                print(f"✅ [DEBUG] Diretório de saída selecionado: {directory}")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao selecionar diretório: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def start_conversion(self):
        """Iniciar processo de conversão"""
        print("🚀 [DEBUG] Iniciando conversão...")
        
        try:
            if not self.input_files:
                messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo para converter")
                print("⚠️  [DEBUG] Nenhum arquivo selecionado")
                return
            
            if not self.output_directory.get():
                messagebox.showwarning("Aviso", "Selecione uma pasta de saída")
                print("⚠️  [DEBUG] Pasta de saída não selecionada")
                return
            
            print(f"🔧 [DEBUG] Arquivos para converter: {len(self.input_files)}")
            print(f"🔧 [DEBUG] Pasta de saída: {self.output_directory.get()}")
            print(f"🔧 [DEBUG] Configurações: {[(k, v.get()) for k, v in self.settings.items()]}")
            
            self.is_converting = True
            self.convert_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.progress_var.set(0)
            
            # Iniciar conversão em thread separada
            print("🔧 [DEBUG] Iniciando thread de conversão...")
            conversion_thread = threading.Thread(target=self.convert_files, daemon=True)
            conversion_thread.start()
            print("✅ [DEBUG] Thread de conversão iniciada")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao iniciar conversão: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            self.update_status(f"❌ Erro ao iniciar conversão: {e}")
    
    def convert_files(self):
        """Converter arquivos (executado em thread separada)"""
        print("🔧 [DEBUG] Executando conversão de arquivos...")
        
        converted = 0
        total = len(self.input_files)
        
        try:
            for i, input_file in enumerate(self.input_files):
                if not self.is_converting:
                    print("⚠️  [DEBUG] Conversão interrompida pelo usuário")
                    break
                
                print(f"🔧 [DEBUG] Convertendo arquivo {i+1}/{total}: {input_file}")
                
                self.root.after(0, lambda: self.update_status(f"🔄 Convertendo {i+1}/{total}: {os.path.basename(input_file)}"))
                
                output_file = os.path.join(
                    self.output_directory.get(),
                    f"{Path(input_file).stem}.{self.settings['output_format'].get()}"
                )
                
                print(f"🔧 [DEBUG] Arquivo de saída: {output_file}")
                
                try:
                    # ✅ CORREÇÃO: Remover parâmetro output_format inválido
                    print("🔧 [DEBUG] Chamando converter.convert_video...")
                    print(f"🔧 [DEBUG] Parâmetros:")
                    print(f"  - input_file: {input_file}")
                    print(f"  - output_file: {output_file}")
                    print(f"  - quality: {self.settings['quality'].get()}")
                    
                    # Verificar se é conversão apenas de áudio
                    if self.settings['audio_only'].get():
                        print("🔧 [DEBUG] Conversão apenas de áudio")
                        success = self.converter.convert_to_audio(
                            input_file,
                            output_file,
                            audio_codec=self.settings['output_format'].get() if self.settings['output_format'].get() in ['mp3', 'aac', 'wav'] else 'mp3'
                        )
                    else:
                        print("🔧 [DEBUG] Conversão de vídeo")
                        success = self.converter.convert_video(
                            input_file,
                            output_file,
                            quality=self.settings['quality'].get()
                        )
                    
                    print(f"🔧 [DEBUG] Resultado da conversão: {success}")
                    
                    if success:
                        converted += 1
                        print(f"✅ [DEBUG] Conversão bem-sucedida: {output_file}")
                    else:
                        print(f"❌ [DEBUG] Falha na conversão: {input_file}")
                    
                    progress = ((i + 1) / total) * 100
                    self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    print(f"🔧 [DEBUG] Progresso: {progress:.1f}%")
                    
                except Exception as e:
                    print(f"❌ [DEBUG] Erro ao converter {input_file}: {e}")
                    print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
                    self.root.after(0, lambda err=str(e), file=input_file: self.update_status(f"❌ Erro ao converter {os.path.basename(file)}: {err}"))
            
            print(f"🔧 [DEBUG] Conversão finalizada: {converted}/{total} arquivos")
            self.root.after(0, lambda: self.conversion_finished(converted, total))
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro geral na conversão: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            self.root.after(0, lambda: self.update_status(f"❌ Erro geral na conversão: {e}"))
            self.root.after(0, lambda: self.conversion_finished(converted, total))
    
    def stop_conversion(self):
        """Parar conversão"""
        print("🛑 [DEBUG] Parando conversão...")
        
        try:
            self.is_converting = False
            self.update_status("⏹️ Conversão interrompida pelo usuário")
            print("✅ [DEBUG] Conversão parada")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao parar conversão: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def conversion_finished(self, converted, total):
        """Finalizar conversão"""
        print(f"🏁 [DEBUG] Conversão finalizada: {converted}/{total}")
        
        try:
            self.is_converting = False
            self.convert_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            
            if converted == total:
                self.update_status(f"✅ Conversão concluída! {converted}/{total} arquivos convertidos com sucesso")
                messagebox.showinfo("Sucesso", f"Conversão concluída!\n{converted}/{total} arquivos convertidos")
            else:
                self.update_status(f"⚠️ Conversão parcial: {converted}/{total} arquivos convertidos")
                messagebox.showwarning("Parcial", f"Conversão parcial\n{converted}/{total} arquivos convertidos")
                
            print("✅ [DEBUG] Finalização concluída")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao finalizar conversão: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def update_status(self, message):
        """Atualizar status"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            full_message = f"[{timestamp}] {message}\n"
            
            self.status_text.insert(tk.END, full_message)
            self.status_text.see(tk.END)
            
            print(f"📊 [DEBUG] Status: {message}")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao atualizar status: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def check_ffmpeg_on_startup(self):
        """Verificar FFmpeg na inicialização"""
        print("🔧 [DEBUG] Verificando FFmpeg...")
        
        try:
            if self.converter.check_ffmpeg():
                self.update_status("✅ FFmpeg encontrado e funcionando")
                print("✅ [DEBUG] FFmpeg OK")
            else:
                self.update_status("❌ FFmpeg não encontrado! Instale o FFmpeg para usar o conversor")
                print("❌ [DEBUG] FFmpeg não encontrado")
                messagebox.showerror("Erro", "FFmpeg não encontrado!\n\nInstale o FFmpeg para usar o conversor.\nDownload: https://ffmpeg.org/download.html")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao verificar FFmpeg: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            self.update_status(f"❌ Erro ao verificar FFmpeg: {e}")
    
    def load_settings(self):
        """Carregar configurações salvas"""
        print("🔧 [DEBUG] Carregando configurações...")
        
        try:
            settings_file = Path("converter_settings.json")
            
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                
                print(f"🔧 [DEBUG] Configurações carregadas: {saved_settings}")
                
                for key, value in saved_settings.items():
                    if key in self.settings:
                        self.settings[key].set(value)
                        print(f"🔧 [DEBUG] {key} = {value}")
                
                if 'output_directory' in saved_settings:
                    self.output_directory.set(saved_settings['output_directory'])
                    print(f"🔧 [DEBUG] output_directory = {saved_settings['output_directory']}")
                
                self.update_status("⚙️ Configurações carregadas")
                print("✅ [DEBUG] Configurações carregadas com sucesso")
            else:
                print("🔧 [DEBUG] Arquivo de configurações não existe")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao carregar configurações: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def save_settings(self):
        """Salvar configurações"""
        print("🔧 [DEBUG] Salvando configurações...")
        
        try:
            settings_to_save = {
                key: var.get() for key, var in self.settings.items()
            }
            settings_to_save['output_directory'] = self.output_directory.get()
            
            print(f"🔧 [DEBUG] Configurações a salvar: {settings_to_save}")
            
            with open("converter_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, indent=2, ensure_ascii=False)
            
            print("✅ [DEBUG] Configurações salvas com sucesso")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao salvar configurações: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
    
    def on_closing(self):
        """Executar ao fechar a aplicação"""
        print("🔧 [DEBUG] Fechando aplicação...")
        
        try:
            if self.is_converting:
                if messagebox.askokcancel("Fechar", "Conversão em andamento. Deseja realmente fechar?"):
                    self.is_converting = False
                    self.save_settings()
                    self.root.destroy()
                    print("✅ [DEBUG] Aplicação fechada (conversão interrompida)")
            else:
                self.save_settings()
                self.root.destroy()
                print("✅ [DEBUG] Aplicação fechada normalmente")
                
        except Exception as e:
            print(f"❌ [DEBUG] Erro ao fechar aplicação: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")
            self.root.destroy()
    
    def run(self):
        """Executar a aplicação"""
        print("🚀 [DEBUG] Iniciando loop principal...")
        
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
            print("✅ [DEBUG] Loop principal finalizado")
            
        except Exception as e:
            print(f"❌ [DEBUG] Erro no loop principal: {e}")
            print(f"🔧 [DEBUG] Traceback: {traceback.format_exc()}")

def main():
    print("🌟 [DEBUG] === INICIANDO APLICAÇÃO ===")
    
    try:
        app = VideoConverterGUILite()
        app.run()
        print("🌟 [DEBUG] === APLICAÇÃO FINALIZADA ===")
        
    except Exception as e:
        print(f"💥 [DEBUG] ERRO FATAL: {e}")
        print(f"🔧 [DEBUG] Traceback completo: {traceback.format_exc()}")
        input("Pressione Enter para fechar...")

if __name__ == "__main__":
    main()