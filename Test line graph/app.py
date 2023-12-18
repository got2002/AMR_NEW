from flask import Flask, render_template
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    # ข้อมูลสำหรับกราฟเส้นที่แยกกัน
    x_data = np.array(range(1, 32))

    y_data_1 = np.random.randint(1, 10, size=(31,))
    y_data_2 = np.random.randint(1, 10, size=(31,))
    y_data_3 = np.random.randint(1, 10, size=(31,))

    # สร้างกราฟเส้นที่ 1
    plt.plot(x_data, y_data_1, marker='o', linestyle='-', color='blue', label='Graph 1')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 1')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_1 = BytesIO()
    plt.savefig(img_1, format='png')
    img_1.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_1 = base64.b64encode(img_1.getvalue()).decode('utf8')

    # สร้างกราฟเส้นที่ 2
    plt.plot(x_data, y_data_2, marker='s', linestyle='--', color='green', label='Graph 2')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 2')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_2 = BytesIO()
    plt.savefig(img_2, format='png')
    img_2.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_2 = base64.b64encode(img_2.getvalue()).decode('utf8')

    # สร้างกราฟเส้นที่ 3
    plt.plot(x_data, y_data_3, marker='^', linestyle='-.', color='red', label='Graph 3')

    # กำหนดชื่อแกน x และ y
    plt.xlabel('Days')
    plt.ylabel('Values')

    # กำหนดชื่อกราฟ
    plt.title('Graph 3')

    # เพิ่มตำแหน่งของ legend
    plt.legend(loc='upper left')

    # แปลงกราฟเป็นรูปภาพและเก็บไว้ใน BytesIO
    img_3 = BytesIO()
    plt.savefig(img_3, format='png')
    img_3.seek(0)
    plt.close()

    # แปลงรูปภาพเป็น base64
    graph_url_3 = base64.b64encode(img_3.getvalue()).decode('utf8')

    return render_template('index.html', graph_url_1=graph_url_1, graph_url_2=graph_url_2, graph_url_3=graph_url_3)

if __name__ == '__main__':
    app.run(debug=True)
