# 🎬 Video Converter Universal
Um conversor de vídeo completo e fácil de usar com interface gráfica moderna, suportando múltiplos formatos e funcionalidades avançadas.

## 📋 Índice
- Características
- Formatos Suportados
- Pré-requisitos
- Instalação
- Uso
- Interface Gráfica
- Linha de Comando
- Executável
- Configurações
- Solução de Problemas
- Contribuição
## ✨ Características
### 🎯 Funcionalidades Principais
- Interface Gráfica Moderna : Interface intuitiva com drag-and-drop
- Conversão em Lote : Processe múltiplos arquivos simultaneamente
- Múltiplos Formatos : Suporte para os principais formatos de vídeo e áudio
- Qualidade Configurável : Opções de qualidade low, medium, high e ultra
- Conversão de Áudio : Extraia áudio de vídeos ou converta formatos de áudio
- Otimização TS : Conversão otimizada especial para arquivos .ts
- Configurações Persistentes : Salve suas preferências automaticamente
- Modo Debug : Logs detalhados para diagnóstico
### 🚀 Tecnologias
- Python 3.8+ : Linguagem principal
- FFmpeg : Engine de conversão de alta performance
- Tkinter : Interface gráfica nativa
- TkinterDnD2 : Funcionalidade drag-and-drop
- OpenCV : Processamento de vídeo (opcional)
- Pillow : Manipulação de imagens (opcional)
## 📁 Formatos Suportados
### 🎥 Formatos de Vídeo
Entrada Saída MP4, AVI, MKV MP4, AVI, MKV MOV, WMV, FLV MOV, WMV, FLV WEBM, TS, M2TS WEBM M4V, 3GP -

### 🎵 Formatos de Áudio
Entrada Saída MP3, WAV, AAC MP3, WAV, AAC FLAC, OGG, M4A FLAC, OGG, M4A

## 🔧 Pré-requisitos
### Sistema Operacional
- Windows 10/11 (testado)
- Python 3.8 ou superior
### Dependências Obrigatórias
- FFmpeg : Engine de conversão
- Python : Ambiente de execução
### Dependências Opcionais
- tkinterdnd2 : Para drag-and-drop
- Pillow : Para manipulação de imagens
- OpenCV : Para processamento avançado de vídeo
## 📦 Instalação
### Método 1: Instalação Automática (Recomendado)
1. Clone ou baixe o projeto :
   
   ```
   git clone https://github.com/seu-usuario/video-converter.git
   cd video-converter
   ```
2. Execute o instalador de dependências :
   
   ```
   python install_gui_dependencies.py
   ```
3. Instale o FFmpeg :
   
   ```
   # Opção 1 - Winget (Windows 10/11)
   winget install FFmpeg
   
   # Opção 2 - Chocolatey
   choco install ffmpeg
   
   # Opção 3 - Manual
   # Baixe em: https://ffmpeg.org/download.html
   ```
4. Reinicie o terminal após instalar o FFmpeg
### Método 2: Instalação Manual
1. Instale as dependências Python :
   
   ```
   pip install -r requirements.txt
   ```
2. Instale o FFmpeg (veja opções acima)
### Método 3: Executável Pré-compilado
1. Baixe o executável da seção Releases
2. Execute diretamente - não precisa instalar Python ou dependências
3. Instale apenas o FFmpeg (obrigatório)
## 🎮 Uso
### Interface Gráfica Execução Normal
```
python video_converter_gui_final.py
``` Modo Debug
```
python video_converter_gui_final.py --debug
``` Usando Executável
```
# Modo normal
VideoConverter.exe

# Modo debug
VideoConverter.exe --debug
```
### Linha de Comando Conversão Básica
```
python video_converter.py input.ts output.mp4
``` Conversão com Qualidade
```
python video_converter.py input.ts output.mp4 --quality high
``` Conversão para Áudio
```
python video_converter.py input.mp4 output.mp3 --audio-only
``` Conversão em Lote
```
python video_converter.py --batch pasta_entrada pasta_saida 
--quality medium
``` Conversão TS Otimizada
```
python video_converter.py input.ts output.mp4 --ts-optimized
```
## 🖥️ Interface Gráfica
### Seções da Interface 📁 Arquivos de Entrada
- Drag & Drop : Arraste arquivos diretamente para a área
- Seleção Manual : Clique para abrir o seletor de arquivos
- Lista de Arquivos : Visualize todos os arquivos adicionados
- Controles : Adicionar, remover ou limpar arquivos ⚙️ Configurações
- Formato de Saída : MP4, AVI, MKV, MOV, WMV, FLV, WEBM
- Qualidade : Low, Medium, High, Ultra
- Apenas Áudio : Extrair somente o áudio
- Sobrescrever : Substituir arquivos existentes 📂 Pasta de Saída
- Seleção de Pasta : Escolha onde salvar os arquivos convertidos
- Pasta Automática : Se não especificada, usa a pasta dos arquivos originais 🔄 Conversão
- Iniciar : Começar o processo de conversão
- Parar : Cancelar conversão em andamento
- Salvar Configurações : Manter suas preferências 📊 Status
- Barra de Progresso : Acompanhe o progresso da conversão
- Status Atual : Informações em tempo real do processo
## 💻 Linha de Comando
### Parâmetros Disponíveis
```
python video_converter.py [opções] input output
``` Opções Principais
Parâmetro Descrição Exemplo --quality Qualidade (low/medium/high/ultra) --quality high --audio-only Converter apenas áudio --audio-only --batch Conversão em lote --batch pasta_in pasta_out --ts-optimized Otimização para arquivos TS --ts-optimized --resolution Resolução de saída --resolution 1920x1080 --video-codec Codec de vídeo --video-codec libx265 --audio-codec Codec de áudio --audio-codec aac

### Exemplos Práticos Converter TS para MP4 (Otimizado)
```
python video_converter.py video.ts video.mp4 --ts-optimized 
--quality high
``` Extrair Áudio de Vídeo
```
python video_converter.py video.mp4 audio.mp3 --audio-only
``` Conversão com Resolução Específica
```
python video_converter.py input.avi output.mp4 --resolution 
1280x720 --quality medium
``` Lote com Codec Específico
```
python video_converter.py --batch ./videos ./convertidos 
--video-codec libx265 --quality ultra
```
## 📦 Executável
### Gerar Executável
1. Execute o script de build :
   
   ```
   python build_exe.py
   ```
2. Encontre o executável :
   
   ```
   dist/VideoConverter.exe
   ```
### Características do Executável
- Arquivo Único : Não precisa instalar Python
- Interface Gráfica : Sem janela de console
- Dependências Incluídas : Todas as bibliotecas Python embutidas
- Modo Debug : Suporte a --debug para diagnóstico
- Tamanho : ~50-80MB (dependendo das dependências)
### Distribuição
- ✅ Portável : Funciona em qualquer Windows 10/11
- ✅ Sem Instalação : Execute diretamente
- ⚠️ FFmpeg Necessário : Deve estar instalado no sistema de destino
## ⚙️ Configurações
### Arquivo de Configuração
As configurações são salvas automaticamente em converter_settings.json :

```
{
  "output_format": "mp4",
  "quality": "medium",
  "audio_only": false,
  "overwrite": true,
  "output_directory": "C:/Users/Usuario/Videos"
}
```
### Configurações Disponíveis
Configuração Valores Padrão Descrição output_format mp4, avi, mkv, mov, wmv, flv, webm mp4 Formato de saída quality low, medium, high, ultra medium Qualidade da conversão audio_only true, false false Converter apenas áudio overwrite true, false true Sobrescrever arquivos output_directory caminho "" Pasta de saída padrão

## 🔧 Solução de Problemas
### Problemas Comuns ❌ "FFmpeg não encontrado"
Solução :

1. Instale o FFmpeg:
   ```
   winget install FFmpeg
   ```
2. Reinicie o terminal
3. Teste: ffmpeg -version ❌ "ModuleNotFoundError: No module named 'tkinterdnd2'"
Solução :

```
python install_gui_dependencies.py
``` ❌ "'bool' object has no attribute '_root'"
Solução :

- Use video_converter_gui_final.py em vez de versões antigas
- Execute com --debug para mais informações ❌ "bad relief 'dashed'"
Solução :

- Atualizar para a versão mais recente
- Problema corrigido em video_converter_gui_final.py ❌ Conversão muito lenta
Soluções :

- Use qualidade "medium" ou "low"
- Feche outros programas pesados
- Verifique se o disco não está cheio ❌ Arquivo de saída corrompido
Soluções :

- Verifique se o arquivo de entrada não está corrompido
- Tente uma qualidade diferente
- Use o modo debug para ver erros detalhados
### Modo Debug
Para diagnóstico detalhado:

```
# Interface gráfica
python video_converter_gui_final.py --debug

# Linha de comando
python video_converter.py input.ts output.mp4 --debug

# Executável
VideoConverter.exe --debug
```
### Logs e Diagnóstico Verificar Instalação
```
python test_tkinter.py
``` Verificar FFmpeg
```
ffmpeg -version
``` Verificar Dependências
```
python -c "import tkinter, tkinterdnd2, PIL, cv2; print('Todas as 
dependências OK')"
```
## 🤝 Contribuição
### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature ( git checkout -b feature/AmazingFeature )
3. Commit suas mudanças ( git commit -m 'Add some AmazingFeature' )
4. Push para a branch ( git push origin feature/AmazingFeature )
5. Abra um Pull Request
### Diretrizes
- ✅ Mantenha o código limpo e documentado
- ✅ Teste suas mudanças antes de enviar
- ✅ Siga o padrão de código existente
- ✅ Adicione testes para novas funcionalidades
- ✅ Atualize a documentação quando necessário
### Reportar Bugs
Ao reportar bugs, inclua:

- Sistema Operacional e versão
- Versão do Python
- Versão do FFmpeg
- Passos para reproduzir o problema
- Logs de erro (use modo --debug )
- Arquivos de exemplo (se possível)
### Sugerir Melhorias
Sugestões são bem-vindas! Abra uma Issue com:

- Descrição clara da melhoria
- Justificativa para a mudança
- Exemplos de uso
- Implementação sugerida (opcional)
## 📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos
- FFmpeg Team - Engine de conversão
- Python Community - Linguagem e bibliotecas
- Tkinter Team - Interface gráfica
- Contribuidores - Melhorias e correções
## 📞 Suporte
- 📧 Email : [ seu-email@exemplo.com ]
- 🐛 Issues : GitHub Issues
- 💬 Discussões : GitHub Discussions
- 📖 Wiki : GitHub Wiki