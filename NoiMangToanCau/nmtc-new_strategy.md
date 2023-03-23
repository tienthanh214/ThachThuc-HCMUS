# Strategy 1: (1 trên - 4 dưới)
## flow chính:
- Thành truyền raw
- Trực nhận raw
- LA đổi raw sang binary
- Nghĩa đổi binary sang hex
- Khôi xor hex
- Trực đổi hex sang char
## flow phụ, song song:
- Nghĩa đổi key từ dec sang hex
- Khôi viết bảng xor
> Lưu ý: Cần luyện nhanh phần truyền raw để Trực nhận xong qua chuyển hex
## Ưu điểm:
- Nếu có lỗi thì check dễ hơn cách cũ
- Truyền ít kí tự hơn cách cũ, chỉ cần 56 kí tự
## Nhược điểm:
- Số loại kí tự cần phải nhớ để truyền lớn hơn cách cũ: gồm 32 kí tự, gồm số và kí tự đặc biệt
- Khi muốn optimize thời gian, cần phải optimize thời gian Trực nhận của giáo và cả thời gian Trực đổi hex sang chả (đấy là Trực nghĩ, thực tế thì chưa chắc chắc)



# Strategy 2: (4 trên - 1 dưới)
## flow chính:
- LA đổi raw sang binary
- Nghĩa đổi binary sang hex
- Khôi xor hex
- Trực đổi hex sang char + truyển cho giáo
- Thành nhận hex
## flow phụ:
- Thành truyền key cho Trực
- Trực đổi key từ dec sang hex
- Khôi viết bảng xor
> Lưu ý: Trực giải hex và truyền xuống tuỳ ý Trực (ví dụ như giải và đọc đc 1 từ thì sẽ truyền xuống, nếu gặp lỗi thì check lại ngay rồi mới truyền)
## Ưu điểm:
- 100% giải đúng từ khoá, không thể lỗi được, xui lắm chỉ có thể sai ở bước Trực truyền xuống giáo thôi
- Truyền ít kí tự, chỉ cần 35 kí tự, nhanh hơn cả cách trên
## Nhược điểm:
- Số loại kí tự cần phải nhớ để truyền lớn: khoảng 90 kí tự, gồm cả chữ thường, chữ hoa, số và kí tự đặc biệt
