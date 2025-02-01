"団体コード"	"都道府県名（漢字）"	"市区町村名（漢字）"	"都道府県名（カナ）"	"市区町村名（カナ）"

CREATE TABLE municipalities (
    id SERIAL PRIMARY KEY,
    prefecture_kanji VARCHAR(255) NOT NULL,
    municipalities_kanji VARCHAR(255) NOT NULL,
    prefecture_kana VARCHAR(255) NOT NULL,
    municipalities_kana VARCHAR(255) NOT NULL
);
-- municipalities
--  地方自治体の名前を格納するテーブル
--  id　       :　団体コード
--  prefecture_kanji　       :　都道府県名（漢字）
--  municipalities_kanji　   :　市区町村名（漢字）
--  prefecture_kana　        :　都道府県名（カナ）
--  municipalities_kana　    :　市区町村名（カナ）

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
);
-- categories
--  ごみ分別目の名前を格納するテーブル
--  category_id　           :　ごみ分別目のID
--  category_name　         :　ごみ分別目の名前
--  例）可燃ごみ、不燃ごみ、資源ごみ

CREATE TABLE item_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL UNIQUE
);
-- item_types
--  ごみの種類を格納するテーブル
--  例）ペットボトル、新聞紙、布類
--  type_id　               :　ごみの種類のID
--  type_name　             :　ごみの種類の名前
--  explanation             :  説明


CREATE TABLE municipality_itemtype_category_map (
    map_id INTEGER SERIAL PRIMARY KEY,
    municipality_id INTEGER REFERENCES municipalities(municipality_id),
    type_id INTEGER REFERENCES item_types(type_id),
    category_id INTEGER REFERENCES categories(category_id)
);
-- municipality_itemtype_category_map
--  地方自治体、ごみの種類、ごみ分別目のマッピングを格納するテーブル
--  map_id　                :　マッピングのID
--  municipality_id　       :　自治体のID
--  type_id　               :　ごみの種類のID
--  category_id　           :　ごみ分別目のID
--  instruction_text　      :　分別方法の説明

CREATE TABLE municipality_category_instructions (
    instruction_id SERIAL PRIMARY KEY,
    municipality_id INTEGER REFERENCES municipalities(municipality_id),
    category_id INTEGER REFERENCES categories(category_id),
    instruction_text TEXT NOT NULL
);
-- municipality_category_instructions
--  地方自治体、ごみ分別目、分別方法の説明を格納するテーブル
--  instruction_id　        :　分別方法のID
--  municipality_id　       :　自治体のID
--  category_id　           :　ごみ分別目のID
--  instruction_text　      :　分別方法の説明