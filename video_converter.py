import os
import sys
import ffmpeg
from pathlib import Path
import argparse
from typing import List, Optional

class VideoConverter:
    """Classe para conversão de diferentes formatos de vídeo e áudio"""
    
    def __init__(self):
        self.supported_video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.ts', '.m2ts']
        self.supported_audio_formats = ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']
    
    def check_ffmpeg(self) -> bool:
        """Verifica se o FFmpeg está instalado"""
        try:
            ffmpeg.probe('test')
            return True
        except ffmpeg.Error:
            return True  # FFmpeg está instalado, apenas falhou no probe
        except FileNotFoundError:
            return False
    
    def get_video_info(self, input_path: str) -> dict:
        """Obtém informações do vídeo"""
        try:
            probe = ffmpeg.probe(input_path)
            video_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_info = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            
            return {
                'duration': float(probe['format']['duration']),
                'size': int(probe['format']['size']),
                'video_codec': video_info['codec_name'] if video_info else None,
                'audio_codec': audio_info['codec_name'] if audio_info else None,
                'width': int(video_info['width']) if video_info else None,
                'height': int(video_info['height']) if video_info else None
            }
        except Exception as e:
            print(f"Erro ao obter informações do vídeo: {e}")
            return {}
    
    def convert_video(self, input_path: str, output_path: str, 
                     video_codec: str = 'libx264', audio_codec: str = 'aac',
                     quality: str = 'medium', resolution: Optional[str] = None) -> bool:
        """Converte vídeo para outro formato"""
        try:
            input_stream = ffmpeg.input(input_path)
            
            # Configurações de qualidade
            quality_settings = {
                'low': {'crf': 28, 'preset': 'fast'},
                'medium': {'crf': 23, 'preset': 'medium'},
                'high': {'crf': 18, 'preset': 'slow'},
                'best': {'crf': 15, 'preset': 'veryslow'}
            }
            
            settings = quality_settings.get(quality, quality_settings['medium'])
            
            # Configurar stream de saída
            output_args = {
                'vcodec': video_codec,
                'acodec': audio_codec,
                'crf': settings['crf'],
                'preset': settings['preset']
            }
            
            # Adicionar resolução se especificada
            if resolution:
                width, height = map(int, resolution.split('x'))
                output_args['s'] = f'{width}x{height}'
            
            output_stream = ffmpeg.output(input_stream, output_path, **output_args)
            
            # Executar conversão
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return True
            
        except Exception as e:
            print(f"Erro na conversão: {e}")
            return False
    
    def convert_to_audio(self, input_path: str, output_path: str, 
                        audio_codec: str = 'mp3', bitrate: str = '192k') -> bool:
        """Converte vídeo para áudio"""
        try:
            input_stream = ffmpeg.input(input_path)
            
            # Configurações de áudio
            audio_settings = {
                'acodec': audio_codec,
                'ab': bitrate,
                'vn': None  # Remove vídeo
            }
            
            output_stream = ffmpeg.output(input_stream, output_path, **audio_settings)
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return True
            
        except Exception as e:
            print(f"Erro na conversão para áudio: {e}")
            return False
    
    def batch_convert(self, input_dir: str, output_dir: str, 
                     output_format: str = 'mp4', quality: str = 'medium') -> List[str]:
        """Conversão em lote de vídeos"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        converted_files = []
        
        for file_path in input_path.iterdir():
            if file_path.suffix.lower() in self.supported_video_formats:
                output_file = output_path / f"{file_path.stem}.{output_format}"
                
                print(f"Convertendo: {file_path.name} -> {output_file.name}")
                
                if self.convert_video(str(file_path), str(output_file), quality=quality):
                    converted_files.append(str(output_file))
                    print(f"✓ Sucesso: {output_file.name}")
                else:
                    print(f"✗ Falha: {file_path.name}")
        
        return converted_files
    
    def ts_to_mp4_optimized(self, input_path: str, output_path: str) -> bool:
        """Conversão otimizada específica para .ts -> .mp4"""
        try:
            input_stream = ffmpeg.input(input_path)
            
            # Configurações otimizadas para TS -> MP4
            output_stream = ffmpeg.output(
                input_stream, 
                output_path,
                vcodec='libx264',
                acodec='aac',
                preset='medium',
                crf=23,
                movflags='faststart'  # Otimização para streaming
            )
            
            ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
            return True
            
        except Exception as e:
            print(f"Erro na conversão TS->MP4: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Conversor de Vídeo Universal')
    parser.add_argument('input', help='Arquivo ou diretório de entrada')
    parser.add_argument('-o', '--output', help='Arquivo ou diretório de saída')
    parser.add_argument('-f', '--format', default='mp4', help='Formato de saída (padrão: mp4)')
    parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high', 'best'], 
                       default='medium', help='Qualidade da conversão')
    parser.add_argument('-r', '--resolution', help='Resolução (ex: 1920x1080)')
    parser.add_argument('--audio-only', action='store_true', help='Converter apenas para áudio')
    parser.add_argument('--batch', action='store_true', help='Conversão em lote')
    parser.add_argument('--ts-optimized', action='store_true', help='Otimização específica para TS->MP4')
    
    args = parser.parse_args()
    
    converter = VideoConverter()
    
    # Verificar FFmpeg
    if not converter.check_ffmpeg():
        print("Erro: FFmpeg não encontrado. Instale o FFmpeg primeiro.")
        print("Download: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Erro: Arquivo/diretório não encontrado: {args.input}")
        sys.exit(1)
    
    # Conversão em lote
    if args.batch:
        if not input_path.is_dir():
            print("Erro: Para conversão em lote, especifique um diretório")
            sys.exit(1)
        
        output_dir = args.output or f"{args.input}_converted"
        converted = converter.batch_convert(str(input_path), output_dir, args.format, args.quality)
        print(f"\nConversão concluída! {len(converted)} arquivos convertidos.")
        return
    
    # Conversão individual
    if input_path.is_file():
        # Definir arquivo de saída
        if args.output:
            output_path = args.output
        else:
            if args.audio_only:
                output_path = f"{input_path.stem}.{args.format if args.format in ['mp3', 'wav', 'aac'] else 'mp3'}"
            else:
                output_path = f"{input_path.stem}.{args.format}"
        
        # Mostrar informações do arquivo
        print(f"Arquivo de entrada: {input_path}")
        info = converter.get_video_info(str(input_path))
        if info:
            print(f"Duração: {info.get('duration', 'N/A'):.2f}s")
            print(f"Resolução: {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
            print(f"Codec de vídeo: {info.get('video_codec', 'N/A')}")
            print(f"Codec de áudio: {info.get('audio_codec', 'N/A')}")
        
        print(f"\nIniciando conversão para: {output_path}")
        
        # Executar conversão
        success = False
        
        if args.audio_only:
            success = converter.convert_to_audio(str(input_path), output_path)
        elif args.ts_optimized and input_path.suffix.lower() == '.ts':
            success = converter.ts_to_mp4_optimized(str(input_path), output_path)
        else:
            success = converter.convert_video(
                str(input_path), output_path, 
                quality=args.quality, resolution=args.resolution
            )
        
        if success:
            print(f"✓ Conversão concluída com sucesso: {output_path}")
        else:
            print("✗ Falha na conversão")
            sys.exit(1)
    else:
        print("Erro: Especifique um arquivo válido")
        sys.exit(1)

if __name__ == "__main__":
    main()