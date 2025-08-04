import tkinter as tk
from tkinter import ttk

class InstagramStyleUI:
    """인스타그램 스타일의 UI 테마"""
    
    @staticmethod
    def setup_style():
        """인스타그램 스타일 설정"""
        style = ttk.Style()
        
        # 색상 팔레트 (인스타그램 스타일)
        colors = {
            'primary': '#405DE6',      # 인스타그램 블루
            'secondary': '#5851DB',    # 보라색
            'accent': '#833AB4',       # 핑크
            'success': '#FD1D1D',      # 빨간색
            'warning': '#F77737',      # 주황색
            'background': '#FAFAFA',   # 밝은 회색
            'surface': '#FFFFFF',      # 흰색
            'text': '#262626',         # 진한 회색
            'text_secondary': '#8E8E93' # 연한 회색
        }
        
        # 기본 스타일 설정
        style.configure('TFrame', background=colors['background'])
        style.configure('TLabel', background=colors['background'], foreground=colors['text'])
        style.configure('TButton', 
                       background=colors['primary'], 
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))
        
        # 강조 버튼 스타일
        style.configure('Accent.TButton',
                       background=colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 12, 'bold'))
        
        # 취소 버튼 스타일
        style.configure('Cancel.TButton',
                       background=colors['text_secondary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10))
        
        # 진행바 스타일
        style.configure('TProgressbar',
                       background=colors['primary'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       lightcolor=colors['primary'],
                       darkcolor=colors['primary'])
        
        # 커스텀 진행바 스타일 (더 두껍고 눈에 띄게)
        style.configure('Custom.Horizontal.TProgressbar',
                       background=colors['accent'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       lightcolor=colors['accent'],
                       darkcolor=colors['accent'],
                       thickness=15)  # 더 두껍게
        
        # 진행률별 색상 변경을 위한 스타일들
        style.configure('Progress.Horizontal.TProgressbar',
                       background=colors['primary'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       lightcolor=colors['primary'],
                       darkcolor=colors['primary'],
                       thickness=15)
        
        # 성공 진행률 스타일
        style.configure('Success.Horizontal.TProgressbar',
                       background=colors['success'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       lightcolor=colors['success'],
                       darkcolor=colors['success'],
                       thickness=15)
        
        # 경고 진행률 스타일
        style.configure('Warning.Horizontal.TProgressbar',
                       background=colors['warning'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       lightcolor=colors['warning'],
                       darkcolor=colors['warning'],
                       thickness=15)
        
        # 스크롤바 스타일
        style.configure('Vertical.TScrollbar',
                       background=colors['primary'],
                       troughcolor=colors['background'],
                       borderwidth=0,
                       arrowcolor=colors['text'],
                       width=12)
        
        return colors
    
    @staticmethod
    def create_card_frame(parent, **kwargs):
        """카드 스타일 프레임 생성"""
        colors = InstagramStyleUI.setup_style()
        card_frame = tk.Frame(parent, bg=colors['surface'], relief="flat", bd=1, **kwargs)
        return card_frame
    
    @staticmethod
    def create_instagram_button(parent, text, command, bg_color=None, **kwargs):
        """인스타그램 스타일 버튼 생성"""
        colors = InstagramStyleUI.setup_style()
        if bg_color is None:
            bg_color = colors['primary']
            
        button = tk.Button(parent, 
                          text=text,
                          command=command,
                          bg=bg_color,
                          fg='white',
                          font=("Arial", 10, "bold"),
                          relief="flat",
                          padx=15,
                          pady=5,
                          cursor="hand2",
                          **kwargs)
        return button 