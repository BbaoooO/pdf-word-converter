from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import threading
import time
from docx import Document
import subprocess
from io import BytesIO

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

def convert_docx_to_pdf_linux(input_path, output_path):
    """Chuyển đổi DOCX sang PDF trên Linux sử dụng LibreOffice"""
    try:
        # Thử sử dụng LibreOffice (có sẵn trên hầu hết Linux servers)
        cmd = [
            'libreoffice', 
            '--headless', 
            '--convert-to', 'pdf', 
            '--outdir', os.path.dirname(output_path),
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            # LibreOffice tạo file với tên khác, cần đổi tên
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            temp_pdf = os.path.join(os.path.dirname(output_path), f"{base_name}.pdf")
            
            if os.path.exists(temp_pdf):
                if temp_pdf != output_path:
                    os.rename(temp_pdf, output_path)
                return True
        
        # Nếu LibreOffice không hoạt động, thử pandoc
        cmd = ['pandoc', input_path, '-o', output_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0 and os.path.exists(output_path):
            return True
            
        # Nếu cả hai đều không hoạt động, sử dụng python-docx + weasyprint
        return convert_docx_to_pdf_python(input_path, output_path)
        
    except Exception as e:
        print(f"Lỗi convert_docx_to_pdf_linux: {e}")
        return convert_docx_to_pdf_python(input_path, output_path)

def convert_docx_to_pdf_python(input_path, output_path):
    """Chuyển đổi DOCX sang PDF sử dụng python-docx + weasyprint"""
    try:
        from docx import Document
        import weasyprint
        
        # Đọc DOCX
        doc = Document(input_path)
        
        # Chuyển đổi thành HTML
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                p { margin-bottom: 10px; }
                h1, h2, h3, h4, h5, h6 { margin: 20px 0 10px 0; }
            </style>
        </head>
        <body>
        """
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                html_content += f"<p>{paragraph.text}</p>\n"
        
        html_content += "</body></html>"
        
        # Chuyển HTML thành PDF
        weasyprint.HTML(string=html_content).write_pdf(output_path)
        
        return os.path.exists(output_path)
        
    except Exception as e:
        print(f"Lỗi convert_docx_to_pdf_python: {e}")
        return False

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
            success = convert_docx_to_pdf_linux(input_path, output_path)
            if not success:
                flash('Lỗi khi chuyển đổi DOCX sang PDF. Vui lòng thử lại!', 'error')
                os.remove(input_path)
                return redirect(url_for('index'))
        
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
