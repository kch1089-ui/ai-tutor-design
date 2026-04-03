from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1440, 900
FONT_REG  = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
FONT_BOLD = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
OUT = "/home/user/ai-tutor-design/designs"
os.makedirs(OUT, exist_ok=True)

# ── theme definitions ──────────────────────────────────────────────────────────
THEMES = [
    {"id":"theme1_starlight","name":"별빛 학교",
     "primary":(255,215,0),"sec":(255,140,0),"acc":(130,60,220),
     "bg":(255,253,230),"nav":(255,215,0),"card":(255,255,255),
     "txt":(50,30,10),"nav_txt":(60,40,0),"dark":False},
    {"id":"theme2_ocean","name":"바다 탐험",
     "primary":(0,180,216),"sec":(0,119,182),"acc":(0,245,212),
     "bg":(224,247,250),"nav":(0,180,216),"card":(255,255,255),
     "txt":(10,40,60),"nav_txt":(255,255,255),"dark":False},
    {"id":"theme3_fairytale","name":"동화 나라",
     "primary":(240,98,146),"sec":(171,71,188),"acc":(255,204,128),
     "bg":(252,228,236),"nav":(240,98,146),"card":(255,255,255),
     "txt":(60,20,40),"nav_txt":(255,255,255),"dark":False},
    {"id":"theme4_rainbow","name":"무지개 마을",
     "primary":(255,82,82),"sec":(255,171,64),"acc":(64,196,255),
     "bg":(255,255,255),"nav":(255,82,82),"card":(255,255,255),
     "txt":(30,30,30),"nav_txt":(255,255,255),"dark":False,
     "rainbow":True},
    {"id":"theme5_space","name":"우주 탐험대",
     "primary":(124,77,255),"sec":(0,191,165),"acc":(255,214,0),
     "bg":(13,27,75),"nav":(26,35,126),"card":(25,45,110),
     "txt":(220,230,255),"nav_txt":(255,255,255),"dark":True},
    {"id":"theme6_lemon","name":"레몬 팝",
     "primary":(255,230,0),"sec":(100,220,50),"acc":(255,100,150),
     "bg":(255,255,230),"nav":(255,230,0),"card":(255,255,255),
     "txt":(40,50,10),"nav_txt":(50,50,10),"dark":False,
     "lemon":True},
    {"id":"theme7_mint","name":"민트 프레시",
     "primary":(0,230,180),"sec":(0,200,230),"acc":(255,90,130),
     "bg":(230,255,250),"nav":(0,220,170),"card":(255,255,255),
     "txt":(10,60,50),"nav_txt":(255,255,255),"dark":False},
    {"id":"theme8_peach","name":"복숭아 동산",
     "primary":(255,140,80),"sec":(255,100,130),"acc":(80,210,230),
     "bg":(255,240,230),"nav":(255,140,80),"card":(255,255,255),
     "txt":(80,30,10),"nav_txt":(255,255,255),"dark":False,
     "peach":True},
    # ── new layout themes ──
    {"id":"theme9_split","name":"산호 스플릿",
     "primary":(255,107,107),"sec":(78,205,196),"acc":(255,230,100),
     "bg":(247,255,254),"nav":(255,107,107),"card":(255,255,255),
     "txt":(40,30,30),"nav_txt":(255,255,255),"dark":False,"layout":"split"},
    {"id":"theme10_dash","name":"바이올렛 대시",
     "primary":(108,99,255),"sec":(255,180,50),"acc":(80,220,180),
     "bg":(245,243,255),"nav":(108,99,255),"card":(255,255,255),
     "txt":(30,20,60),"nav_txt":(255,255,255),"dark":False,"layout":"dashboard"},
    {"id":"theme11_immersive","name":"에메랄드 몰입",
     "primary":(0,200,150),"sec":(255,217,61),"acc":(255,100,130),
     "bg":(240,255,250),"nav":(0,200,150),"card":(255,255,255),
     "txt":(10,50,40),"nav_txt":(255,255,255),"dark":False,"layout":"immersive"},
]

# ── helpers ────────────────────────────────────────────────────────────────────
def fnt(size, bold=False):
    try: return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except: return ImageFont.load_default()

def rr(draw, x1,y1,x2,y2, r, fill, outline=None, ow=2):
    draw.rounded_rectangle([x1,y1,x2,y2], radius=r, fill=fill,
                            outline=outline, width=ow)

def txt(draw, text, x, y, font, color, anchor="la"):
    draw.text((x,y), text, font=font, fill=color, anchor=anchor)

def btn(draw, x1,y1,x2,y2, label, f, bg, fg, r=22):
    rr(draw, x1,y1,x2,y2, r, bg)
    cx,cy = (x1+x2)//2,(y1+y2)//2
    txt(draw, label, cx, cy, f, fg, anchor="mm")

def avatar(draw, cx, cy, sz, color, bg=(80,80,120)):
    # head
    hr = sz//4
    draw.ellipse([cx-hr, cy-sz//2, cx+hr, cy-sz//2+hr*2], fill=color)
    # eyes
    eo = hr//3
    ey = cy - sz//2 + hr
    draw.ellipse([cx-eo-4, ey-4, cx-eo+4, ey+4], fill=(255,255,255))
    draw.ellipse([cx+eo-4, ey-4, cx+eo+4, ey+4], fill=(255,255,255))
    draw.ellipse([cx-eo-2, ey-2, cx-eo+2, ey+2], fill=(40,40,40))
    draw.ellipse([cx+eo-2, ey-2, cx+eo+2, ey+2], fill=(40,40,40))
    # smile
    draw.arc([cx-eo, ey+6, cx+eo, ey+6+eo], 0, 180, fill=(40,40,40), width=3)
    # body
    bw, bh = sz//3, sz//2
    rr(draw, cx-bw, cy-sz//4+hr*2-10, cx+bw, cy+bh, 15, color)

def nav_bar(draw, img, t, height=68):
    # background
    if t.get("rainbow"):
        # gradient nav
        for x in range(W):
            r = int(255 - (255-64)*x/W)
            g = int(82 + (196-82)*x/W)
            b = int(82 + (255-82)*x/W)
            draw.line([(x,0),(x,height)], fill=(r,g,b))
    else:
        draw.rectangle([0,0,W,height], fill=t["nav"])

    # logo circle
    draw.ellipse([18,14,54,54], fill=t["acc"])
    txt(draw,"AI",36,34,fnt(14,True),t["nav_txt"],anchor="mm")
    txt(draw,"AI선생님",62,34,fnt(18,True),t["nav_txt"],anchor="lm")

    # nav links
    links=["홈","수업","게시판","리포트"]
    for i,l in enumerate(links):
        lx = 560+i*110
        txt(draw,l,lx,34,fnt(15),t["nav_txt"],anchor="mm")

    # right buttons
    rr(draw,1220,18,1320,50,16,(255,255,255,80))
    txt(draw,"로그인",1270,34,fnt(13),t["nav_txt"],anchor="mm")
    rr(draw,1330,18,1420,50,16,t["acc"])
    txt(draw,"회원가입",1375,34,fnt(13),(255,255,255),anchor="mm")

def shadow_card(draw, x1,y1,x2,y2, r, fill):
    # simple drop shadow
    draw.rounded_rectangle([x1+4,y1+4,x2+4,y2+4], radius=r,
                            fill=(180,180,180,60))
    rr(draw,x1,y1,x2,y2,r,fill)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: MAIN
# ══════════════════════════════════════════════════════════════════════════════
def draw_main(t):
    img = Image.new("RGB",(W,H),t["bg"])
    draw = ImageDraw.Draw(img, "RGBA")

    NAV_H = 68
    HERO_H = 360
    FEAT_H = 280

    # ── HERO ──────────────────────────────────────────────────────────────────
    # hero gradient bg
    hero_c1 = t["primary"]
    hero_c2 = tuple(min(255,c+60) for c in t["sec"])
    for y in range(NAV_H, NAV_H+HERO_H):
        f = (y - NAV_H) / HERO_H
        r = int(hero_c1[0]*(1-f)+hero_c2[0]*f)
        g = int(hero_c1[1]*(1-f)+hero_c2[1]*f)
        b = int(hero_c1[2]*(1-f)+hero_c2[2]*f)
        draw.line([(0,y),(W,y)],fill=(r,g,b))

    # headline
    htxt = t["nav_txt"] if not t["dark"] else (255,255,255)
    txt(draw,"AI 선생님과 함께하는",80,NAV_H+55,fnt(36,True),htxt)
    txt(draw,"스마트 학습!",80,NAV_H+105,fnt(48,True),htxt)
    txt(draw,"내가 원하는 아바타로 배우는 즐거운 공부",80,NAV_H+170,fnt(20),(255,255,255))

    btn(draw,80,NAV_H+220,320,NAV_H+270,"무료로 시작하기",
        fnt(18,True),(255,255,255),t["acc"],r=28)
    btn(draw,340,NAV_H+220,500,NAV_H+270,"체험해보기",
        fnt(16),(0,0,0,50),(255,255,255),r=28)

    # avatar display box
    rr(draw,880,NAV_H+30,1200,NAV_H+310,30,(0,0,0,40))
    rr(draw,884,NAV_H+34,1196,NAV_H+306,28,t["card"])
    avatar(draw,1042,NAV_H+175,200,t["acc"])
    txt(draw,"나만의 AI 선생님",1042,NAV_H+290,fnt(14,True),t["txt"],anchor="mm")

    # floating badges
    rr(draw,850,NAV_H+60,1010,NAV_H+100,20,(255,255,255,200))
    txt(draw,"🎤 음성 질문 가능",870,NAV_H+80,fnt(13),t["txt"],anchor="lm")
    rr(draw,1040,NAV_H+270,1200,NAV_H+310,20,(255,255,255,200))
    txt(draw,"📊 실시간 집중도 체크",1050,NAV_H+290,fnt(13),t["txt"],anchor="lm")

    # ── FEATURES ──────────────────────────────────────────────────────────────
    feat_y = NAV_H + HERO_H + 20
    txt(draw,"주요 기능",W//2,feat_y+10,fnt(24,True),t["txt"],anchor="mm")

    cards=[
        ("마이크","실시간 질문","수업 중 언제든지\n음성으로 질문"),
        ("눈","집중도 체크","카메라로 시선 분석\n집중 상태 확인"),
        ("별","맞춤형 수업","AI가 수준에 맞게\n커스텀 수업 제공"),
        ("차트","학부모 리포트","수업 태도와 성적을\n학부모에게 전달"),
    ]
    cx_starts=[80,400,720,1040]
    for i,(ico,title,desc) in enumerate(cards):
        cx0=cx_starts[i]; cy0=feat_y+45
        shadow_card(draw,cx0,cy0,cx0+310,cy0+195,20,t["card"])
        # icon circle
        draw.ellipse([cx0+20,cy0+15,cx0+80,cy0+75],fill=t["primary"])
        txt(draw,ico,cx0+50,cy0+48,fnt(22),t["txt"],anchor="mm")
        txt(draw,title,cx0+100,cy0+28,fnt(16,True),t["txt"])
        for j,line in enumerate(desc.split("\n")):
            txt(draw,line,cx0+20,cy0+95+j*22,fnt(13),
                (120,120,120) if not t["dark"] else (180,180,200))

    # ── FOOTER ────────────────────────────────────────────────────────────────
    footer_y = H-72
    draw.rectangle([0,footer_y,W,H],fill=(30,30,50) if not t["dark"] else (10,15,40))
    txt(draw,"© 2025 AI선생님 | 모든 연령 대상 스마트 학습 플랫폼",
        W//2,footer_y+36,fnt(13),(160,160,180),anchor="mm")

    nav_bar(draw,img,t)
    return img

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: LEARNING
# ══════════════════════════════════════════════════════════════════════════════
def draw_learning(t):
    img = Image.new("RGB",(W,H),t["bg"])
    draw = ImageDraw.Draw(img, "RGBA")

    # ── TOP BAR ───────────────────────────────────────────────────────────────
    draw.rectangle([0,0,W,60],fill=t["nav"])
    txt(draw,"← 뒤로",24,30,fnt(14),t["nav_txt"],anchor="lm")
    txt(draw,"3학년 수학 - 곱셈",W//2,30,fnt(17,True),t["nav_txt"],anchor="mm")
    # progress bar
    rr(draw,800,22,1200,38,8,(255,255,255,80))
    rr(draw,800,22,1000,38,8,(255,255,255))
    txt(draw,"진행률 50%",1250,30,fnt(13),t["nav_txt"],anchor="lm")
    txt(draw,"⏱ 24:35",1380,30,fnt(13),t["nav_txt"],anchor="lm")

    # ── MAIN CONTENT (left 1020px) ─────────────────────────────────────────
    SIDEBAR_X = 1040

    # avatar area
    rr(draw,20,70,SIDEBAR_X-20,530,24,
       (30,40,80) if not t["dark"] else (15,25,60))

    # "LIVE" badge
    rr(draw,40,82,130,108,14,(220,50,50))
    txt(draw,"● LIVE",85,95,fnt(13,True),(255,255,255),anchor="mm")
    txt(draw,"AI 선생님",190,95,fnt(14,True),t["nav_txt"] if t["dark"] else (220,230,255))

    # avatar figure
    avatar(draw,530,310,240,t["primary"])

    # speech bubble
    rr(draw,610,140,960,230,20,(255,255,255,230))
    draw.polygon([(610,185),(590,205),(630,205)],fill=(255,255,255,230))
    txt(draw,"자, 3×4는 무엇일까요?",785,175,fnt(16,True),t["txt"],anchor="mm")
    txt(draw,"잘 생각해 보세요! 😊",785,205,fnt(14),(100,100,100),anchor="mm")

    # whiteboard area
    rr(draw,40,380,520,510,15,(255,255,255))
    txt(draw,"3 × 4 = ?",280,445,fnt(32,True),(50,50,50),anchor="mm")
    txt(draw,"칠판",280,495,fnt(12),(160,160,160),anchor="mm")

    # ── CONTROLS ──────────────────────────────────────────────────────────────
    ctrl_y = 545
    draw.rectangle([20,ctrl_y,SIDEBAR_X-20,ctrl_y+65],fill=t["card"] if not t["dark"] else (25,45,100))

    # mic btn
    draw.ellipse([40,ctrl_y+8,90,ctrl_y+58],fill=t["primary"])
    txt(draw,"🎤",65,ctrl_y+33,fnt(18),(255,255,255),anchor="mm")
    # camera btn
    draw.ellipse([105,ctrl_y+8,155,ctrl_y+58],fill=t["sec"])
    txt(draw,"📷",130,ctrl_y+33,fnt(18),(255,255,255),anchor="mm")
    # question btn
    btn(draw,175,ctrl_y+13,350,ctrl_y+53,"질문하기",
        fnt(15,True),t["acc"],(255,255,255),r=20)
    # volume slider
    rr(draw,380,ctrl_y+26,600,ctrl_y+40,7,(200,200,200))
    rr(draw,380,ctrl_y+26,510,ctrl_y+40,7,t["primary"])
    draw.ellipse([500,ctrl_y+18,524,ctrl_y+48],fill=t["primary"])
    txt(draw,"🔊 음량",640,ctrl_y+33,fnt(13),t["txt"],anchor="lm")

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    sx = SIDEBAR_X+10
    sw = W-sx-15

    # attention indicator
    rr(draw,sx,70,sx+sw,170,18,t["card"] if not t["dark"] else (25,45,110))
    txt(draw,"집중도",sx+15,90,fnt(14,True),t["txt"])
    rr(draw,sx+15,110,sx+sw-15,140,8,(220,220,220))
    filled_w = int((sw-30)*0.85)
    rr(draw,sx+15,110,sx+15+filled_w,140,8,(80,200,80))
    txt(draw,"85%",sx+sw//2,125,fnt(13,True),(255,255,255),anchor="mm")
    txt(draw,"😊 집중하고 있어요!",sx+15,158,fnt(12),(80,180,80))

    # quiz card
    rr(draw,sx,185,sx+sw,420,18,t["card"] if not t["dark"] else (25,45,110))
    txt(draw,"퀴즈",sx+15,205,fnt(14,True),t["primary"])
    rr(draw,sx+10,220,sx+sw-10,255,10,(240,240,255) if not t["dark"] else (40,55,130))
    txt(draw,"다음 중 3×4의 답은?",sx+sw//2,237,fnt(13,True),t["txt"],anchor="mm")

    opts=[("A","10"),("B","12"),("C","14"),("D","16")]
    for i,(lbl,val) in enumerate(opts):
        oy = 268+i*35
        ox = sx+15 if i%2==0 else sx+sw//2+5
        ow2 = sw//2-25
        bc = t["acc"] if lbl=="B" else ((230,230,240) if not t["dark"] else (40,55,130))
        fc = (255,255,255) if lbl=="B" else t["txt"]
        rr(draw,ox,oy,ox+ow2,oy+28,10,bc)
        txt(draw,f"{lbl}. {val}",ox+ow2//2,oy+14,fnt(13),fc,anchor="mm")

    # chat
    rr(draw,sx,430,sx+sw,H-15,18,t["card"] if not t["dark"] else (25,45,110))
    txt(draw,"채팅 / 질문",sx+15,448,fnt(14,True),t["txt"])

    msgs=[
        ("학생","12라고 생각해요!",(230,245,255) if not t["dark"] else (40,60,130)),
        ("AI","정답이에요! 🎉",(230,255,230) if not t["dark"] else (30,80,60)),
        ("학생","감사합니다!",(230,245,255) if not t["dark"] else (40,60,130)),
    ]
    for i,(who,msg,mc) in enumerate(msgs):
        my = 470+i*60
        rr(draw,sx+10,my,sx+sw-10,my+48,12,mc)
        txt(draw,who,sx+20,my+10,fnt(11,True),t["primary"])
        txt(draw,msg,sx+20,my+28,fnt(13),t["txt"])

    # chat input
    rr(draw,sx+10,H-55,sx+sw-55,H-20,12,(245,245,250) if not t["dark"] else (40,55,130))
    txt(draw,"메시지를 입력하세요...",sx+22,H-37,fnt(13),(180,180,180),anchor="lm")
    btn(draw,sx+sw-50,H-55,sx+sw-5,H-20,"전송",fnt(12,True),t["primary"],(255,255,255),r=10)

    return img

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: BOARD
# ══════════════════════════════════════════════════════════════════════════════
def draw_board(t):
    img = Image.new("RGB",(W,H),t["bg"])
    draw = ImageDraw.Draw(img, "RGBA")
    NAV_H = 68

    # ── BOARD HEADER ──────────────────────────────────────────────────────────
    bh_y = NAV_H+10
    txt(draw,"학습 게시판",60,bh_y+28,fnt(28,True),t["txt"])
    txt(draw,"수업 관련 공지, 질문, 자료를 공유하세요",60,bh_y+65,fnt(14),(150,150,170))

    # search bar
    rr(draw,700,bh_y+20,1160,bh_y+60,22,(255,255,255) if not t["dark"] else (25,45,110))
    if not t["dark"]:
        draw.rounded_rectangle([700,bh_y+20,1160,bh_y+60],radius=22,
                                outline=(200,200,200),width=2)
    txt(draw,"🔍  검색어를 입력하세요...",740,bh_y+40,fnt(14),(180,180,190),anchor="lm")
    btn(draw,1180,bh_y+20,1290,bh_y+60,"검색",fnt(15,True),t["primary"],(255,255,255),r=22)
    btn(draw,1310,bh_y+20,1420,bh_y+60,"글쓰기",fnt(15,True),t["acc"],(255,255,255),r=22)

    # ── CATEGORY TABS ─────────────────────────────────────────────────────────
    tabs=["공지사항","질문/답변","학습자료","수업후기"]
    tab_w=180; tab_y=NAV_H+110
    draw.rectangle([0,tab_y,W,tab_y+48],
                   fill=(245,245,248) if not t["dark"] else (20,35,90))
    for i,tab in enumerate(tabs):
        tx=60+i*(tab_w+20)
        if i==1:  # active
            draw.rectangle([tx-10,tab_y,tx+tab_w+10,tab_y+48],fill=t["card"])
            draw.rectangle([tx-10,tab_y+44,tx+tab_w+10,tab_y+48],fill=t["primary"])
            txt(draw,tab,tx+tab_w//2,tab_y+24,fnt(15,True),t["primary"],anchor="mm")
        else:
            txt(draw,tab,tx+tab_w//2,tab_y+24,fnt(14),(160,160,175),anchor="mm")

    # ── POST LIST ─────────────────────────────────────────────────────────────
    list_y = tab_y+58

    # header row
    draw.rectangle([0,list_y,W,list_y+38],fill=t["primary"])
    headers=[("분류",90),("제목",480),("작성자",820),("날짜",980),("조회",1120)]
    for label,lx in headers:
        txt(draw,label,lx,list_y+19,fnt(13,True),t["nav_txt"],anchor="mm")
    list_y+=38

    categories=[
        ("공지","[공지] 이번 주 수업 일정 안내드립니다","관리자","2025.04.01",342,(255,82,82),(255,240,240)),
        ("질문","3학년 수학 나눗셈 개념이 잘 이해가 안돼요","김민준","2025.04.01",128,(0,180,216),(240,250,255)),
        ("자료","곱셈구구단 학습 자료 공유합니다 (PDF)","이선생","2025.03.31",521,(80,200,80),(240,255,240)),
        ("후기","오늘 수업 너무 재밌었어요! AI 선생님 최고","박지수","2025.03.31",89,(171,71,188),(248,240,255)),
        ("질문","집중도 체크 기능은 어떻게 작동하나요?","최현우","2025.03.30",204,(255,171,64),(255,248,235)),
        ("자료","영어 단어 암기 도움 자료 올립니다","정서연","2025.03.30",317,(0,191,165),(235,255,250)),
        ("후기","아이가 공부에 흥미를 갖게 되었어요","학부모A","2025.03.29",156,(240,98,146),(255,240,248)),
        ("공지","4월 수업 스케줄 변경 안내","관리자","2025.03.29",445,(255,82,82),(255,240,240)),
    ]

    for i,(cat,title,author,date,views,badge_c,row_bg) in enumerate(categories):
        ry = list_y+i*58
        # alternate rows
        if t["dark"]:
            rc = (20,35,90) if i%2==0 else (25,45,110)
        else:
            rc = (255,255,255) if i%2==0 else (248,249,252)
        draw.rectangle([0,ry,W,ry+58],fill=rc)
        draw.line([(0,ry+57),(W,ry+57)],fill=(220,220,230) if not t["dark"] else (40,55,130))

        # category badge
        bx=40
        rr(draw,bx,ry+16,bx+56,ry+42,12,badge_c)
        txt(draw,cat,bx+28,ry+29,fnt(11,True),(255,255,255),anchor="mm")

        # title
        txt(draw,title,180,ry+29,fnt(14),t["txt"],anchor="lm")
        # author
        txt(draw,author,820,ry+29,fnt(13),(130,130,150),anchor="mm")
        # date
        txt(draw,date,980,ry+29,fnt(13),(150,150,170),anchor="mm")
        # views
        txt(draw,str(views),1120,ry+29,fnt(13),(130,130,150),anchor="mm")

    # ── PAGINATION ────────────────────────────────────────────────────────────
    pg_y = H-52
    pages=["‹","1","2","3","4","5","›"]
    for i,p in enumerate(pages):
        px = W//2-180+i*60
        if p=="2":
            draw.ellipse([px-20,pg_y-18,px+20,pg_y+18],fill=t["primary"])
            txt(draw,p,px,pg_y,fnt(14,True),(255,255,255),anchor="mm")
        else:
            draw.ellipse([px-20,pg_y-18,px+20,pg_y+18],
                         fill=(240,240,245) if not t["dark"] else (30,50,120))
            txt(draw,p,px,pg_y,fnt(14),t["txt"],anchor="mm")

    nav_bar(draw,img,t)
    return img

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE ALL
# ══════════════════════════════════════════════════════════════════════════════
NEW_IDS = {"theme6_lemon","theme7_mint","theme8_peach"}
for t in [x for x in THEMES if x["id"] in NEW_IDS]:
    for page_fn, page_name in [(draw_main,"main"),(draw_learning,"learning"),(draw_board,"board")]:
        img = page_fn(t)
        path = f"{OUT}/{t['id']}_{page_name}.png"
        img.save(path, "PNG")
        print(f"Saved: {path}")

print("Done! All 15 PNG files generated.")
