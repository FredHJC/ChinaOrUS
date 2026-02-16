"""PDF 导出模块：生成结果报告"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet

# 尝试注册中文字体，如果没有则使用 Helvetica
FONT_NAME = "Helvetica"
try:
    import platform
    if platform.system() == "Darwin":
        pdfmetrics.registerFont(TTFont("PingFang", "/System/Library/Fonts/PingFang.ttc", subfontIndex=0))
        FONT_NAME = "PingFang"
    elif platform.system() == "Linux":
        import os
        for path in ["/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
                      "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc"]:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont("WQY", path))
                FONT_NAME = "WQY"
                break
except Exception:
    pass


def generate_pdf(session_data: dict) -> bytes:
    """
    生成 PDF 报告。

    session_data 包含:
        session_id, us_total_score, cn_total_score,
        quadrant, quadrant_label, diagnosis, created_at
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    # 标题
    c.setFont(FONT_NAME, 22)
    c.drawCentredString(width / 2, height - 40 * mm, "留学生去留决策量表 - 测试报告")

    # 分割线
    c.setStrokeColor(HexColor("#3366cc"))
    c.setLineWidth(1)
    c.line(30 * mm, height - 48 * mm, width - 30 * mm, height - 48 * mm)

    # 基础信息
    y = height - 65 * mm
    c.setFont(FONT_NAME, 12)
    c.drawString(30 * mm, y, f"测试编号: {session_data['session_id'][:8]}...")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"测试时间: {session_data['created_at']}")

    # 结果
    y -= 16 * mm
    c.setFont(FONT_NAME, 16)
    c.setFillColor(HexColor("#3366cc"))
    c.drawString(30 * mm, y, f"诊断结果: {session_data['quadrant_label']}")

    y -= 12 * mm
    c.setFillColor(HexColor("#333333"))
    c.setFont(FONT_NAME, 14)
    c.drawString(30 * mm, y, f"美国吸引力指数: {session_data['us_total_score']}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"中国吸引力指数: {session_data['cn_total_score']}")

    # 四象限示意
    y -= 16 * mm
    cx = width / 2
    cy = y - 50 * mm
    box_size = 60 * mm

    # 画十字线
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(0.5)
    c.line(cx - box_size, cy, cx + box_size, cy)
    c.line(cx, cy - box_size, cx, cy + box_size)

    # 标注轴
    c.setFont(FONT_NAME, 9)
    c.setFillColor(HexColor("#666666"))
    c.drawString(cx + box_size + 2 * mm, cy - 2 * mm, "CN")
    c.drawCentredString(cx, cy + box_size + 4 * mm, "US")

    # 画用户点
    us = session_data["us_total_score"]
    cn = session_data["cn_total_score"]
    from scoring import THRESHOLD
    threshold = THRESHOLD
    # 将分数映射到坐标
    px = cx + (cn - threshold) / (225 - 5) * 2 * box_size
    py = cy + (us - threshold) / (225 - 5) * 2 * box_size
    c.setFillColor(HexColor("#ff4444"))
    c.circle(px, py, 4 * mm, fill=1, stroke=0)

    # 诊断话术
    y = cy - box_size - 20 * mm
    c.setFillColor(HexColor("#333333"))
    c.setFont(FONT_NAME, 11)

    # 自动换行
    diagnosis = session_data["diagnosis"]
    max_width = width - 60 * mm
    words = list(diagnosis)
    line = ""
    for char in words:
        test_line = line + char
        if c.stringWidth(test_line, FONT_NAME, 11) > max_width:
            c.drawString(30 * mm, y, line)
            y -= 6 * mm
            line = char
        else:
            line = test_line
    if line:
        c.drawString(30 * mm, y, line)

    c.save()
    buf.seek(0)
    return buf.read()
