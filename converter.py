import whisper
import torch
import time
import os

class WhisperConverter:
    """Whisper 음성 변환 로직을 담당하는 클래스"""
    
    def __init__(self, progress_callback=None, cancel_callback=None):
        self.progress_callback = progress_callback
        self.cancel_callback = cancel_callback
        self.is_cancelled = False
        self.start_time = None
        self.model = None  # 모델 캐싱을 위한 변수
        
    def convert_audio(self, audio_path, output_path, model_size, optimize_speed=True):
        """음성 파일을 텍스트로 변환"""
        try:
            self.start_time = time.time()
            self.is_cancelled = False
            
            # 진행률 추적을 위한 변수 초기화
            self.last_percentage = 0
            self.last_elapsed_time = 0
            
            # 1단계: 모델 로드 (10-30%)
            self._update_progress("🔧 Whisper 모델을 로드하는 중...", 10)
            if self._is_cancelled():
                return None
            
            # 모델이 이미 로드되어 있지 않거나 다른 모델인 경우에만 로드
            if self.model is None or not hasattr(self.model, 'name') or self.model.name != model_size:
                self.model = whisper.load_model(model_size)
                self._update_progress("✅ 모델 로드 완료", 20)
            else:
                self._update_progress("✅ 캐시된 모델 사용", 20)
            
            # 2단계: GPU 설정 및 최적화 (30-40%)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._update_progress(f"🚀 {device.upper()}에서 모델을 실행 중...", 30)
            
            self.model = self.model.to(device)
            
            # GPU 메모리 최적화
            if device == "cuda":
                torch.cuda.empty_cache()
                self._update_progress("💾 GPU 메모리 최적화 완료", 35)
            else:
                self._update_progress("💻 CPU 모드로 실행", 35)
            
            if self._is_cancelled():
                return None
            
            # 3단계: 변환 옵션 설정 (40-50%)
            self._update_progress("⚙️ 변환 옵션을 설정하는 중...", 40)
            
            transcribe_options = {
                "language": "ko",
                "verbose": False,
                "fp16": device == "cuda",  # GPU에서 16비트 정밀도 사용
                "temperature": 0.0,  # 결정적 출력으로 속도 향상
                "compression_ratio_threshold": 2.4,  # 압축 비율 임계값
                "logprob_threshold": -1.0,  # 로그 확률 임계값
                "no_speech_threshold": 0.6,  # 무음 임계값
            }
            
            # 속도 최적화 옵션 추가
            if optimize_speed:
                transcribe_options.update({
                    "beam_size": 1,  # 빔 검색 크기 최소화
                    "best_of": 1,    # 최적 후보 수 최소화
                    "patience": 1,   # 빔 검색 인내심 최소화
                })
                self._update_progress("⚡ 속도 최적화 옵션 적용", 45)
            else:
                self._update_progress("🎯 정확도 우선 옵션 적용", 45)
            
            # 4단계: 음성 파일 분석 (50-80%)
            self._update_progress("🎵 음성 파일을 분석하는 중...", 50)
            if self._is_cancelled():
                return None
            
            # 음성 파일 변환 (가장 시간이 오래 걸리는 부분)
            self._update_progress("🔄 음성을 텍스트로 변환하는 중... (이 단계가 가장 오래 걸립니다)", 60)
            result = self.model.transcribe(audio_path, **transcribe_options)
            
            if self._is_cancelled():
                return None
            
            # 5단계: 결과 후처리 (80-95%)
            self._update_progress("📝 변환 결과를 정리하는 중...", 80)
            
            # 텍스트 정리 (불필요한 공백 제거 등)
            cleaned_text = result["text"].strip()
            
            # 6단계: 파일 저장 (95-100%)
            self._update_progress("💾 결과를 파일에 저장하는 중...", 90)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
            
            self._update_progress("🎉 변환 완료!", 100)
            return cleaned_text
            
        except Exception as e:
            self._update_progress(f"❌ 오류 발생: {str(e)}", 0)
            raise e
    
    def _update_progress(self, message, percentage):
        """진행 상황 업데이트"""
        if self.progress_callback:
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            
            # 더 정확한 시간 예측 (이전 진행률과 비교)
            if hasattr(self, 'last_percentage') and hasattr(self, 'last_elapsed_time'):
                if percentage > self.last_percentage:
                    # 진행률이 증가한 경우에만 시간 예측 업데이트
                    progress_increase = percentage - self.last_percentage
                    time_increase = elapsed_time - self.last_elapsed_time
                    
                    if progress_increase > 0 and time_increase > 0:
                        # 현재 속도로 남은 진행률을 완료하는데 필요한 시간
                        remaining_progress = 100 - percentage
                        estimated_remaining = (remaining_progress / progress_increase) * time_increase
                    else:
                        estimated_remaining = 0
                else:
                    estimated_remaining = 0
            else:
                # 첫 번째 업데이트인 경우
                estimated_remaining = (elapsed_time / percentage * 100) - elapsed_time if percentage > 0 else 0
            
            # 이전 값 저장
            self.last_percentage = percentage
            self.last_elapsed_time = elapsed_time
            
            self.progress_callback(message, percentage, elapsed_time, estimated_remaining)
    
    def _is_cancelled(self):
        """취소 여부 확인"""
        if self.cancel_callback:
            self.is_cancelled = self.cancel_callback()
        return self.is_cancelled
    
    def cancel(self):
        """변환 취소"""
        self.is_cancelled = True
    
    def clear_model_cache(self):
        """모델 캐시 정리"""
        if self.model is not None:
            del self.model
            self.model = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    @staticmethod
    def get_optimization_tips():
        """속도 최적화 팁 반환"""
        tips = [
            "🎯 **모델 크기**: base 모델이 가장 빠릅니다",
            "⚡ **GPU 사용**: CUDA GPU가 있으면 CPU보다 3-5배 빠릅니다",
            "📁 **파일 크기**: 작은 파일일수록 빠릅니다",
            "🔧 **최적화 옵션**: 속도 최적화 옵션을 활성화하세요",
            "💾 **메모리**: 충분한 RAM과 VRAM을 확보하세요",
            "🔄 **캐싱**: 같은 모델을 재사용하면 로딩 시간이 단축됩니다"
        ]
        return tips 