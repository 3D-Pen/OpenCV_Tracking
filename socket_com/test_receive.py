import socket
import keyboard

# サーバーのIPアドレスとポート番号を設定
SERVER_HOST = '169.254.13.242'  # 全てのネットワークインターフェースから接続を受け付ける
SERVER_PORT = 5000               # クライアント側と同じポート番号

def receive_file(save_path):
    # ソケットを作成し、TCP接続を設定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f'Server listening on {SERVER_HOST}:{SERVER_PORT}')
        
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')
        
        # ファイルを受信して保存
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            with open(save_path, 'ab') as file:  # 'ab'モードで追記
                file.write(data)
                
            print(f'Received {len(data)} bytes. Press "n" to stop receiving.')

        print('File received successfully.')

if __name__ == "__main__":
    # 受信スレッドを開始するためのラッパー関数
    def start_receiving():
        save_path = 'received.txt'
        while True:
            receive_file(save_path)
            if keyboard.is_pressed('n'):  # 'n'キーが押されているか確認
                print("Stopping data reception.")
                break

    print("Press 'n' to stop receiving data.")
    start_receiving()
