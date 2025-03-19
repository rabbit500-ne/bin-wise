from bin_wise.utils.pdf2pic import Pdf2Pic
import os
from bin_wise.utils.s6pad import split_image_with_overlap
from bin_wise.utils.picturellm import PictureLLM
import argparse

pdf_pic_dir = "./data/pdf_pic"
square_dir = "./data/square"
ocr_text_dir = "./data/ocr_text"

class pdf2text:
    def __init__(self):
        self.pictureLLM = PictureLLM()

    def convert(self, pdf_path):
        pdf_name = os.path.basename(pdf_path).split(".")[0]
        pic = Pdf2Pic("./output")
        page_paths = pic.run(pdf_path)

        for idx, pic_path in enumerate(page_paths):
            breakpoint()
            # 画像を正方形に分割
            square_paths = split_image_with_overlap(pic_path, square_dir)
            text = self.pictureLLM.invoke(square_paths)
            with open(os.path.join(ocr_text_dir, f"{pdf_name}_{idx}.txt"), "w") as f:
                f.write(text)
            
        # さらに画像を正方形に分割
        return pic_path
    
if __name__ == "__main__":
    # の引数で指定したPDFファイルをテキストに変換
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", help="PDF file path")
    args = parser.parse_args()

    pdf2text = pdf2text()
    pdf2text.convert(args.pdf_path)