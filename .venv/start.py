import moondream as md
from PIL import Image
import sys
import os

# Initialize with local model path. Can also read .mf.gz files, but we recommend decompressing
# up-front to avoid decompression overhead every time the model is initialized.
model = md.vl(model="../model/moondream-2b-int8.mf")

folder_path = "../dataset"
Im = []
Im_name = []

for file_name in os.listdir(folder_path):
    if file_name.endswith((".png","jpg","jpeg","bmp")):
        file_path = os.path.join(folder_path, file_name)
        image = Image.open(file_path)
        # 解析图片
        encoded_image = model.encode_image(image)

        # Generate caption
        caption = model.caption(encoded_image)["caption"]
        print("Caption:", caption)

        # Ask questions
        answer = model.query(encoded_image, "What's in this image?")["answer"]
        answer = str(answer)
        # 创建一个与图片名相同的txt文件
        txt_file_name = os.path.splitext(file_name)[0] + ".txt"
        txt_file_path = os.path.join(folder_path, txt_file_name)

        print("正在保存"+file_name)
        # 将图片名称写入txt文件,pyhton3默认Unicode，win简中txt默认gbk，冲突报错
        with open(txt_file_path, "w",encoding='utf-8') as txt_file:
            txt_file.write(answer.encode('utf-8').decode('utf-8'))