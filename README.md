# 📄 PDF ↔ Word Converter

Ứng dụng web đơn giản cho phép chuyển đổi file PDF sang Word (.docx) và ngược lại, được xây dựng bằng Python Flask.

## ✨ Tính năng

- 🔄 Chuyển đổi PDF sang DOCX và DOCX sang PDF
- 📱 Giao diện đẹp, responsive, thân thiện với người dùng
- 🚀 Không cần đăng ký hay đăng nhập
- 🔒 Tự động xóa file sau 5 phút để bảo mật
- 📊 Hỗ trợ file lên đến 50MB
- ⚡ Xử lý nhanh chóng và ổn định

## 🛠️ Cài đặt và chạy local

### Yêu cầu hệ thống
- Python 3.7+
- pip

### Hướng dẫn cài đặt

1. **Clone hoặc tải về project:**
```bash
git clone <repository-url>
cd pdf-word-converter
```

2. **Tạo môi trường ảo (khuyến nghị):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Cài đặt các thư viện:**
```bash
pip install -r requirements.txt
```

4. **Chạy ứng dụng:**
```bash
python app.py
```

5. **Mở trình duyệt và truy cập:**
```
http://localhost:5000
```

## 🌐 Deploy lên Render.com

### Cách 1: Deploy từ GitHub

1. **Đẩy code lên GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Truy cập [Render.com](https://render.com) và:**
   - Đăng nhập/Đăng ký tài khoản
   - Chọn "New Web Service"
   - Kết nối với GitHub repo của bạn
   - Cấu hình như sau:

**Cấu hình Render:**
```
Name: pdf-word-converter
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

3. **Deploy và truy cập URL được cung cấp**

### Cách 2: Deploy thủ công

1. **Zip toàn bộ project**
2. **Upload lên Render qua giao diện web**
3. **Sử dụng cấu hình tương tự như trên**

## 🚀 Deploy lên Railway.app

1. **Cài đặt Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Đăng nhập Railway:**
```bash
railway login
```

3. **Deploy project:**
```bash
railway init
railway up
```

4. **Railway sẽ tự động phát hiện và deploy ứng dụng Flask**

## 📁 Cấu trúc project

```
pdf-word-converter/
├── app.py              # Flask application chính
├── requirements.txt    # Danh sách thư viện Python
├── README.md          # Hướng dẫn sử dụng
├── templates/         # Template HTML
│   └── index.html     # Giao diện chính
└── uploads/           # Thư mục lưu file tạm thời
```

## 🔧 Các thư viện sử dụng

- **Flask**: Framework web Python
- **pdf2docx**: Chuyển đổi PDF sang DOCX
- **docx2pdf**: Chuyển đổi DOCX sang PDF
- **Werkzeug**: Xử lý file upload an toàn
- **Gunicorn**: WSGI server cho production

## 🎯 Cách sử dụng

1. **Truy cập website**
2. **Chọn file PDF hoặc DOCX từ máy tính**
3. **Chọn kiểu chuyển đổi:**
   - PDF → Word: Chuyển file PDF sang DOCX
   - Word → PDF: Chuyển file DOCX/DOC sang PDF
4. **Nhấn "Bắt đầu chuyển đổi"**
5. **Tải xuống file kết quả**

## ⚠️ Lưu ý quan trọng

- File được lưu tạm thời và **tự động xóa sau 5 phút**
- Giới hạn kích thước file: **50MB**
- Chỉ hỗ trợ định dạng: **PDF, DOCX, DOC**
- Không lưu trữ file của người dùng

## 🐛 Xử lý lỗi thường gặp

### Lỗi cài đặt `docx2pdf` trên Windows:
```bash
# Cài đặt Microsoft C++ Build Tools
# Hoặc sử dụng conda thay vì pip:
conda install -c conda-forge python-docx2pdf
```

### Lỗi chuyển đổi PDF:
- Đảm bảo file PDF không bị mã hóa
- Kiểm tra file PDF không bị hỏng

### Lỗi chuyển đổi DOCX:
- Đảm bảo có Microsoft Word hoặc LibreOffice được cài đặt
- Trên Linux/macOS: cài đặt `libreoffice`

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📞 Liên hệ

Nếu có bất kỳ câu hỏi nào, vui lòng tạo issue trên GitHub.

---

**Lưu ý**: Đây là một ứng dụng demo. Trong môi trường production, cần thêm các biện pháp bảo mật như giới hạn rate limit, xác thực, v.v.
