import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias para a GUI"""
    print("🔧 Instalando dependências da GUI...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, text=True)
        print("✅ FFmpeg encontrado!")
        version_line = result.stdout.split('\n')[0]
        print(f"   {version_line}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg não encontrado!")
        print("\n📥 Para instalar o FFmpeg no Windows:")
        print("   1. Opção 1 - Winget: winget install FFmpeg")
        print("   2. Opção 2 - Chocolatey: choco install ffmpeg")
        print("   3. Opção 3 - Manual: https://ffmpeg.org/download.html")
        print("\n⚠️  Reinicie o terminal após a instalação!")
        return False

def test_gui_dependencies():
    """Testa se as dependências da GUI estão funcionando"""
    print("\n🧪 Testando dependências da GUI...")
    
    try:
        import tkinter
        print("✅ tkinter: OK")
    except ImportError:
        print("❌ tkinter: ERRO - Instale Python com tkinter")
        return False
    
    try:
        import tkinterdnd2
        print("✅ tkinterdnd2: OK")
    except ImportError:
        print("❌ tkinterdnd2: ERRO")
        return False
    
    try:
        import PIL
        print("✅ Pillow: OK")
    except ImportError:
        print("❌ Pillow: ERRO")
        return False
    
    try:
        import cv2
        print("✅ OpenCV: OK")
    except ImportError:
        print("❌ OpenCV: ERRO")
        return False
    
    try:
        import ffmpeg
        print("✅ ffmpeg-python: OK")
    except ImportError:
        print("❌ ffmpeg-python: ERRO")
        return False
    
    return True

def create_desktop_shortcut():
    """Cria atalho na área de trabalho (Windows)"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Conversor de Video.lnk")
        target = os.path.join(os.getcwd(), "video_converter_gui.py")
        wDir = os.getcwd()
        icon = target
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Atalho criado na área de trabalho!")
    except ImportError:
        print("⚠️  Para criar atalho, instale: pip install winshell pywin32")
    except Exception as e:
        print(f"⚠️  Não foi possível criar atalho: {e}")

if __name__ == "__main__":
    print("🎬 Configurando Conversor de Vídeo com GUI")
    print("=" * 50)
    
    # Instalar dependências
    if install_requirements():
        print("\n" + "=" * 50)
        
        # Testar dependências
        if test_gui_dependencies():
            print("\n" + "=" * 50)
            
            # Verificar FFmpeg
            ffmpeg_ok = check_ffmpeg()
            
            print("\n" + "=" * 50)
            print("📋 RESUMO DA INSTALAÇÃO:")
            print(f"   🐍 Dependências Python: ✅")
            print(f"   🎥 FFmpeg: {'✅' if ffmpeg_ok else '❌'}")
            
            if ffmpeg_ok:
                print("\n🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
                print("\n🚀 Para iniciar a GUI, execute:")
                print("   python video_converter_gui.py")
                
                # Criar atalho
                create_desktop_shortcut()
                
                # Perguntar se quer iniciar agora
                response = input("\n❓ Deseja iniciar a GUI agora? (s/n): ")
                if response.lower() in ['s', 'sim', 'y', 'yes']:
                    print("\n🎬 Iniciando GUI...")
                    try:
                        subprocess.run([sys.executable, 'video_converter_gui.py'])
                    except Exception as e:
                        print(f"❌ Erro ao iniciar GUI: {e}")
            else:
                print("\n⚠️  INSTALAÇÃO PARCIAL - FFmpeg necessário")
                print("   Instale o FFmpeg e execute novamente.")
        else:
            print("\n❌ ERRO NAS DEPENDÊNCIAS")
            print("   Verifique os erros acima e tente novamente.")
    else:
        print("\n❌ FALHA NA INSTALAÇÃO")
        print("   Verifique sua conexão e permissões.")
    
    input("\n⏸️  Pressione Enter para sair...")