import torch
import sys
import subprocess
import platform

def check_gpu_status():
    """GPU 상태를 자세히 확인하는 함수"""
    print("🔍 GPU 상태 확인 중...\n")
    
    # 1. PyTorch 버전 확인
    print(f"📦 PyTorch 버전: {torch.__version__}")
    
    # 2. CUDA 사용 가능 여부
    cuda_available = torch.cuda.is_available()
    print(f"⚡ CUDA 사용 가능: {'✅ 예' if cuda_available else '❌ 아니오'}")
    
    if cuda_available:
        # 3. CUDA 버전
        cuda_version = torch.version.cuda
        print(f"🔧 CUDA 버전: {cuda_version}")
        
        # 4. GPU 개수
        gpu_count = torch.cuda.device_count()
        print(f"🎮 GPU 개수: {gpu_count}")
        
        # 5. 각 GPU 정보
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3  # GB
            print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
        
        # 6. 현재 GPU
        current_device = torch.cuda.current_device()
        print(f"🎯 현재 GPU: {current_device}")
        
        # 7. GPU 메모리 사용량
        allocated = torch.cuda.memory_allocated() / 1024**3
        cached = torch.cuda.memory_reserved() / 1024**3
        print(f"💾 GPU 메모리 사용량: {allocated:.2f}GB (할당됨) / {cached:.2f}GB (캐시됨)")
        
    else:
        print("\n❌ CUDA를 사용할 수 없는 이유:")
        
        # PyTorch가 CPU 버전인지 확인
        if not hasattr(torch, 'cuda'):
            print("   • PyTorch가 CPU 전용 버전으로 설치됨")
        else:
            print("   • CUDA 드라이버가 설치되지 않음")
            print("   • NVIDIA GPU가 없음")
            print("   • CUDA 버전이 호환되지 않음")
    
    # 8. 시스템 정보
    print(f"\n💻 시스템 정보:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version}")
    
    return cuda_available

def check_nvidia_driver():
    """NVIDIA 드라이버 설치 여부 확인"""
    print("\n🔧 NVIDIA 드라이버 확인 중...")
    
    try:
        # nvidia-smi 명령어 실행
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ NVIDIA 드라이버가 설치되어 있습니다.")
            print("📋 GPU 정보:")
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # 처음 10줄만 출력
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print("❌ NVIDIA 드라이버가 설치되지 않았습니다.")
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi 명령어를 찾을 수 없습니다.")
        return False
    except subprocess.TimeoutExpired:
        print("❌ nvidia-smi 명령어 실행 시간 초과.")
        return False

def install_gpu_pytorch():
    """GPU용 PyTorch 설치 방법 안내"""
    print("\n🚀 GPU용 PyTorch 설치 방법:")
    print("1. 현재 PyTorch 제거:")
    print("   pip uninstall torch torchaudio")
    print("\n2. GPU용 PyTorch 설치 (CUDA 11.8 기준):")
    print("   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118")
    print("\n3. 또는 CUDA 12.1용:")
    print("   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print("\n4. 설치 후 확인:")
    print("   python -c \"import torch; print(torch.cuda.is_available())\"")

def main():
    print("🎤 Whisper GPU 상태 확인 도구")
    print("=" * 50)
    
    # GPU 상태 확인
    cuda_available = check_gpu_status()
    
    # NVIDIA 드라이버 확인
    nvidia_available = check_nvidia_driver()
    
    print("\n" + "=" * 50)
    print("📊 종합 결과:")
    
    if cuda_available and nvidia_available:
        print("✅ GPU 사용 가능! Whisper가 GPU에서 실행됩니다.")
        print("💡 권장사항: base 모델 + 최적화 옵션으로 빠른 변환을 경험하세요!")
    elif nvidia_available and not cuda_available:
        print("⚠️  NVIDIA GPU는 있지만 PyTorch가 CPU 버전입니다.")
        print("💡 해결방법: GPU용 PyTorch를 설치하세요.")
        install_gpu_pytorch()
    else:
        print("❌ GPU 사용이 불가능합니다.")
        print("💡 CPU에서도 Whisper가 동작하지만 속도가 느릴 수 있습니다.")
        print("💡 GPU 사용을 원한다면 NVIDIA GPU와 드라이버를 설치하세요.")

if __name__ == "__main__":
    main() 