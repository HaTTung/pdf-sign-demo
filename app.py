import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

# Gọi các hàm từ file của nhóm bạn
import sign_module
import verify_module

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign', methods=['POST'])
def sign():
    try:
        pdf_file = request.files['pdf']
        if not pdf_file or pdf_file.filename == '':
            return "Lỗi: Chưa chọn file", 400

        # Lưu file gốc
        filename = secure_filename(pdf_file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(input_path)

        # Định nghĩa đường dẫn file đầu ra
        output_filename = filename.replace('.pdf', '_signed.pdf')
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

        # Gọi hàm ký số (Hàm của bạn Truong2005 chỉ cần 2 tham số này)
        sign_module.sign_pdf(input_path, output_path)

        # Trả file đã ký về cho người dùng tải xuống
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"<h1>Có lỗi khi ký:</h1><p>{str(e)}</p>"

@app.route('/verify', methods=['POST'])
def verify():
    try:
        pdf_file = request.files['pdf']
        if not pdf_file or pdf_file.filename == '':
            return "Lỗi: Chưa chọn file", 400

        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(pdf_path)

        # Gọi hàm xác thực từ verify_module
        result_dict = verify_module.verify_signature(pdf_path)

        # Đẩy kết quả (Dict) sang cho file HTML xử lý hiển thị
        return render_template('index.html', verify_result=result_dict)
    except Exception as e:
        return f"<h1>Có lỗi khi xác thực:</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)