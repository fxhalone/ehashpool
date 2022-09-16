import hmac, base64, struct, hashlib, time



"""计算谷歌验证码（16位谷歌秘钥，生成6位验证码）"""

# 使用静态方法，调用这个方法时，不必对类进行实例化

def getGoogleCode(secret, current_time=int(time.time()) // 30):
    """
    :param secret:   16位谷歌秘钥
    :param current_time:   时间（谷歌验证码是30s更新一次）
    :return:  返回6位谷歌验证码
    """
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", current_time)
    google_code = hmac.new(key, msg, hashlib.sha1).digest()
    o = ord(chr(google_code[19])) & 15  # python3时，ord的参数必须为chr类型
    google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
    return '%06d' % google_code  # 不足6位时，在前面补0


if __name__ == '__main__':
    secret_key = "YWVHUKUYMOOISMCH"
    print(getGoogleCode(secret_key))    # 并未实例化CalGoogleCode，也可以调用它的方法