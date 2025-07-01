Cách chạy chương trình:
1. Cài đặt Python 3.8+ và Pygame: `pip install -r requirements.txt`
2. Chạy `main.py`: `python main.py`
3. Giao diện Pygame:
   - Nhấn các nút BFS/DFS/UCS/A* để chọn thuật toán.
   - Nhấn Play/Pause để xem giải pháp từng bước.
   - Nhấn Reset để quay lại trạng thái ban đầu.
   - Thống kê hiển thị: số bước, chi phí, số node mở rộng, thời gian.
4. File map nằm trong thư mục Map, định dạng mỗi file:
   - Dòng 1: Số lượng xe
   - Mỗi dòng tiếp theo: id,length,is_horizontal,row,col
5. Xe mục tiêu màu đỏ, các xe khác có màu khác nhau, cổng ra màu vàng.