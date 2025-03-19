import os
import sys
from PIL import Image

def split_vertical_rectangle_into_squares(input_path, output_dir):
    """
    縦長長方形画像を幅(width)を一辺とする正方形に分割して
    上部・下部の2枚の画像を出力する。
    上部と下部の切り出し範囲が重なる場合がある点に注意。

    Parameters
    ----------
    input_path : str
        入力画像のファイルパス
    output_dir : str
        出力先フォルダのパス
    """
    # 出力先フォルダが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 画像を開く
    img = Image.open(input_path)
    width, height = img.size
    
    # 正方形の一辺を幅(width)とする
    side = width
    
    # 万が一、縦より幅の方が大きい画像だった場合はエラーを出す
    if height < side:
        print("縦の長さが幅よりも短いため、正方形に切り出せません。")
        return
    
    # 上部の正方形 (0,0)～(width,width)
    top_square = img.crop((0, 0, side, side))
    
    # 下部の正方形 (0, height-width)～(width,height)
    bottom_square = img.crop((0, height - side, side, height))
    
    # ファイルパスを作成して保存
    top_square_path = os.path.join(output_dir, "top_square.png")
    bottom_square_path = os.path.join(output_dir, "bottom_square.png")
    
    top_square.save(top_square_path)
    bottom_square.save(bottom_square_path)
    
    print(f"上部の正方形を {top_square_path} に保存しました。")
    print(f"下部の正方形を {bottom_square_path} に保存しました。")

if __name__ == "__main__":
    """
    実行例:
      python split_into_squares.py input.jpg output_folder
    """
    if len(sys.argv) != 3:
        print("使い方: python split_into_squares.py <入力画像パス> <出力フォルダパス>")
        sys.exit(1)
    
    input_img = sys.argv[1]
    output_folder = sys.argv[2]
    
    split_vertical_rectangle_into_squares(input_img, output_folder)
