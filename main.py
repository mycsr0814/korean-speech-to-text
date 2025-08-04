import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
from datetime import timedelta

# 분할된 모듈들 import
from converter import WhisperConverter
from ui_theme import InstagramStyleUI
from gui_components import FileSection, ModelSection, ProgressSection, ResultSection, OptimizationSection

class WhisperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Whisper 음성-텍스트 변환기")
        self.root.geometry("800x800")  # 창 크기를 더 크게 설정
        self.root.resizable(True, True)
        
        # 인스타그램 스타일 적용
        self.colors = InstagramStyleUI.setup_style()
        self.root.configure(bg=self.colors['background'])
        
        # 변수 초기화
        self.audio_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.model_size = tk.StringVar(value="base")
        self.optimize_speed = tk.BooleanVar(value=True)  # 기본적으로 최적화 활성화
        self.is_processing = False
        self.converter = None
        
        # GUI 컴포넌트들
        self.progress_section = None
        self.result_section = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 스크롤 가능한 캔버스 생성
        canvas = tk.Canvas(main_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style='Vertical.TScrollbar')
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 마우스 휠 스크롤 지원
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 제목 (인스타그램 스타일)
        title_frame = tk.Frame(scrollable_frame)
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        title_label = tk.Label(title_frame, 
                              text="🎤 Whisper", 
                              font=("Arial", 24, "bold"),
                              fg=self.colors['primary'],
                              bg=self.colors['background'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="음성을 텍스트로 변환하세요",
                                 font=("Arial", 12),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['background'])
        subtitle_label.pack()
        
        # 입력 파일 선택 (카드 스타일)
        FileSection(scrollable_frame, 1, "음성 파일 선택", 
                   self.audio_path, self.browse_audio_file, "파일 찾기")
        
        # 출력 파일 선택 (카드 스타일)
        FileSection(scrollable_frame, 3, "저장 경로 설정", 
                   self.output_path, self.browse_output_file, "저장 위치")
        
        # 모델 크기 선택 (카드 스타일)
        ModelSection(scrollable_frame, 5, self.model_size)
        
        # 속도 최적화 섹션 (카드 스타일)
        OptimizationSection(scrollable_frame, 7, self.optimize_speed)
        
        # 버튼 프레임
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        # 변환 버튼
        self.convert_btn = tk.Button(button_frame, 
                                   text="🎵 변환 시작", 
                                   command=self.start_conversion,
                                   bg=self.colors['accent'],
                                   fg='white',
                                   font=("Arial", 14, "bold"),
                                   relief="flat",
                                   padx=30,
                                   pady=10,
                                   cursor="hand2")
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 취소 버튼
        self.cancel_btn = tk.Button(button_frame,
                                  text="❌ 취소",
                                  command=self.cancel_conversion,
                                  bg=self.colors['text_secondary'],
                                  fg='white',
                                  font=("Arial", 12),
                                  relief="flat",
                                  padx=20,
                                  pady=10,
                                  cursor="hand2",
                                  state="disabled")
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 도움말 버튼
        help_btn = tk.Button(button_frame,
                           text="❓ 속도 팁",
                           command=self.show_speed_tips,
                           bg=self.colors['primary'],
                           fg='white',
                           font=("Arial", 10),
                           relief="flat",
                           padx=15,
                           pady=10,
                           cursor="hand2")
        help_btn.pack(side=tk.LEFT)
        
        # 진행 상황 표시 (카드 스타일)
        self.progress_section = ProgressSection(scrollable_frame, 10)
        
        # 결과 텍스트 영역 (카드 스타일)
        self.result_section = ResultSection(scrollable_frame, 12)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 캔버스와 스크롤바 배치
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 창 크기 변경 시 캔버스 크기 조정
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind('<Configure>', configure_scroll_region)
    
    def show_speed_tips(self):
        """속도 최적화 팁 표시"""
        tips = WhisperConverter.get_optimization_tips()
        tips_text = "\n".join(tips)
        
        messagebox.showinfo(
            "🚀 속도 최적화 팁", 
            f"음성 변환 속도를 향상시키는 방법들:\n\n{tips_text}\n\n"
            "💡 현재 설정:\n"
            f"• 모델: {self.model_size.get()}\n"
            f"• 최적화: {'활성화' if self.optimize_speed.get() else '비활성화'}\n"
            f"• GPU: {'사용 가능' if self.check_gpu() else 'CPU 사용'}"
        )
    
    def check_gpu(self):
        """GPU 사용 가능 여부 확인"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
        
    def browse_audio_file(self):
        """음성 파일 선택"""
        filetypes = [
            ("음성 파일", "*.wav *.mp3 *.m4a *.flac *.ogg *.wma"),
            ("WAV 파일", "*.wav"),
            ("MP3 파일", "*.mp3"),
            ("모든 파일", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="음성 파일을 선택하세요",
            filetypes=filetypes
        )
        
        if filename:
            self.audio_path.set(filename)
            # 자동으로 출력 파일명 생성
            audio_file = Path(filename)
            output_file = audio_file.parent / f"{audio_file.stem}_변환결과.txt"
            self.output_path.set(str(output_file))
    
    def browse_output_file(self):
        """저장 파일 선택"""
        filename = filedialog.asksaveasfilename(
            title="저장할 위치를 선택하세요",
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        
        if filename:
            self.output_path.set(filename)
    
    def start_conversion(self):
        """변환 시작"""
        if self.is_processing:
            return
            
        # 입력 검증
        if not self.audio_path.get():
            messagebox.showerror("오류", "음성 파일을 선택해주세요!")
            return
            
        if not self.output_path.get():
            messagebox.showerror("오류", "저장 경로를 설정해주세요!")
            return
            
        if not os.path.exists(self.audio_path.get()):
            messagebox.showerror("오류", "선택한 음성 파일이 존재하지 않습니다!")
            return
        
        # UI 상태 변경
        self.is_processing = True
        self.convert_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_section.progress_var.set("모델을 로드하는 중...")
        self.progress_section.progress.config(value=0)
        self.progress_section.percent_var.set("0%")
        self.progress_section.time_var.set("")
        self.result_section.result_text.delete(1.0, tk.END)
        
        # 변환기 초기화
        self.converter = WhisperConverter(
            progress_callback=self.update_progress,
            cancel_callback=self.is_cancelled
        )
        
        # 별도 스레드에서 변환 실행
        thread = threading.Thread(target=self.convert_audio)
        thread.daemon = True
        thread.start()
    
    def convert_audio(self):
        """음성 변환 실행"""
        try:
            result = self.converter.convert_audio(
                self.audio_path.get(),
                self.output_path.get(),
                self.model_size.get(),
                self.optimize_speed.get()  # 최적화 옵션 전달
            )
            
            if result and not self.is_cancelled():
                self.show_result(result)
                messagebox.showinfo("완료", "음성 변환이 완료되었습니다!")
            
        except Exception as e:
            if not self.is_cancelled():
                messagebox.showerror("오류", f"변환 중 오류가 발생했습니다:\n{str(e)}")
        finally:
            # UI 상태 복원
            self.root.after(0, self.finish_conversion)
    
    def cancel_conversion(self):
        """변환 취소"""
        if self.converter:
            self.converter.cancel()
        self.finish_conversion()
        messagebox.showinfo("취소", "변환이 취소되었습니다.")
    
    def is_cancelled(self):
        """취소 여부 확인"""
        return not self.is_processing
    
    def update_progress(self, message, percentage, elapsed_time, remaining_time):
        """진행 상황 업데이트"""
        def update():
            self.progress_section.progress_var.set(message)
            self.progress_section.progress.config(value=percentage)
            self.progress_section.percent_var.set(f"{percentage}%")
            
            # 단계별 진행 상황 표시
            stage = self._get_stage_from_percentage(percentage)
            self.progress_section.stage_label.config(text=f"단계: {stage}")
            
            # 시간 정보 포맷팅
            if elapsed_time > 0:
                elapsed_str = self._format_time(elapsed_time)
                
                if remaining_time > 0 and percentage < 100:
                    remaining_str = self._format_time(remaining_time)
                    time_info = f"⏱️ 경과: {elapsed_str} | ⏳ 예상 남은 시간: {remaining_str}"
                else:
                    time_info = f"⏱️ 총 소요 시간: {elapsed_str}"
                
                self.progress_section.time_var.set(time_info)
            else:
                self.progress_section.time_var.set("")
        
        self.root.after(0, update)
    
    def _get_stage_from_percentage(self, percentage):
        """퍼센트에 따른 단계 반환"""
        if percentage == 0:
            return "대기 중"
        elif percentage <= 20:
            return "모델 로드"
        elif percentage <= 40:
            return "시스템 설정"
        elif percentage <= 50:
            return "옵션 설정"
        elif percentage <= 80:
            return "음성 변환"
        elif percentage <= 95:
            return "결과 처리"
        else:
            return "완료"
    
    def _format_time(self, seconds):
        """시간을 읽기 쉬운 형태로 포맷팅"""
        if seconds < 60:
            return f"{int(seconds)}초"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}분 {secs}초"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours}시간 {minutes}분 {secs}초"
    
    def show_result(self, text):
        """결과 텍스트 표시"""
        self.root.after(0, lambda: self.result_section.result_text.insert(tk.END, text))
    
    def finish_conversion(self):
        """변환 완료 후 UI 상태 복원"""
        self.is_processing = False
        self.convert_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self.progress_section.progress.stop()

def main():
    root = tk.Tk()
    app = WhisperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()