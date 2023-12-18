from flask import Flask, render_template
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    # ข้อมูลสำหรับแกน x และ y
    x_data = np.array([1, 2, 3, 4, 5])
    y_data = np.array([2, 4, 6, 8, 10])

    # สร้าง Line Graph
    plt.plot(x_data, y_data, marker='o', linestyle='-', color='b', label='Line 1')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('X Axis Label')
    plt.ylabel('Y Axis Label')

    # กำหนดชื่อกราฟ
    plt.title('Line Graph Example')

    # เพิ่มแต่ละจุดบนกราฟ
    for x, y in zip(x_data, y_data):
        plt.text(x, y, f'({x}, {y})')

    # เพิ่มกริด
    plt.grid(True)

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('index.html', graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
