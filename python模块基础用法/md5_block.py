import hashlib
# 待加密信息
import json

str = 'this is a md5 test.'

# 创建md5对象
m = hashlib.md5()

# Tips
# 此处必须encode
# 若写法为m.update(str)  报错为： Unicode-objects must be encoded before hashing
# 因为python3里默认的str是unicode
# 或者 b = bytes(str, encoding='utf-8')，作用相同，都是encode为bytes

b = str.encode(encoding='utf-8')
m.update(b)
str_md5 = m.hexdigest()

print('MD5加密前为 ：' + str)
print('MD5加密后为 ：' + str_md5)


# 方法二 ：b‘’前缀代表的就是bytes
str_md5 = hashlib.md5(b'this is a md5 test.').hexdigest()
print('MD5加密后为 ：' + str_md5)


def md5_hex():
    m = hashlib.md5()
    info = {"info": "1"}
    m.update(repr(info).encode(encoding='utf-8'))
    hex_info = m.hexdigest()
    print(hex_info)


if __name__ == '__main__':
    md5_hex()