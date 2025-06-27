// PDF ↔ Word Converter JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const convertForm = document.getElementById('convertForm');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const fileInput = document.getElementById('file');
    const pdfToDocx = document.querySelector('input[value="pdf_to_docx"]');
    const docxToPdf = document.querySelector('input[value="docx_to_pdf"]');

    // Xử lý form submit với loading
    if (convertForm) {
        convertForm.addEventListener('submit', function(e) {
            if (submitBtn && loading) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Đang xử lý...';
                loading.style.display = 'block';
            }
        });
    }

    // Cập nhật tên file khi chọn
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name;
            if (fileName) {
                console.log('Đã chọn file:', fileName);
                
                // Tự động chọn loại chuyển đổi dựa trên file
                const ext = fileName.split('.').pop().toLowerCase();
                
                if (ext === 'pdf' && pdfToDocx) {
                    pdfToDocx.checked = true;
                } else if ((ext === 'docx' || ext === 'doc') && docxToPdf) {
                    docxToPdf.checked = true;
                }
            }
        });
    }
});
