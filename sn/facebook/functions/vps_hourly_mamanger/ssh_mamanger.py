import io

import paramiko
from os import path, listdir

class SSHManager:
    def __init__(self, ):
        self.private_key_folder = r"D:\p_key"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def load_private_keys(self):
        private_keys = []
        try:
            # Lấy danh sách tên các tệp trong thư mục
            files = listdir(self.private_key_folder)

            # Lọc ra các tệp có tên bắt đầu bằng 'private_key'
            private_key_files = [file for file in files if file.startswith('private_key')]

            # Đọc nội dung của từng tệp và thêm vào danh sách
            for file in private_key_files:
                file_path = path.join(self.private_key_folder, file)
                with open(file_path, 'r') as f:
                    private_keys.append(f.read().strip())
        except Exception as e:
            print("An error occurred while loading private keys:", str(e))
        return private_keys

    def check_matching_private_key(self, public_key, private_keys):
        matching_private_key = None
        for private_key_str in private_keys:
            try:
                # Tạo đối tượng khóa RSA từ chuỗi khóa riêng tư
                private_key_file = io.StringIO()
                private_key_file.write(private_key_str)
                keyfile = io.StringIO(private_key_str)
                private_key_file.seek(0)
                private_key = paramiko.RSAKey.from_private_key(private_key_file)
                # So sánh khóa công khai với khóa công khai từ khóa riêng tư
                if private_key.get_base64() in public_key:
                    matching_private_key = private_key
                    break
            except paramiko.ssh_exception.SSHException:
                pass
        return matching_private_key

    def auto_connect(self, host, username,  public_key):
        p_key_list = self.load_private_keys()
        private_key = self.check_matching_private_key(public_key, p_key_list)
        try:
            # Kết nối bằng cách sử dụng khóa riêng đã tải
            self.ssh.connect(hostname=host, username=username, pkey=private_key)
            print("Connected to", host)
        except Exception as e:
            print("Connection failed:", str(e))

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            print("Output:", output)
            if error:
                print("Error:", error)
        except Exception as e:
            print("An error occurred while executing command:", str(e))

    def close(self):
        self.ssh.close()
        print("Connection closed")


# Thay thế các thông tin sau bằng thông tin của VPS của bạn
# hostname = "103.205.60.109"
# username = "root"
# public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7jo27pQca9b8PvFVoJ6vuV1jBjJo2iZO5xo/tP1HQCiy6TUVE9Nrw4tHYPq44D9bNbHGr/jCiNdgDh1DDl+eEFI1/Eo+rBA9+WvUaUXDCIVJtXxfrCOsxHrSbEOQ83V0uiLzyDH5ha77SXY7xc2HtpZWbqNNRkFydCe8BfwqmDM7Zlc/QVCpQjBRhwslWjt7KMLSD5UE/EmCBoG1+ZHlT00p0Bs3YuSgqnigs3reCAOQR0LtusZmmZjr27qBy4qcAI18CKWF3gdm7X9BVCU4ZjMcs78drgYiNcFhGIpU+KRELD6vocjMsdTHASu9YVLxHebtVUAx52nJ6vT6uNb1ZSEeOJ4MHHdg+x50bAqg3XnhE9RO/srhZuvfW5ME/dwXCeLWPFuPzHRvjmvx/8wOaFAaI3i/ryz52ouC9A3hrMzKJ9UDFPndyfeVVQOTCbzrYCalmfX5/F1JZEL33YtoTzp98H9R4ibuj8jS1DZG9waeesVzsCfPAusz0UbBBvb8= root@MASTER-hourly.lanit.com.vn"
# ssh_manager = SSHManager()
# ssh_manager.auto_connect(host=hostname, username=username, public_key=public_key)
# ssh_manager.execute_command("ls -l")
# ssh_manager.execute_command("df -h")
#
# # Đóng kết nối SSH
# ssh_manager.close()
