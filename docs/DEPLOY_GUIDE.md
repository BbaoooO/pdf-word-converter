# 🚀 Hướng dẫn Deploy lên Render.com

## Bước 1: Tạo GitHub Repository

1. **Truy cập GitHub.com và tạo repository mới:**
   - Repository name: `pdf-word-converter`
   - Chọn Public (để deploy miễn phí)
   - Không cần README (vì đã có sẵn)

2. **Đẩy code lên GitHub:**
```bash
# Thêm remote origin (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/pdf-word-converter.git

# Đẩy code lên GitHub
git branch -M main
git push -u origin main
```

## Bước 2: Deploy trên Render.com

1. **Truy cập [Render.com](https://render.com) và đăng ký/đăng nhập**

2. **Tạo Web Service mới:**
   - Nhấn **"New"** → **"Web Service"**
   - Chọn **"Connect a repository"**
   - Chọn repository `pdf-word-converter` vừa tạo

3. **Cấu hình Deploy:**
   ```
   Name: pdf-word-converter
   Environment: Python 3
   Region: Oregon (US West) - gần nhất với châu Á
   Branch: main
   Root Directory: (để trống)
   Runtime: Python 3.9.18
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Environment Variables (không cần thiết cho app này)**

5. **Nhấn "Create Web Service"**

## Bước 3: Chờ Deploy hoàn tất

- Render sẽ tự động build và deploy
- Quá trình mất khoảng 5-10 phút
- Bạn sẽ nhận được URL dạng: `https://pdf-word-converter.onrender.com`

## ✅ **Tính năng Free Plan Render:**

- ✅ **Hoàn toàn miễn phí**
- ✅ **512MB RAM** (đủ cho app này)
- ✅ **HTTPS tự động**
- ✅ **Custom domain** (nếu muốn)
- ✅ **Auto-deploy** khi push code mới
- ⚠️ **Sleep after 15 minutes** không hoạt động (cần 30s để wake up)

## 🔄 **Cập nhật app:**

Mỗi khi bạn muốn cập nhật:
```bash
git add .
git commit -m "Update features"
git push origin main
```
→ Render sẽ tự động deploy lại!

## 🌐 **URL cuối cùng:**

Sau khi deploy xong, bạn sẽ có URL công khai dạng:
```
https://pdf-word-converter-xyz.onrender.com
```

## 🎯 **Lưu ý quan trọng:**

1. **Free plan có giới hạn:**
   - App sẽ "ngủ" sau 15 phút không hoạt động
   - Lần truy cập đầu tiên sẽ mất 30s để "thức dậy"

2. **File upload:**
   - Render hỗ trợ file upload tạm thời
   - Files sẽ bị xóa khi app restart

3. **Để giữ app "thức":** 
   - Có thể dùng service như UptimeRobot để ping định kỳ
   - Hoặc upgrade lên Paid plan ($7/tháng)

## 🚀 **Sau khi deploy thành công:**

Bạn có thể chia sẻ link cho bạn bè sử dụng:
"Chuyển đổi PDF ↔ Word miễn phí tại: https://your-app.onrender.com"

---

**Happy deploying! 🎉**
