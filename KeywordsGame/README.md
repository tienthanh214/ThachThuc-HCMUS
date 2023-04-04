# Round 1 - Khởi động - Keywords Game

Team 5 người chia thành 2 đội, một đội có nhiệm vụ mô tả keyword để đội còn lại có thể đoán được chính xác từ khoá tiếng anh về thuật ngữ IT.

[Luật chơi](https://fb.watch/jHYAFI4XFn/)

## Game giả lập vòng chơi 
### Keywords Database
Database keywords được lưu ở [keywords_.json](/KeywordsGame/keywords/keywords_.json)

Có định dạng json mảng object gồm 2 key là "Keywords" và "Counter", đại diện cho nội dung từ khoá và số lần đã gặp từ này.

Thêm từ khoá mới vào file json trên

### Chọn chế độ
Game hỗ trợ 2 chế độ là 
- Official: 10 từ khoá trong 120 giây như cuộc thi thật
- Endless: chế độ luyện tập vô hạn từ khoá, vô hạn thời gian

Có 3 chế độ thứ tự các từ khoá xuất hiện
- Sorted: từ ngắn đến dài
- Random: ngẫu nhiên
- Reversed: từ dài đến ngắn

<p float="center">
  <img src="/images/keyword_mode.png" alt="intro" height=300>
  <img src="/images/keyword_order.png" alt="intro" height=300>
</p>

### Chơi thôi

<p float="center">
  <img src="/images/keyword.png" alt="intro" height=300>
  <img src="/images/keyword_ingame.PNG" alt="ingame" height=300>
</p>



## Run game
1. Chạy trực tiếp file thực thi exe
2. Chạy file python (cần cài đặt thư viện pygame `pip3 install pygame`) 
  ```bash
  python keywords_game.py
  ```


## Version 3.0 - Latest
- Thống kê từ đã bỏ qua
- Thống kê thời gian và số từ đúng trong chế độ Official
- Các từ khoá đã gặp sẽ có xác suất gặp lại thấp hơn những từ ít gặp
