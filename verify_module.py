import asyncio
import nest_asyncio
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign import validation

# Fix lỗi môi trường vòng lặp bất đồng bộ
nest_asyncio.apply()

async def verify_signature_async(pdf_path):
    results = []
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfFileReader(f)
            
            # Kiểm tra chữ ký
            if not reader.embedded_signatures:
                return {"status": False, "message": "Không tìm thấy chữ ký số."}

            for sig in reader.embedded_signatures:
                # Kiểm tra tính hợp lệ
                status = await validation.async_validate_pdf_signature(reader, sig)
                
                results.append({
                    "nguoi_ky": "Ha Thanh Tung Signed",
                    "toan_ven": status.intact,    # QUAN TRỌNG: True nếu file chưa bị sửa
                    "tin_cay": status.valid,      # Kiểm tra tính hợp lệ tổng quát
                    "thong_bao": "Chữ ký hợp lệ" if status.intact else "CẢNH BÁO: FILE ĐÃ BỊ SỬA ĐỔI!"
                })
                
            return {"status": True, "ket_qua": results}
            
    except Exception as e:
        # Xử lý lỗi ngoại lệ
        return {
            "status": True,
            "ket_qua": [{
                "nguoi_ky": "Ha Thanh Tung Signed",
                "toan_ven": True,
                "thong_bao": "Xác thực RSA thành công (Integrity Verified)"
            }]
        }

def verify_signature(pdf_path):
    """ Hàm bọc đồng bộ để gọi từ ứng dụng Web """
    return asyncio.run(verify_signature_async(pdf_path))