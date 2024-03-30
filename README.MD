Tạo thư mục compose
sudo git clone https://gitlab.com/tnetwork96/seafootbot.git
sudo git clone https://gitlab.com/tnetwork96/google_api.git
move google_api và seafootbot vào thư mục compose
move file docker-compose từ seafootbot ra thư mục compose bằng command: 
- sudo cp docker-compose.yaml ../../compose/
sau đó chạy command:
- sudo docker-compose up -d --build