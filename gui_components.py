import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pathlib import Path
from ui_theme import InstagramStyleUI

class FileSection:
    """파일 선택 섹션 컴포넌트"""
    
    def __init__(self, parent, row, title, path_var, browse_func, button_text):
        self.colors = InstagramStyleUI.setup_style()
        self.create_section(parent, row, title, path_var, browse_func, button_text)
    
    def create_section(self, parent, row, title, path_var, browse_func, button_text):
        """파일 선택 섹션 생성 (카드 스타일)"""
        # 카드 프레임
        card_frame = InstagramStyleUI.create_card_frame(parent)
        card_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # 제목
        title_label = tk.Label(card_frame, text=title, 
                              font=("Arial", 12, "bold"),
                              fg=self.colors['text'],
                              bg=self.colors['surface'])
        title_label.grid(row=0, column=0, sticky=tk.W, padx=15, pady=(15, 10))
        
        # 입력 프레임
        input_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=15, pady=(0, 15))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # 엔트리 (인스타그램 스타일)
        entry = tk.Entry(input_frame, textvariable=path_var, 
                        font=("Arial", 10),
                        relief="flat",
                        bg=self.colors['background'],
                        fg=self.colors['text'],
                        insertbackground=self.colors['primary'])
        entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10), pady=5)
        
        # 버튼 (인스타그램 스타일)
        browse_btn = InstagramStyleUI.create_instagram_button(input_frame, button_text, browse_func)
        browse_btn.grid(row=0, column=1)

class ModelSection:
    """모델 선택 섹션 컴포넌트"""
    
    def __init__(self, parent, row, model_size_var):
        self.colors = InstagramStyleUI.setup_style()
        self.create_section(parent, row, model_size_var)
    
    def create_section(self, parent, row, model_size_var):
        """모델 선택 섹션 생성 (카드 스타일)"""
        # 카드 프레임
        card_frame = InstagramStyleUI.create_card_frame(parent)
        card_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # 제목
        title_label = tk.Label(card_frame, text="모델 크기 선택", 
                              font=("Arial", 12, "bold"),
                              fg=self.colors['text'],
                              bg=self.colors['surface'])
        title_label.grid(row=0, column=0, sticky=tk.W, padx=15, pady=(15, 10))
        
        # 모델 옵션 프레임
        model_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        model_frame.grid(row=1, column=0, sticky=tk.W, padx=15, pady=(0, 15))
        
        model_sizes = [
            ("⚡ 빠름 (base)", "base", self.colors['success']),
            ("⚖️ 균형 (small)", "small", self.colors['warning']),
            ("🎯 정확도 (medium)", "medium", self.colors['accent']),
            ("🏆 최고 정확도 (large)", "large", self.colors['primary'])
        ]
        
        for i, (text, value, color) in enumerate(model_sizes):
            btn = tk.Radiobutton(model_frame, text=text, variable=model_size_var, 
                               value=value, font=("Arial", 10),
                               bg=self.colors['surface'], fg=self.colors['text'],
                               selectcolor=self.colors['background'],
                               activebackground=self.colors['surface'],
                               activeforeground=color)
            btn.grid(row=0, column=i, padx=(0, 15))

class OptimizationSection:
    """속도 최적화 섹션 컴포넌트"""
    
    def __init__(self, parent, row, optimize_var):
        self.colors = InstagramStyleUI.setup_style()
        self.optimize_var = optimize_var
        self.create_section(parent, row)
    
    def create_section(self, parent, row):
        """속도 최적화 섹션 생성 (카드 스타일)"""
        # 카드 프레임
        card_frame = InstagramStyleUI.create_card_frame(parent)
        card_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # 제목
        title_label = tk.Label(card_frame, text="⚡ 속도 최적화", 
                              font=("Arial", 12, "bold"),
                              fg=self.colors['text'],
                              bg=self.colors['surface'])
        title_label.grid(row=0, column=0, sticky=tk.W, padx=15, pady=(15, 10))
        
        # 최적화 옵션 프레임
        opt_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        opt_frame.grid(row=1, column=0, sticky=tk.W, padx=15, pady=(0, 15))
        
        # 속도 최적화 체크박스
        optimize_check = tk.Checkbutton(opt_frame, 
                                       text="🚀 속도 최적화 활성화 (빠른 변환)",
                                       variable=self.optimize_var,
                                       font=("Arial", 10),
                                       bg=self.colors['surface'], 
                                       fg=self.colors['text'],
                                       selectcolor=self.colors['background'],
                                       activebackground=self.colors['surface'],
                                       activeforeground=self.colors['accent'])
        optimize_check.grid(row=0, column=0, sticky=tk.W)
        
        # 최적화 설명
        desc_label = tk.Label(opt_frame,
                             text="빔 검색 최소화, 결정적 출력으로 속도 향상 (정확도 약간 감소)",
                             font=("Arial", 9),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['surface'])
        desc_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

class ProgressSection:
    """진행 상황 섹션 컴포넌트"""
    
    def __init__(self, parent, row):
        self.colors = InstagramStyleUI.setup_style()
        self.progress_var = tk.StringVar(value="대기 중...")
        self.time_var = tk.StringVar(value="")
        self.percent_var = tk.StringVar(value="0%")
        self.progress = None
        self.status_label = None
        self.create_section(parent, row)
    
    def create_section(self, parent, row):
        """진행 상황 섹션 생성 (카드 스타일)"""
        # 카드 프레임
        card_frame = InstagramStyleUI.create_card_frame(parent)
        card_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # 제목
        title_label = tk.Label(card_frame, text="🔄 변환 진행 상황", 
                              font=("Arial", 12, "bold"),
                              fg=self.colors['text'],
                              bg=self.colors['surface'])
        title_label.grid(row=0, column=0, sticky=tk.W, padx=15, pady=(15, 10))
        
        # 진행 상황 프레임
        progress_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=15, pady=(0, 15))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        # 상태 메시지 (더 큰 폰트로)
        self.status_label = tk.Label(progress_frame, textvariable=self.progress_var,
                                    font=("Arial", 11),
                                    fg=self.colors['text'],
                                    bg=self.colors['surface'],
                                    wraplength=600)  # 긴 메시지 자동 줄바꿈
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # 예상 시간 (더 눈에 띄게)
        time_label = tk.Label(progress_frame, textvariable=self.time_var,
                             font=("Arial", 10, "bold"),
                             fg=self.colors['accent'],
                             bg=self.colors['surface'])
        time_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 12))
        
        # 진행바 프레임
        progressbar_frame = tk.Frame(progress_frame, bg=self.colors['surface'])
        progressbar_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        progressbar_frame.grid_columnconfigure(0, weight=1)
        
        # 진행바 (더 두껍게, 실시간 업데이트 지원)
        self.progress = ttk.Progressbar(progressbar_frame, mode='determinate', length=400, style='Custom.Horizontal.TProgressbar')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 퍼센트 표시 (더 눈에 띄게)
        percent_label = tk.Label(progressbar_frame, textvariable=self.percent_var,
                                font=("Arial", 12, "bold"),
                                fg=self.colors['primary'],
                                bg=self.colors['surface'])
        percent_label.grid(row=0, column=1, padx=(10, 0))
        
        # 진행 단계 표시
        self.stage_label = tk.Label(progress_frame, text="단계: 대기 중",
                                   font=("Arial", 9),
                                   fg=self.colors['text_secondary'],
                                   bg=self.colors['surface'])
        self.stage_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        
        # 실시간 진행률 표시를 위한 추가 정보
        self.detail_label = tk.Label(progress_frame, text="",
                                    font=("Arial", 9),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['surface'])
        self.detail_label.grid(row=4, column=0, sticky=tk.W, pady=(5, 0))

class ResultSection:
    """결과 섹션 컴포넌트"""
    
    def __init__(self, parent, row):
        self.colors = InstagramStyleUI.setup_style()
        self.result_text = None
        self.create_section(parent, row)
    
    def create_section(self, parent, row):
        """결과 섹션 생성 (카드 스타일)"""
        # 카드 프레임
        card_frame = InstagramStyleUI.create_card_frame(parent)
        card_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=5)
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_rowconfigure(1, weight=1)
        
        # 제목
        title_label = tk.Label(card_frame, text="변환 결과", 
                              font=("Arial", 12, "bold"),
                              fg=self.colors['text'],
                              bg=self.colors['surface'])
        title_label.grid(row=0, column=0, sticky=tk.W, padx=15, pady=(15, 10))
        
        # 텍스트 영역
        text_frame = tk.Frame(card_frame, bg=self.colors['surface'])
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15))
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(
            text_frame, 
            height=12, 
            width=70,
            font=("Arial", 10),
            bg=self.colors['background'],
            fg=self.colors['text'],
            relief="flat",
            insertbackground=self.colors['primary']
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) 