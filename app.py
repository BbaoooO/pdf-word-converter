from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
from pdf2docx import Converter
from docx2pdf import convert
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Tạo thư mục uploads nếu chưa tồn tại
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_file_after_delay(filepath, delay=300):  # Xóa file sau 5 phút
    """Xóa file sau một khoảng thời gian để tiết kiệm bộ nhớ"""
    def delete_file():
        time.sleep(delay)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Đã xóa file: {filepath}")
        except Exception as e:
            print(f"Lỗi khi xóa file {filepath}: {e}")
    
    thread = threading.Thread(target=delete_file)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        if 'file' not in request.files:
            flash('Vui lòng chọn file để upload!', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        conversion_type = request.form.get('conversion_type')
        
        if file.filename == '':
            flash('Vui lòng chọn file để upload!', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Định dạng file không được hỗ trợ! Chỉ chấp nhận PDF, DOCX, DOC.', 'error')
            return redirect(url_for('index'))
        
        # Lưu file upload
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)
        
        # Tạo tên file output
        name, ext = os.path.splitext(filename)
        
        if conversion_type == 'pdf_to_docx':
            if ext.lower() != '.pdf':
                flash('Vui lòng chọn file PDF để chuyển đổi sang DOCX!', 'error')
                os.remove(input_path)
                return redirect(url_for('index'))
            
            output_filename = f"{name}_converted.docx"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            
            # Chuyển đổi PDF sang DOCX
            cv = Converter(input_path)
            cv.convert(output_path)
            cv.close()
            
        elif conversion_type == 'docx_to_pdf':
            if ext.lower() not in ['.docx', '.doc']:
                flash('Vui lòng chọn file DOCX/DOC để chuyển đổi sang PDF!', 'error')
                os.remove(input_path)
                return redirect(url_for('index'))
            
            output_filename = f"{name}_converted.pdf"
            output_path = os.path.join(UPLOAD_FOLDER, output_filename)
            
            # Chuyển đổi DOCX sang PDF
            convert(input_path, output_path)
        
        else:
            flash('Kiểu chuyển đổi không hợp lệ!', 'error')
            os.remove(input_path)
            return redirect(url_for('index'))
        
        # Xóa file input ngay lập tức
        os.remove(input_path)
        
        # Lên lịch xóa file output sau 5 phút
        delete_file_after_delay(output_path, 300)
        
        flash(f'Chuyển đổi thành công! File: {output_filename}', 'success')
        return render_template('index.html', download_file=output_filename)
        
    except Exception as e:
        flash(f'Lỗi trong quá trình chuyển đổi: {str(e)}', 'error')
        # Dọn dẹp file nếu có lỗi
        if 'input_path' in locals() and os.path.exists(input_path):
            os.remove(input_path)
        if 'output_path' in locals() and os.path.exists(output_path):
            os.remove(output_path)
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('File không tồn tại hoặc đã bị xóa!', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Lỗi khi tải file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File quá lớn! Vui lòng chọn file nhỏ hơn 50MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Lấy port từ environment variable (Render yêu cầu)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
