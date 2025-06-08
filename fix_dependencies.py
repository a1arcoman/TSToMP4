import subprocess
import sys
import os

def fix_numpy_opencv_compatibility():
    """Corrige incompatibilidade entre NumPy 2 e OpenCV"""
    print("🔧 Corrigindo incompatibilidade NumPy 2 + OpenCV...")
    
    try:
        # Desinstalar versões problemáticas
        print("📦 Removendo versões incompatíveis...")
        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', 'numpy', 'opencv-python', '-y'], 
                      capture_output=True)
        
        # Instalar versões compatíveis
        print("📥 Instalando versões compatíveis...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy<2.0.0'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python==4.8.1.78'])
        
        print("✅ Compatibilidade corrigida!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao corrigir dependências: {e}")
        return False

def install_all_dependencies():
    """Instala todas as dependências com versões corretas"""
    print("📦 Instalando todas as dependências...")
    
    try:
        # Instalar do requirements.txt atualizado
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Todas as dependências instaladas!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na instalação: {e}")
        return False

def test_imports():
    """Testa se todas as importações funcionam"""
    print("\n🧪 Testando importações...")
    
    modules = {
        'tkinter': 'tkinter',
        'tkinterdnd2': 'tkinterdnd2', 
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'ffmpeg': 'ffmpeg-python',
        'numpy': 'numpy'
    }
    
    all_ok = True
    
    for module, package in modules.items():
        try:
            __import__(module)
            print(f"✅ {package}: OK")
        except ImportError as e:
            print(f"❌ {package}: ERRO - {e}")
            all_ok = False
    
    return all_ok

def main():
    print("🛠️  CORREÇÃO DE DEPENDÊNCIAS - Conversor de Vídeo")
    print("=" * 55)
    
    # Método 1: Corrigir incompatibilidade específica
    print("\n🎯 Método 1: Correção específica NumPy + OpenCV")
    if fix_numpy_opencv_compatibility():
        if test_imports():
            print("\n🎉 PROBLEMA RESOLVIDO!")
            print("\n🚀 Agora você pode executar:")
            print("   python video_converter_gui.py")
            return
    
    # Método 2: Reinstalação completa
    print("\n🔄 Método 2: Reinstalação completa")
    if install_all_dependencies():
        if test_imports():
            print("\n🎉 PROBLEMA RESOLVIDO!")
            print("\n🚀 Agora você pode executar:")
            print("   python video_converter_gui.py")
            return
    
    # Se nada funcionou
    print("\n⚠️  SOLUÇÕES ALTERNATIVAS:")
    print("\n1️⃣  Instalação manual:")
    print("   pip uninstall numpy opencv-python -y")
    print("   pip install 'numpy<2.0.0'")
    print("   pip install opencv-python==4.8.1.78")
    
    print("\n2️⃣  Ambiente virtual limpo:")
    print("   python -m venv venv_conversor")
    print("   venv_conversor\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    
    print("\n3️⃣  Versão sem OpenCV (sem preview):")
    print("   Remova 'opencv-python' do requirements.txt")
    print("   A GUI funcionará sem preview de vídeo")

if __name__ == "__main__":
    main()
    input("\n⏸️  Pressione Enter para sair...")