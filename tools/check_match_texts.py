# -*- coding: utf-8 -*-
# @FileName  : check_match_texts.py
# @Description 按符号检查完整文本返回
# @Author： 公众号：阿三先生
# @Date 3/28/23 4:48 PM
# @Version 1.0

character = [",", "?", "!", "，", "。", "？", "！", "......", "'", "‘", "’", "\"", "”", "“"]

def func_match_text(texts):
    if texts.strip()[-1] in character[-6:] and texts.strip()[-2] not in character[:-6]:
        return False

    shuang = [char for char in texts.strip() if char in character[-6:]]
    if not shuang:
      return True

    for tmp_shuang in shuang:
      if tmp_shuang == "'" and texts.count(tmp_shuang) % 2 != 0:
        return False

      if tmp_shuang == "\"" and texts.count(tmp_shuang) % 2 != 0:
        return False

      if tmp_shuang == "‘" and texts.count(tmp_shuang) != texts.count("’"):
        return False

      if tmp_shuang == "’" and texts.count(tmp_shuang) != texts.count("‘"):
        return False

      if tmp_shuang == "”" and texts.count(tmp_shuang) != texts.count("“"):
        return False

      if tmp_shuang == "“" and texts.count(tmp_shuang) != texts.count("”"):
        return False

    return True
