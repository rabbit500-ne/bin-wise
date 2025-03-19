import fitz  # pymupdf
import time
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

PIC_DIR = "./output"

class Pdf2Pic:
    """ PDFファイルを画像化するクラス

    出力ファイル名規則
    {pdfファイル名}_{ページ番号}.png
    """
    def __init__(self, pic_dir):
        self.pic_dir = pic_dir

    def render_page(self, item):
        file_name, img = item
        try:
            img.save(f"{self.pic_dir}/{file_name}")
        except Exception as e:
            pass
            # save_error_image(f"./output/{file_name}")

    def run(self, pdf_document):
        doc = fitz.open(pdf_document)

        # ディレクトリ、拡張子をとったファイル名取得
        doc_name = pdf_document.split("/")[-1].split(".")[0]

        zoom_x = 300 / 72  # 水平方向のズーム倍率（例: 2.0は200%）
        zoom_y = 300 / 72  # 垂直方向のズーム倍率（例: 2.0は200%）
        matrix = fitz.Matrix(zoom_x, zoom_y)
        
        pixs = {}
        pdfs = []
        # 各ページ、画像化
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            pix = page.get_pixmap(matrix=matrix)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # 横長の画像は2分割で保存
            # 横幅がしきい値を超える場合は2つに分割
            if pix.width > pix.height:
                half_width = pix.width // 2
                # 左側画像
                left_img = img.crop((0, 0, half_width, pix.height))
                # 右側画像
                right_img = img.crop((half_width, 0, pix.width, pix.height))
                file_name = f"{doc_name}_{page_number + 1}_1.png"
                pixs[file_name] = left_img
                pdfs.append((os.path.join(self.pic_dir, file_name), pdf_document, page_number + 1, 'left'))

                file_name = f"{doc_name}_{page_number + 1}_2.png"
                pixs[file_name] = right_img
                pdfs.append((os.path.join(self.pic_dir, file_name), pdf_document, page_number + 1, 'right'))
            else:
                file_name = f"{doc_name}_{page_number + 1}.png"
                pixs[file_name] = img
                pdfs.append((os.path.join(self.pic_dir, file_name), pdf_document, page_number + 1, 'full'))

        # 最大10スレッドで並行処理
        max_threads = 20
        with ThreadPoolExecutor(max_threads) as executor:
            executor.map(self.render_page, pixs.items())
        # return [os.path.join(self.pic_dir, path) for path in pixs.keys()]
        return pdfs

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to images.")
    parser.add_argument("--input", type=str, required=True, help="Input PDF file path")
    parser.add_argument("--output", type=str, required=True, help="Output directory path")
    args = parser.parse_args()

    pdf_file_url = args.input
    output_dir = args.output

    _start = time.time()
    pp = Pdf2Pic(output_dir)
    pp.run(pdf_file_url)
    print(f"Elapsed time: {time.time() - _start}")