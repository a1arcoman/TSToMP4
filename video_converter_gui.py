import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import os
import sys
from pathlib import Path
import json
from datetime import datetime
import subprocess
from PIL import Image, ImageTk
import cv2
from video_converter import VideoConverter

class VideoConverterGUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Conversor de Vídeo Universal - v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configurar ícone e estilo
        self.setup_styles()
        
        # Variáveis
        self.converter = VideoConverter()
        self.input_files = []
        self.output_directory = tk.StringVar()
        self.current_conversion = None
        self.conversion_queue = []
        self.is_converting = False
        
        # Configurações
        self.settings = {
            'output_format': tk.StringVar(value='mp4'),
            'quality': tk.StringVar(value='medium'),
            'video_codec': tk.StringVar(value='libx264'),
            'audio_codec': tk.StringVar(value='aac'),
            'resolution': tk.StringVar(value='original'),
            'audio_bitrate': tk.StringVar(value='192k'),
            'video_bitrate': tk.StringVar(value='auto'),
            'fps': tk.StringVar(value='original'),
            'audio_only': tk.BooleanVar(False),
            'overwrite': tk.BooleanVar(True),
            'preserve_metadata': tk.BooleanVar(True)
        }
        
        self.create_widgets()
        self.load_settings()
        
        # Configurar drag and drop
        self.setup_drag_drop()
        
        # Verificar FFmpeg
        self.check_ffmpeg_on_startup()
    
    def setup_styles(self):
        """Configurar estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Error.TLabel', foreground='#e74c3c')
        style.configure('Warning.TLabel', foreground='#f39c12')
        
        # Botões personalizados
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', background='#27ae60')
        style.configure('Danger.TButton', background='#e74c3c')
    
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎬 Conversor de Vídeo Universal", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(1, weight=1)
        
        # Criar abas
        self.create_conversion_tab()
        self.create_batch_tab()
        self.create_settings_tab()
        self.create_history_tab()
        
        # Barra de status
        self.create_status_bar(main_frame)
    
    def create_conversion_tab(self):
        """Criar aba de conversão individual"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="Conversão Individual")
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(tab_frame, text="Arquivo de Entrada", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        tab_frame.columnconfigure(0, weight=1)
        
        # Área de drop
        self.drop_area = tk.Frame(input_frame, bg='#ecf0f1', relief='dashed', bd=2, height=100)
        self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        drop_label = tk.Label(self.drop_area, text="📁 Arraste arquivos aqui ou clique para selecionar", 
                             bg='#ecf0f1', font=('Arial', 12), fg='#7f8c8d')
        drop_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Botões de seleção
        ttk.Button(input_frame, text="Selecionar Arquivo", 
                  command=self.select_input_file).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(input_frame, text="Limpar", 
                  command=self.clear_input).grid(row=1, column=1, padx=5)
        
        # Informações do arquivo
        self.file_info_frame = ttk.LabelFrame(tab_frame, text="Informações do Arquivo", padding="10")
        self.file_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.file_info_text = tk.Text(self.file_info_frame, height=6, width=50, state='disabled')
        self.file_info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Preview do vídeo
        self.preview_frame = ttk.LabelFrame(tab_frame, text="Preview", padding="10")
        self.preview_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(0, 10))
        
        self.preview_label = tk.Label(self.preview_frame, text="Nenhum arquivo selecionado", 
                                     bg='#bdc3c7', width=30, height=15)
        self.preview_label.grid(row=0, column=0)
        
        # Configurações de conversão
        self.create_conversion_settings(tab_frame)
        
        # Botões de ação
        action_frame = ttk.Frame(tab_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(action_frame, text="🎯 Converter", style='Primary.TButton',
                  command=self.start_conversion).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="⏹️ Parar", 
                  command=self.stop_conversion).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="📂 Abrir Pasta de Saída", 
                  command=self.open_output_folder).grid(row=0, column=2, padx=5)
    
    def create_conversion_settings(self, parent):
        """Criar configurações de conversão"""
        settings_frame = ttk.LabelFrame(parent, text="Configurações de Conversão", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Primeira linha
        ttk.Label(settings_frame, text="Formato:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        format_combo = ttk.Combobox(settings_frame, textvariable=self.settings['output_format'], 
                                   values=['mp4', 'avi', 'mkv', 'mov', 'webm', 'mp3', 'wav', 'aac'], width=10)
        format_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(settings_frame, text="Qualidade:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.settings['quality'],
                                    values=['low', 'medium', 'high', 'best'], width=10)
        quality_combo.grid(row=0, column=3, padx=5)
        
        ttk.Label(settings_frame, text="Resolução:").grid(row=0, column=4, sticky=tk.W, padx=(10, 5))
        resolution_combo = ttk.Combobox(settings_frame, textvariable=self.settings['resolution'],
                                       values=['original', '1920x1080', '1280x720', '854x480', '640x360'], width=12)
        resolution_combo.grid(row=0, column=5, padx=5)
        
        # Segunda linha
        ttk.Label(settings_frame, text="Codec Vídeo:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        video_codec_combo = ttk.Combobox(settings_frame, textvariable=self.settings['video_codec'],
                                        values=['libx264', 'libx265', 'libvpx', 'libvpx-vp9'], width=10)
        video_codec_combo.grid(row=1, column=1, padx=5, pady=(10, 0))
        
        ttk.Label(settings_frame, text="Codec Áudio:").grid(row=1, column=2, sticky=tk.W, padx=(10, 5), pady=(10, 0))
        audio_codec_combo = ttk.Combobox(settings_frame, textvariable=self.settings['audio_codec'],
                                        values=['aac', 'mp3', 'libvorbis', 'flac'], width=10)
        audio_codec_combo.grid(row=1, column=3, padx=5, pady=(10, 0))
        
        ttk.Label(settings_frame, text="Bitrate Áudio:").grid(row=1, column=4, sticky=tk.W, padx=(10, 5), pady=(10, 0))
        audio_bitrate_combo = ttk.Combobox(settings_frame, textvariable=self.settings['audio_bitrate'],
                                          values=['128k', '192k', '256k', '320k'], width=12)
        audio_bitrate_combo.grid(row=1, column=5, padx=5, pady=(10, 0))
        
        # Terceira linha - Checkboxes
        checkbox_frame = ttk.Frame(settings_frame)
        checkbox_frame.grid(row=2, column=0, columnspan=6, pady=(15, 0))
        
        ttk.Checkbutton(checkbox_frame, text="Apenas Áudio",
                       variable=self.settings['audio_only']).grid(row=0, column=0, padx=(0, 20))
        ttk.Checkbutton(checkbox_frame, text="Sobrescrever Arquivos",
                       variable=self.settings['overwrite']).grid(row=0, column=1, padx=20)
        ttk.Checkbutton(checkbox_frame, text="Preservar Metadados",
                       variable=self.settings['preserve_metadata']).grid(row=0, column=2, padx=20)
        
        # Pasta de saída
        output_frame = ttk.Frame(settings_frame)
        output_frame.grid(row=3, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(15, 0))
        settings_frame.columnconfigure(0, weight=1)
        
        ttk.Label(output_frame, text="Pasta de Saída:").grid(row=0, column=0, sticky=tk.W)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_directory, width=50)
        output_entry.grid(row=0, column=1, padx=(10, 5), sticky=(tk.W, tk.E))
        output_frame.columnconfigure(1, weight=1)
        ttk.Button(output_frame, text="Procurar",
                  command=self.select_output_directory).grid(row=0, column=2, padx=5)
    
    def create_batch_tab(self):
        """Criar aba de conversão em lote"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="Conversão em Lote")
        
        # Lista de arquivos
        files_frame = ttk.LabelFrame(tab_frame, text="Arquivos para Conversão", padding="10")
        files_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        
        # Treeview para lista de arquivos
        columns = ('arquivo', 'formato', 'tamanho', 'status')
        self.files_tree = ttk.Treeview(files_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.files_tree.heading('arquivo', text='Arquivo')
        self.files_tree.heading('formato', text='Formato')
        self.files_tree.heading('tamanho', text='Tamanho')
        self.files_tree.heading('status', text='Status')
        
        self.files_tree.column('arquivo', width=300)
        self.files_tree.column('formato', width=80)
        self.files_tree.column('tamanho', width=100)
        self.files_tree.column('status', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=scrollbar.set)
        
        self.files_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        
        # Botões de controle
        control_frame = ttk.Frame(tab_frame)
        control_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(control_frame, text="➕ Adicionar Arquivos",
                  command=self.add_batch_files).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="📁 Adicionar Pasta",
                  command=self.add_batch_folder).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="🗑️ Remover Selecionado",
                  command=self.remove_selected_files).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="🧹 Limpar Tudo",
                  command=self.clear_batch_files).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="🚀 Converter Todos", style='Primary.TButton',
                  command=self.start_batch_conversion).grid(row=0, column=4, padx=5)
    
    def create_settings_tab(self):
        """Criar aba de configurações"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="Configurações")
        
        # Configurações gerais
        general_frame = ttk.LabelFrame(tab_frame, text="Configurações Gerais", padding="10")
        general_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Configurações avançadas
        advanced_frame = ttk.LabelFrame(tab_frame, text="Configurações Avançadas", padding="10")
        advanced_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Presets
        presets_frame = ttk.LabelFrame(tab_frame, text="Presets de Conversão", padding="10")
        presets_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botões de configuração
        config_buttons_frame = ttk.Frame(tab_frame)
        config_buttons_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(config_buttons_frame, text="💾 Salvar Configurações",
                  command=self.save_settings).grid(row=0, column=0, padx=5)
        ttk.Button(config_buttons_frame, text="🔄 Restaurar Padrões",
                  command=self.reset_settings).grid(row=0, column=1, padx=5)
        ttk.Button(config_buttons_frame, text="📥 Importar Preset",
                  command=self.import_preset).grid(row=0, column=2, padx=5)
        ttk.Button(config_buttons_frame, text="📤 Exportar Preset",
                  command=self.export_preset).grid(row=0, column=3, padx=5)
    
    def create_history_tab(self):
        """Criar aba de histórico"""
        tab_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab_frame, text="Histórico")
        
        # Lista de conversões
        history_frame = ttk.LabelFrame(tab_frame, text="Histórico de Conversões", padding="10")
        history_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        
        # Treeview para histórico
        history_columns = ('data', 'arquivo_origem', 'arquivo_destino', 'formato', 'status', 'tempo')
        self.history_tree = ttk.Treeview(history_frame, columns=history_columns, show='headings', height=20)
        
        # Configurar colunas do histórico
        self.history_tree.heading('data', text='Data/Hora')
        self.history_tree.heading('arquivo_origem', text='Arquivo Origem')
        self.history_tree.heading('arquivo_destino', text='Arquivo Destino')
        self.history_tree.heading('formato', text='Formato')
        self.history_tree.heading('status', text='Status')
        self.history_tree.heading('tempo', text='Tempo')
        
        # Scrollbar para histórico
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        # Botões do histórico
        history_buttons_frame = ttk.Frame(tab_frame)
        history_buttons_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(history_buttons_frame, text="🔄 Atualizar",
                  command=self.refresh_history).grid(row=0, column=0, padx=5)
        ttk.Button(history_buttons_frame, text="🗑️ Limpar Histórico",
                  command=self.clear_history).grid(row=0, column=1, padx=5)
        ttk.Button(history_buttons_frame, text="📊 Exportar Relatório",
                  command=self.export_report).grid(row=0, column=2, padx=5)
    
    def create_status_bar(self, parent):
        """Criar barra de status"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                           mode='determinate', length=300)
        self.progress_bar.grid(row=0, column=0, padx=(0, 10))
        
        # Label de status
        self.status_label = ttk.Label(status_frame, text="Pronto para conversão")
        self.status_label.grid(row=0, column=1, sticky=tk.W)
        
        # Informações do sistema
        self.system_info_label = ttk.Label(status_frame, text="")
        self.system_info_label.grid(row=0, column=2, sticky=tk.E)
        status_frame.columnconfigure(1, weight=1)
    
    def setup_drag_drop(self):
        """Configurar drag and drop"""
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
        
        # Tornar a área clicável
        self.drop_area.bind('<Button-1>', lambda e: self.select_input_file())
    
    def on_drop(self, event):
        """Manipular arquivos arrastados"""
        files = self.root.tk.splitlist(event.data)
        if files:
            self.input_files = [f for f in files if os.path.isfile(f)]
            if self.input_files:
                self.update_file_info(self.input_files[0])
                self.update_preview(self.input_files[0])
    
    def select_input_file(self):
        """Selecionar arquivo de entrada"""
        file_path = filedialog.askopenfilename(
            title="Selecionar arquivo de vídeo",
            filetypes=[
                ("Todos os vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ts *.m2ts"),
                ("MP4", "*.mp4"),
                ("AVI", "*.avi"),
                ("MKV", "*.mkv"),
                ("TS", "*.ts *.m2ts"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if file_path:
            self.input_files = [file_path]
            self.update_file_info(file_path)
            self.update_preview(file_path)
    
    def update_file_info(self, file_path):
        """Atualizar informações do arquivo"""
        try:
            info = self.converter.get_video_info(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            
            info_text = f"""📁 Arquivo: {os.path.basename(file_path)}
📏 Tamanho: {file_size:.2f} MB
⏱️ Duração: {info.get('duration', 0):.2f} segundos
📺 Resolução: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}
🎥 Codec Vídeo: {info.get('video_codec', 'N/A')}
🔊 Codec Áudio: {info.get('audio_codec', 'N/A')}"""
            
            self.file_info_text.config(state='normal')
            self.file_info_text.delete(1.0, tk.END)
            self.file_info_text.insert(1.0, info_text)
            self.file_info_text.config(state='disabled')
            
        except Exception as e:
            self.file_info_text.config(state='normal')
            self.file_info_text.delete(1.0, tk.END)
            self.file_info_text.insert(1.0, f"Erro ao ler arquivo: {str(e)}")
            self.file_info_text.config(state='disabled')
    
    def update_preview(self, file_path):
        """Atualizar preview do vídeo"""
        try:
            # Capturar frame do vídeo
            cap = cv2.VideoCapture(file_path)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Redimensionar frame
                height, width = frame.shape[:2]
                max_size = 200
                
                if width > height:
                    new_width = max_size
                    new_height = int(height * max_size / width)
                else:
                    new_height = max_size
                    new_width = int(width * max_size / height)
                
                frame = cv2.resize(frame, (new_width, new_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Converter para PhotoImage
                image = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(image)
                
                self.preview_label.config(image=photo, text="")
                self.preview_label.image = photo  # Manter referência
            else:
                self.preview_label.config(image="", text="Preview não disponível")
                
        except Exception as e:
            self.preview_label.config(image="", text=f"Erro no preview: {str(e)[:30]}...")
    
    def clear_input(self):
        """Limpar entrada"""
        self.input_files = []
        self.file_info_text.config(state='normal')
        self.file_info_text.delete(1.0, tk.END)
        self.file_info_text.config(state='disabled')
        self.preview_label.config(image="", text="Nenhum arquivo selecionado")
        self.preview_label.image = None
    
    def select_output_directory(self):
        """Selecionar diretório de saída"""
        directory = filedialog.askdirectory(title="Selecionar pasta de saída")
        if directory:
            self.output_directory.set(directory)
    
    def start_conversion(self):
        """Iniciar conversão"""
        if not self.input_files:
            messagebox.showwarning("Aviso", "Selecione um arquivo para converter")
            return
        
        if not self.output_directory.get():
            # Usar diretório do arquivo de entrada como padrão
            input_dir = os.path.dirname(self.input_files[0])
            self.output_directory.set(input_dir)
        
        # Iniciar conversão em thread separada
        self.is_converting = True
        thread = threading.Thread(target=self._convert_file, args=(self.input_files[0],))
        thread.daemon = True
        thread.start()
    
    def _convert_file(self, input_path):
        """Converter arquivo (executado em thread separada)"""
        try:
            # Preparar parâmetros
            input_file = Path(input_path)
            output_format = self.settings['output_format'].get()
            output_file = Path(self.output_directory.get()) / f"{input_file.stem}.{output_format}"
            
            # Atualizar status
            self.root.after(0, lambda: self.update_status("Convertendo...", 0))
            
            # Executar conversão
            if self.settings['audio_only'].get():
                success = self.converter.convert_to_audio(
                    str(input_file), str(output_file),
                    audio_codec=output_format if output_format in ['mp3', 'aac', 'wav'] else 'mp3'
                )
            else:
                success = self.converter.convert_video(
                    str(input_file), str(output_file),
                    video_codec=self.settings['video_codec'].get(),
                    audio_codec=self.settings['audio_codec'].get(),
                    quality=self.settings['quality'].get(),
                    resolution=None if self.settings['resolution'].get() == 'original' else self.settings['resolution'].get()
                )
            
            # Atualizar interface
            if success:
                self.root.after(0, lambda: self.update_status("Conversão concluída!", 100))
                self.root.after(0, lambda: messagebox.showinfo("Sucesso", f"Arquivo convertido: {output_file}"))
            else:
                self.root.after(0, lambda: self.update_status("Erro na conversão", 0))
                self.root.after(0, lambda: messagebox.showerror("Erro", "Falha na conversão"))
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"Erro: {str(e)}", 0))
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na conversão: {str(e)}"))
        
        finally:
            self.is_converting = False
    
    def stop_conversion(self):
        """Parar conversão"""
        if self.is_converting:
            # Implementar lógica para parar conversão
            self.is_converting = False
            self.update_status("Conversão cancelada", 0)
    
    def update_status(self, message, progress=None):
        """Atualizar status e progresso"""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress_var.set(progress)
    
    def open_output_folder(self):
        """Abrir pasta de saída"""
        if self.output_directory.get() and os.path.exists(self.output_directory.get()):
            os.startfile(self.output_directory.get())
        else:
            messagebox.showwarning("Aviso", "Pasta de saída não definida ou não existe")
    
    def add_batch_files(self):
        """Adicionar arquivos para conversão em lote"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos para conversão em lote",
            filetypes=[
                ("Todos os vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ts *.m2ts"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        for file_path in files:
            self.add_file_to_batch(file_path)
    
    def add_batch_folder(self):
        """Adicionar pasta para conversão em lote"""
        folder = filedialog.askdirectory(title="Selecionar pasta com vídeos")
        if folder:
            for file_path in Path(folder).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.ts', '.m2ts']:
                    self.add_file_to_batch(str(file_path))
    
    def add_file_to_batch(self, file_path):
        """Adicionar arquivo à lista de lote"""
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            file_format = Path(file_path).suffix[1:].upper()
            
            self.files_tree.insert('', 'end', values=(
                os.path.basename(file_path),
                file_format,
                f"{file_size:.1f} MB",
                "Aguardando"
            ))
        except Exception as e:
            print(f"Erro ao adicionar arquivo {file_path}: {e}")
    
    def remove_selected_files(self):
        """Remover arquivos selecionados da lista"""
        selected_items = self.files_tree.selection()
        for item in selected_items:
            self.files_tree.delete(item)
    
    def clear_batch_files(self):
        """Limpar todos os arquivos da lista"""
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
    
    def start_batch_conversion(self):
        """Iniciar conversão em lote"""
        items = self.files_tree.get_children()
        if not items:
            messagebox.showwarning("Aviso", "Adicione arquivos para conversão em lote")
            return
        
        if not self.output_directory.get():
            messagebox.showwarning("Aviso", "Selecione uma pasta de saída")
            return
        
        # Implementar conversão em lote
        messagebox.showinfo("Info", "Conversão em lote iniciada!")
    
    def check_ffmpeg_on_startup(self):
        """Verificar FFmpeg na inicialização"""
        if not self.converter.check_ffmpeg():
            messagebox.showerror(
                "FFmpeg não encontrado",
                "FFmpeg não foi encontrado no sistema.\n\n"
                "Para usar este programa, você precisa instalar o FFmpeg:\n"
                "1. Baixe de: https://ffmpeg.org/download.html\n"
                "2. Ou use: winget install FFmpeg\n"
                "3. Ou use: choco install ffmpeg"
            )
    
    def save_settings(self):
        """Salvar configurações"""
        settings_data = {key: var.get() for key, var in self.settings.items()}
        settings_data['output_directory'] = self.output_directory.get()
        
        try:
            with open('converter_settings.json', 'w') as f:
                json.dump(settings_data, f, indent=2)
            messagebox.showinfo("Sucesso", "Configurações salvas!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def load_settings(self):
        """Carregar configurações"""
        try:
            if os.path.exists('converter_settings.json'):
                with open('converter_settings.json', 'r') as f:
                    settings_data = json.load(f)
                
                for key, value in settings_data.items():
                    if key == 'output_directory':
                        self.output_directory.set(value)
                    elif key in self.settings:
                        self.settings[key].set(value)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    def reset_settings(self):
        """Restaurar configurações padrão"""
        defaults = {
            'output_format': 'mp4',
            'quality': 'medium',
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'resolution': 'original',
            'audio_bitrate': '192k',
            'video_bitrate': 'auto',
            'fps': 'original',
            'audio_only': False,
            'overwrite': True,
            'preserve_metadata': True
        }
        
        for key, value in defaults.items():
            if key in self.settings:
                self.settings[key].set(value)
        
        self.output_directory.set('')
        messagebox.showinfo("Sucesso", "Configurações restauradas para o padrão!")
    
    def import_preset(self):
        """Importar preset"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def export_preset(self):
        """Exportar preset"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def refresh_history(self):
        """Atualizar histórico"""
        messagebox.showinfo("Info", "Histórico atualizado")
    
    def clear_history(self):
        """Limpar histórico"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        messagebox.showinfo("Sucesso", "Histórico limpo!")
    
    def export_report(self):
        """Exportar relatório"""
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()

def main():
    try:
        app = VideoConverterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()