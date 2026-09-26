"""Pillow로 제출용 아키텍처 PNG를 생성한다. Windows의 맑은 고딕 사용."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
canvas = Image.new('RGB', (1500, 1060), '#f3f6fa')
draw = ImageDraw.Draw(canvas)
FONT = 'C:/Windows/Fonts/malgun.ttf'
BOLD = 'C:/Windows/Fonts/malgunbd.ttf'


def label(x, y, text, size=22, color='#20334b', bold=False):
    draw.multiline_text((x, y), text, font=ImageFont.truetype(BOLD if bold else FONT, size),
                        fill=color, spacing=11)


def box(rect, fill='#ffffff', outline='#b4c3d6', width=2):
    draw.rounded_rectangle(rect, radius=18, fill=fill, outline=outline, width=width)


def arrow(start, end):
    draw.line([start, end], fill='#178579', width=5)
    x, y = end
    if start[1] == y:
        draw.polygon([(x, y), (x-14, y-9), (x-14, y+9)], fill='#178579')
    else:
        draw.polygon([(x, y), (x-9, y-14), (x+9, y-14)], fill='#178579')


label(70, 32, 'B6-1  |  기존 OCI 인스턴스로 웹 서비스 공개', 37, bold=True)
label(72, 88, 'ai-research · ap-chuncheon-1 · 기존 리소스 보존 / 실습 서비스만 추가', 21, '#5f7087')
box((70, 145, 555, 270))
label(95, 163, '외부 사용자 / 인터넷', 25, bold=True)
label(95, 209, 'HTTP :80   /   HTTPS :443 (공개 인증서)', 21)
arrow((555, 208), (650, 208))
box((650, 145, 1430, 270), '#e6f5f1', '#59a798')
label(680, 163, '기존 Internet Gateway · 공인 IP 152.67.213.106', 25, bold=True)
label(680, 209, '라우트: 0.0.0.0/0 → IGW  |  API 조회·외부 HTTP 검증', 21)
box((70, 320, 1430, 930), '#e8eef7', '#8da4c2')
label(100, 341, 'VCN: vcn-ai-research · 10.10.0.0/16  (AWS VPC 대응)', 26, bold=True)
box((100, 395, 1400, 900), '#f8fafd', '#a6b9d0')
label(125, 411, '기존 Subnet · 10.10.1.0/24', 23, bold=True)
draw.line([(1050, 270), (1050, 447), (305, 447)], fill='#178579', width=5)
arrow((305, 447), (305, 475))
box((130, 475, 480, 760), '#fff8e6', '#d6b667')
label(154, 498, 'OCI 네트워크 보안', 25, bold=True)
label(154, 548, 'NSG b6-1-web\nTCP 80·443 공개\nSL: SSH 개인 IP /32', 23)
label(154, 693, 'API 적용·외부 검증 완료', 20, '#8c6517')
arrow((480, 610), (535, 610))
box((535, 467, 1370, 865), '#ffffff', '#6685aa', 3)
label(560, 483, 'Compute: ai-research  |  10.10.1.250  |  Ubuntu · ARM64', 24, bold=True)
box((560, 543, 850, 700), '#f0f4fa')
label(581, 561, '호스트 UFW', 25, bold=True)
label(581, 607, 'TCP 80 / 443 허용\n기존 SSH 규칙 유지', 22)
arrow((850, 619), (896, 619))
box((897, 543, 1340, 700), '#e6f5f1', '#59a798')
label(917, 558, 'b6-1-cloud-lab', 25, bold=True)
label(917, 602, 'Docker host network · Caddy\n정적 페이지 / GET /health → OK', 21)
box((560, 725, 1340, 835), '#f2f4f7')
label(580, 741, '기존 서비스 보존', 23, bold=True)
label(580, 782, 'mirofish · execution-tools · Docker · NetBird', 22)
label(76, 953, '실측 완료: VCN·서브넷·IGW·NSG·SSH 제한·IAM·DNS·HTTP/HTTPS 200', 21, '#216f63')
label(76, 994, '유지: VM·볼륨·기존 서비스 / www.codyssey-domain-test.kro.kr / 원복은 명시적 요청 후', 20, '#806321')
canvas.save(ROOT / 'docs/architecture.png')
print(ROOT / 'docs/architecture.png')
