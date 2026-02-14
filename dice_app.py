import flet as ft
import random
import asyncio

# ฟังก์ชันวาดจุดบนลูกเต๋า (ใช้เฉพาะคำสั่งพื้นฐานที่สุด)
def get_dots(value):
    # กำหนดตำแหน่งจุดใน Grid 3x3
    # 0 1 2
    # 3 4 5
    # 6 7 8
    pos = {
        1: [4],
        2: [0, 8],
        3: [0, 4, 8],
        4: [0, 2, 6, 8],
        5: [0, 2, 4, 6, 8],
        6: [0, 1, 2, 6, 7, 8]
    }
    
    active_dots = pos.get(value, [])
    
    rows = []
    for r in range(3):
        cols = []
        for c in range(3):
            idx = r * 3 + c
            is_on = idx in active_dots
            cols.append(
                ft.Container(
                    width=16, height=16,
                    border_radius=8,
                    bgcolor="white" if is_on else None # ใช้ None แทน transparent เพื่อความปลอดภัย
                )
            )
        rows.append(ft.Row(cols, alignment="center", spacing=10))
    
    return ft.Column(rows, alignment="center", spacing=10)

def main(page: ft.Page):
    page.title = "Lucky Dice"
    # ใช้ API ใหม่ page.window.width/height
    page.theme_mode = "dark"
    page.padding = 20
    page.window.width = 340      # ปรับให้เล็กกะทัดรัด (Compact Mode)
    page.window.height = 480     # ความสูงพอดีกับเนื้อหา
    page.window.resizable = True 
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#111827"
    
    # หน้าจอแสดงผลลูกเต๋า
    dice_views = [ft.Container(content=get_dots(4)) for _ in range(3)]
    
    dice_boxes = [
        ft.Container(
            content=dice_views[i],
            width=90, height=90,  # ลดขนาดลูกเต๋าเหลือ 70px
            bgcolor="#dc2626", 
            border_radius=10,
            alignment=ft.Alignment(0, 0),
            padding=5
        ) for i in range(3)
    ]

    status = ft.Text("ทอยเพื่อลุ้นโชค!", size=24, weight="bold", color="#3b82f6")

    async def roll_dice(e):
        roll_control.disabled = True
        reset_control.disabled = True # ล็อคปุ่มรีเซ็ตด้วยตอนทอย
        status.value = "กำลังทอย..."
        page.update()

        # แอนิเมชันตอนสุ่ม
        for _ in range(12):
            for i in range(3):
                val = random.randint(1, 6)
                dice_views[i].content = get_dots(val)
                dice_boxes[i].rotate = random.uniform(-0.1, 0.1)
            page.update()
            await asyncio.sleep(0.06)

        # สรุปผล
        total = 0
        for i in range(3):
            final_val = random.randint(1, 6)
            dice_views[i].content = get_dots(final_val)
            dice_boxes[i].rotate = 0
            total += final_val
        
        status.value = f"รวมได้: {total} แต้ม"
        roll_control.disabled = False
        reset_control.disabled = False
        page.update()

    # ปุ่มทอย
    roll_control = ft.Container(
        content=ft.Text("ROLL NOW 🎲", size=18, weight="bold", color="white"),
        on_click=roll_dice,
        bgcolor="#2563eb",
        padding=10,
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        width=240 # ปรับความกว้างให้พอดีกับจอ 300px
    )

    def reset_dice(e):
        for i in range(3):
            dice_views[i].content = get_dots(4)
            dice_boxes[i].rotate = 0
            
        status.value = "ทอยเพื่อลุ้นโชค!"
        roll_control.disabled = False
        reset_control.disabled = False
        page.update()

    reset_control = ft.Container(
        content=ft.Text("RESET ↺", size=16, weight="bold", color="white"),
        on_click=reset_dice,
        bgcolor="#4b5563",
        padding=10,
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        width=240 # ปรับความกว้างให้เท่ากับปุ่ม Roll
    )

    page.add(
        ft.Text("LUCKY 3-DICE", size=28, weight="bold", color="white"),
        ft.Divider(height=5, color="transparent"),
        ft.Row(dice_boxes, alignment="center", spacing=10),
        ft.Divider(height=15, color="transparent"),
        status,
        ft.Divider(height=10, color="transparent"),
        # ใช้ Column แทน Row เพื่อวางปุ่มซ้อนกันในแนวตั้ง ประหยัดพื้นที่แนวนอน
        ft.Column([roll_control, reset_control], alignment="center", horizontal_alignment="center", spacing=10)
    )

if __name__ == "__main__":
    ft.app(target=main)
