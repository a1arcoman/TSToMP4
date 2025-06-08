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
except ImportError:
    OPENCV_AVAILABLE = False

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from video_converter import VideoConverter

class VideoConverterGUI:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        
        if self.debug_mode:
            print("🚀 [DEBUG] Iniciando VideoConverterGUI...")
        
        # Inicializar tkinter padrão primeiro
        self.root = tk.Tk()
        self.dnd_enabled = False
        
        # Tentar atualizar para TkinterDnD se disponível
        if DND_AVAILABLE:
            try:
                self.root.destroy()
                self.root = TkinterDnD.Tk()
                self.dnd_enabled = True
                if self.debug_mode:
                    print("✅ [DEBUG] TkinterDnD inicializado com sucesso")
            except Exception as e:
                if self.debug_mode:
                    print(f"❌ [DEBUG] Erro ao inicializar TkinterDnD: {e}")
                self.root = tk.Tk()
                self.dnd_enabled = False
        
        self.root.title("Conversor de Vídeo Universal v4.0")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Configurar estilo
        self.setup_styles()
        
        # Variáveis
        self.converter = VideoConverter()
        self.input_files = []
        self.is_converting = False
        
        # Variáveis tkinter com master explícito
        self.output_directory = tk.StringVar(master=self.root)
        self.progress_var = tk.DoubleVar(master=self.root)
        self.status_var = tk.StringVar(master=self.root, value="Pronto para conversão")
        
        # Configurações
        self.settings = {
            'output_format': tk.StringVar(master=self.root, value='mp4'),
            'quality': tk.StringVar(master=self.root, value='medium'),
            'audio_only': tk.BooleanVar(master=self.root, value=False),
            'overwrite': tk.BooleanVar(master=self.root, value=True)
        }
        
        # Criar interface
        self.create_widgets()
        self.load_settings()
        
        # Configurar drag-drop se habilitado
        if self.dnd_enabled and hasattr(self, 'drop_area'):
            self.setup_drag_drop()
        
        # Verificar FFmpeg
        self.check_ffmpeg_on_startup()
        
        if self.debug_mode:
            print("✅ [DEBUG] Inicialização concluída com sucesso!")
    
    def debug_print(self, message):
        """Imprimir mensagem apenas se debug estiver habilitado"""
        if self.debug_mode:
            print(message)
    
    def setup_styles(self):
        """Configurar estilos básicos"""
        try:
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('Title.TLabel', font=('Arial', 12, 'bold'))
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro ao configurar estilos: {e}")
    
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Seções
        self.create_input_section(main_frame)
        self.create_settings_section(main_frame)
        self.create_output_section(main_frame)
        self.create_conversion_section(main_frame)
        self.create_status_section(main_frame)
    
    def create_input_section(self, parent):
        """Criar seção de entrada de arquivos"""
        # Frame de entrada
        input_frame = ttk.LabelFrame(parent, text="📁 Arquivos de Entrada", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Área de drop
        try:
            if self.dnd_enabled:
                self.drop_area = tk.Frame(input_frame, bg='#ecf0f1', relief='ridge', bd=2, height=80)
                self.drop_area.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
                self.drop_area.grid_propagate(False)
                
                drop_label = tk.Label(self.drop_area, text="🎬 Arraste arquivos de vídeo aqui ou clique para selecionar",
                                    bg='#ecf0f1', font=('Arial', 10))
                drop_label.place(relx=0.5, rely=0.5, anchor='center')
                drop_label.bind('<Button-1>', lambda e: self.select_input_file())
                self.drop_area.bind('<Button-1>', lambda e: self.select_input_file())
            else:
                # Botão simples se DnD não estiver disponível
                select_btn = ttk.Button(input_frame, text="📁 Selecionar Arquivos de Vídeo", 
                                      command=self.select_input_file)
                select_btn.grid(row=0, column=0, pady=(0, 10))
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro ao criar área de drop: {e}")
            # Fallback para botão simples
            select_btn = ttk.Button(input_frame, text="📁 Selecionar Arquivos de Vídeo", 
                                  command=self.select_input_file)
            select_btn.grid(row=0, column=0, pady=(0, 10))
        
        # Lista de arquivos
        self.file_listbox = tk.Listbox(input_frame, height=6)
        self.file_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Botões de controle
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="➕ Adicionar", command=self.select_input_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="➖ Remover", command=self.remove_selected_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Limpar Tudo", command=self.clear_file_list).pack(side=tk.LEFT)
    
    def create_settings_section(self, parent):
        """Criar seção de configurações"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=(0, 5))
        
        # Formato de saída
        ttk.Label(settings_frame, text="Formato:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        format_combo = ttk.Combobox(settings_frame, textvariable=self.settings['output_format'], 
                                   values=['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'], state="readonly")
        format_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        # Qualidade
        ttk.Label(settings_frame, text="Qualidade:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.settings['quality'],
                                   values=['low', 'medium', 'high', 'ultra'], state="readonly")
        quality_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 0))
        
        # Opções
        ttk.Checkbutton(settings_frame, text="Apenas áudio", 
                       variable=self.settings['audio_only']).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        ttk.Checkbutton(settings_frame, text="Sobrescrever arquivos", 
                       variable=self.settings['overwrite']).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        settings_frame.columnconfigure(1, weight=1)
    
    def create_output_section(self, parent):
        """Criar seção de saída"""
        output_frame = ttk.LabelFrame(parent, text="📂 Pasta de Saída", padding="10")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        
        # Entrada de diretório
        dir_frame = ttk.Frame(output_frame)
        dir_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(dir_frame, textvariable=self.output_directory)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(dir_frame, text="📁", command=self.select_output_directory, width=3).grid(row=0, column=1)
        
        # Informações
        info_text = "💡 Dica: Se não especificar uma pasta, os arquivos serão salvos na mesma pasta dos originais."
        ttk.Label(output_frame, text=info_text, font=('Arial', 8), foreground='gray').grid(row=1, column=0, sticky=tk.W)
    
    def create_conversion_section(self, parent):
        """Criar seção de conversão"""
        conversion_frame = ttk.LabelFrame(parent, text="🔄 Conversão", padding="10")
        conversion_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        conversion_frame.columnconfigure(0, weight=1)
        
        # Botões
        btn_frame = ttk.Frame(conversion_frame)
        btn_frame.grid(row=0, column=0, pady=(0, 10))
        
        self.convert_btn = ttk.Button(btn_frame, text="🚀 Iniciar Conversão", command=self.start_conversion)
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹️ Parar", command=self.stop_conversion, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(btn_frame, text="💾 Salvar Configurações", command=self.save_settings).pack(side=tk.LEFT)
    
    def create_status_section(self, parent):
        """Criar seção de status"""
        status_frame = ttk.LabelFrame(parent, text="📊 Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_frame.columnconfigure(0, weight=1)
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.grid(row=1, column=0, sticky=tk.W)
    
    def setup_drag_drop(self):
        """Configurar funcionalidade de drag and drop"""
        try:
            self.drop_area.drop_target_register(DND_FILES)
            self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
            self.debug_print("✅ [DEBUG] Drag-drop configurado com sucesso")
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro ao configurar drag-drop: {e}")
    
    def on_drop(self, event):
        """Manipular arquivos arrastados"""
        try:
            files = self.root.tk.splitlist(event.data)
            for file_path in files:
                if os.path.isfile(file_path) and self.is_video_file(file_path):
                    if file_path not in self.input_files:
                        self.input_files.append(file_path)
                        self.file_listbox.insert(tk.END, os.path.basename(file_path))
            self.update_status(f"Adicionados {len(files)} arquivo(s)")
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro no drop: {e}")
            messagebox.showerror("Erro", f"Erro ao processar arquivos: {e}")
    
    def is_video_file(self, file_path):
        """Verificar se o arquivo é um vídeo"""
        video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.ts', '.m4v', '.3gp'}
        return Path(file_path).suffix.lower() in video_extensions
    
    def select_input_file(self):
        """Selecionar arquivos de entrada"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos de vídeo",
            filetypes=[
                ("Arquivos de vídeo", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.ts *.m4v *.3gp"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        for file_path in files:
            if file_path not in self.input_files:
                self.input_files.append(file_path)
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
        
        if files:
            self.update_status(f"Adicionados {len(files)} arquivo(s)")
    
    def remove_selected_file(self):
        """Remover arquivo selecionado"""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            del self.input_files[index]
            self.update_status("Arquivo removido")
    
    def clear_file_list(self):
        """Limpar lista de arquivos"""
        self.file_listbox.delete(0, tk.END)
        self.input_files.clear()
        self.update_status("Lista de arquivos limpa")
    
    def select_output_directory(self):
        """Selecionar diretório de saída"""
        directory = filedialog.askdirectory(title="Selecionar pasta de saída")
        if directory:
            self.output_directory.set(directory)
    
    def start_conversion(self):
        """Iniciar processo de conversão"""
        if not self.input_files:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo de vídeo.")
            return
        
        if self.is_converting:
            messagebox.showwarning("Aviso", "Uma conversão já está em andamento.")
            return
        
        self.is_converting = True
        self.convert_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        # Iniciar conversão em thread separada
        conversion_thread = threading.Thread(target=self.convert_files, daemon=True)
        conversion_thread.start()
    
    def convert_files(self):
        """Converter arquivos (executado em thread separada)"""
        try:
            total_files = len(self.input_files)
            
            for i, input_file in enumerate(self.input_files):
                if not self.is_converting:  # Verificar se foi cancelado
                    break
                
                # Atualizar status
                filename = os.path.basename(input_file)
                self.update_status(f"Convertendo {filename} ({i+1}/{total_files})...")
                
                # Determinar arquivo de saída
                output_dir = self.output_directory.get() or os.path.dirname(input_file)
                output_format = self.settings['output_format'].get()
                base_name = Path(input_file).stem
                output_file = os.path.join(output_dir, f"{base_name}.{output_format}")
                
                # Verificar sobrescrita
                if os.path.exists(output_file) and not self.settings['overwrite'].get():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.{output_format}")
                
                try:
                    # Converter arquivo
                    if self.settings['audio_only'].get():
                        self.converter.convert_to_audio(input_file, output_file)
                    else:
                        self.converter.convert_video(
                            input_file, 
                            output_file,
                            quality=self.settings['quality'].get()
                        )
                    
                    self.debug_print(f"✅ [DEBUG] Conversão concluída: {output_file}")
                    
                except Exception as e:
                    self.debug_print(f"❌ [DEBUG] Erro ao converter {input_file}: {e}")
                    messagebox.showerror("Erro de Conversão", f"Erro ao converter {filename}:\n{str(e)}")
                
                # Atualizar progresso
                progress = ((i + 1) / total_files) * 100
                self.progress_var.set(progress)
            
            if self.is_converting:
                self.update_status("✅ Conversão concluída com sucesso!")
                messagebox.showinfo("Sucesso", "Conversão concluída com sucesso!")
            else:
                self.update_status("⏹️ Conversão cancelada")
                
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro geral na conversão: {e}")
            messagebox.showerror("Erro", f"Erro durante a conversão:\n{str(e)}")
        finally:
            self.is_converting = False
            self.convert_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.progress_var.set(0)
    
    def stop_conversion(self):
        """Parar conversão"""
        self.is_converting = False
        self.update_status("Parando conversão...")
    
    def update_status(self, message):
        """Atualizar status na interface"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def check_ffmpeg_on_startup(self):
        """Verificar FFmpeg na inicialização"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.debug_print("✅ [DEBUG] FFmpeg encontrado")
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showwarning(
                "FFmpeg não encontrado",
                "FFmpeg não foi encontrado no sistema.\n\n"
                "Para instalar:\n"
                "• Windows: winget install FFmpeg\n"
                "• Ou baixe em: https://ffmpeg.org/download.html\n\n"
                "Reinicie o terminal após a instalação."
            )
    
    def save_settings(self):
        """Salvar configurações"""
        try:
            settings_data = {
                'output_format': self.settings['output_format'].get(),
                'quality': self.settings['quality'].get(),
                'audio_only': self.settings['audio_only'].get(),
                'overwrite': self.settings['overwrite'].get(),
                'output_directory': self.output_directory.get()
            }
            
            with open('converter_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.debug_print("✅ [DEBUG] Configurações salvas")
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
    
    def load_settings(self):
        """Carregar configurações"""
        try:
            if os.path.exists('converter_settings.json'):
                with open('converter_settings.json', 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                
                self.settings['output_format'].set(settings_data.get('output_format', 'mp4'))
                self.settings['quality'].set(settings_data.get('quality', 'medium'))
                self.settings['audio_only'].set(settings_data.get('audio_only', False))
                self.settings['overwrite'].set(settings_data.get('overwrite', True))
                self.output_directory.set(settings_data.get('output_directory', ''))
                
                self.debug_print("✅ [DEBUG] Configurações carregadas")
        except Exception as e:
            self.debug_print(f"❌ [DEBUG] Erro ao carregar configurações: {e}")
    
    def run(self):
        """Executar a aplicação"""
        self.root.mainloop()

def main():
    # Verificar se deve executar em modo debug
    debug_mode = '--debug' in sys.argv or '-d' in sys.argv
    
    app = VideoConverterGUI(debug_mode=debug_mode)
    app.run()

if __name__ == "__main__":
    main()