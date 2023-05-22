<div align="center">

NLP Backend

</div>

### Thiết lập môi trường

##### Cài môi trường java để chạy lệnh tách từ

- Có thể đọc hường dẫn chi tiết tại [đây](https://github.com/ChenRocks/cnn-dailymail)

1. Nếu chưa cài môi trường java thì cài, kiểm tra bằng lệnh

   ```shell
   java --version
   ```

2. Download coreNLP tại [đây](https://stanfordnlp.github.io/CoreNLP/). Sau khi download thì giải nén ra
3. Thêm vào bash profile:

   ```shell
   export CLASSPATH=/path/to/stanford-corenlp-full-2016-10-31/stanford-corenlp-3.7.0.jar
   ```

###### Cài đặt thư viện

- Chương trình sử dụng [anaconda](https://www.anaconda.com/) để cài thư viện

###### Điều chỉnh các config

1. Điều chỉnh lại đường dẫn đến các thư mục liên quan

- Điều chỉnh tại [đây](app/config/constants.py)

### Chạy chương trình

1. Active môi trường anaconda

   ```shell
   conda activate
   ```

2. Cài đặt thư viện
3. export java classpath

   ```shell
   export CLASSPATH=../../nlp/stanford-corenlp-4.5.1/stanford-corenlp-4.5.1.jar
   ```

4. Chạy chương trình

   ```shell
   python3 main.py
   ```
