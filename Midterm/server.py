from flask import Flask, request
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file_data = request.data
    if file_data:
        print("File received successfully!")
        return "File uploaded successfully!", 200
    else:
        return "No file uploaded!", 400

# Thêm route mới
@app.route('/uploadfile', methods=['POST'])
def upload_file_alias():
    file_data = request.data
    if file_data:
        print("File received on /uploadfile!")
        return "File uploaded successfully on /uploadfile!", 200
    else:
        return "No file uploaded on /uploadfile!", 400

if __name__ == "__main__":
    app.run(port=5000)
