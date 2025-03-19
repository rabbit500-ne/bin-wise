""" ストアに登録を行う """
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic import BaseModel
import sqlite3
import pandas as pd
from bin_wise.embedd import EMBEDD, EmbeddingModel 


"""地方自治体 Excelファイルのデータ構造
"団体コード"	"都道府県名（漢字）"	"市区町村名（漢字）"	"都道府県名（カナ）"	"市区町村名（カナ）"

"""

class Municipalities(BaseModel):
    # 団体コード
    id: str
    # 都道府県名（漢字）
    prefecture_kanji : str    
    # 市区町村名（漢字）
    municipalities_kanji : str
    # 都道府県名（カナ）
    prefecture_kana : str
    # 市区町村名（カナ）
    municipalities_kana : str


"""
-- categories
--  ごみ分別目の名前を格納するテーブル
--  category_id　           :　ごみ分別目のID
--  category_name　         :　ごみ分別目の名前
--  例）可燃ごみ、不燃ごみ、資源ごみ
"""
class Categories(BaseModel):
    # ごみ分別目のID
    category_id: str
    # ごみ分別目の名前
    category_name: str

"""

-- item_types
--  ごみの種類を格納するテーブル
--  例）ペットボトル、新聞紙、布類
--  type_id　               :　ごみの種類のID
--  type_name　             :　ごみの種類の名前
--  explanation             :  説明
"""
class ItemTypes(BaseModel):
    # ごみの種類のID
    type_id: str
    # ごみの種類の名前
    type_name: str
    # ごみの種類の名前のベクトル
    type_vector: list
    # 説明
    explanation: str
    # 説明ベクトル
    explanation_vector: list


class MunicipalityItemTypeCategoryMap(BaseModel):
    """自治体、ごみの種類、ごみ分別目のマッピング"""
    # マッピングのID
    id: str
    # 自治体のID
    municipality_id: str
    # ごみの種類のID
    type_id: str
    # ごみ分別目のID
    category_id: str
    # 補足
    instruction_text: str


class DBhandler:
    def __init__(self):
        self.conn = sqlite3.connect(os.getenv('DB_PATH'))
        self.cur = self.conn.cursor()

    def set_municipalities(self, municipalities: Municipalities):
        # idとnameを登録
        self.cur.execute('INSERT INTO municipalities (id, prefecture_kanji, municipalities_kanji, prefecture_kana, municipalities_kana) VALUES (?, ?, ?, ?, ?)',
         (municipalities.id, municipalities.prefecture_kanji, municipalities.municipalities_kanji, municipalities.prefecture_kana, municipalities.municipalities_kana))
        self.conn.commit()

    def get_municipalities(self):
        self.cur.execute('SELECT * FROM municipalities')
        return self.cur.fetchall()

    def close(self):
        self.conn.close()

    def load_municipalities(self, file_path):
        df = pd.read_excel(file_path)
        for i in range(len(df)):
            municipalities = Municipalities(
                id=df.iloc[i, 0],
                prefecture_kanji=df.iloc[i, 1],
                municipalities_kanji=df.iloc[i, 2],
                prefecture_kana=df.iloc[i, 3],
                municipalities_kana=df.iloc[i, 4]
            )
            self.set_municipalities(municipalities)                

        return self.cur.fetchall()
    
    def set_categories(self, categorie_name: str):
        # idは自動採番
        # category_nameはユニーク。重複する場合はFalseを返す
        # 既に存在するかチェック
        self.cur.execute("SELECT id FROM categories WHERE value = ?", (value,))
        row = cursor.fetchone()
        
        if row:
            return row[0]  # 既存の id を返す
        
        # 存在しない場合は挿入
        self.cur.execute("INSERT INTO categories (value) VALUES (?)", (value,))
        self.conn.commit()  # 自動採番された id を確定
        return cursor.lastrowid  # 挿入した id を返す

    def set_item_types(self, item_type: str):
        # idは自動採番
        # item_typeはユニーク。重複する場合はFalseを返す
        # 既に存在するかチェック
        self.cur.execute("SELECT id FROM item_types WHERE value = ?", (value,))
        row = cursor.fetchone()
        
        if row:
            return row[0]  # 既存の id を返す
        
        # 存在しない場合は挿入
        self.cur.execute("INSERT INTO item_types (value) VALUES (?)", (value,))
        self.conn.commit()
        return cursor.lastrowid  # 挿入した id を返す

    def set_municipality_itemtype_category_map(self, municipality_id: int, item_name: str, categorie_name: str, instruction_text: str):
        category_id = self.set_categories(categorie_name)
        item_type_id = self.set_item_types(item_name)
        # idは自動採番
        self.cur.execute("INSERT INTO municipality_itemtype_category_map (municipality_id, item_type_id, category_id, instruction_text) VALUES (?, ?, ?, ?)", 
            (municipality_id, item_type_id, category_id, instruction_text))

        self.conn.commit()

    def get_item_type_id(self, item_name: str):
        self.cur.execute("SELECT id FROM item_types WHERE value = ?", (value, ))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

    # ごみ捨て方法を取得
    def get_category(self, item_type_id: int, municipality_id: int):
        """ category_name , instruction_text を取得""" 
        self.cur.execute("SELECT category_name, instruction_text FROM municipality_itemtype_category_map WHERE municipality_id = ? AND item_type_id = ?", 
            (municipality_id, item_type_id))
        # MunicipalityItemTypeCategoryMapインスタンスを返す
        mm = MunicipalityItemTypeCategoryMap(
            map_id = self.cur.fetchone()[0],
            municipality_id = municipality_id,
            type_id = item_type_id,
            category_id = self.cur.fetchone()[1],
        )
        return mm

from bin_wise import embedd


from qdrant_client import QdrantClient
print(os.environ.get("QDRANT_URL"))
print(os.environ.get("QDRANT_API_KEY"))
#qdrant_client = QdrantClient(
#    url=os.environ.get("QDRANT_URL"),
#    api_key=os.environ.get("QDRANT_API_KEY"),
#)


#print(qdrant_client.get_collections())