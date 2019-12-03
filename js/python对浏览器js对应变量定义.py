# coding:utf-8

# 说明 navicate = {};
"""
pip install PyExecJS
python  执行execjs代码实例
"""
import random

# 带参数
import execjs


def with_params():
    command = """
    function add (x, y){
        return x+y;
    };
    """
    ctx = execjs.compile(command)
    return ctx.call("add", 2, 2)


def get_k_h(url):
    b = int(random.random() * 100) + 1
    a = url.find("url=")
    url = url + "&k=" + str(b) + "&h=" + url[a + 4 + 21 + b: a + 4 + 21 + b + 1]
    return url


# 不带参数
def no_params():
    command = """
    function add (){
        return url;
    };
    """
    ctx = execjs.compile(command)
    return ctx.call("add")


def no_params_test():
    command = """
    const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><meta charset="UTF-8"><p>Hello world</p>`);
window = dom.window;
document = window.document;
    
   var CryptoJS = CryptoJS ||
function(u, p) {
var d = {},
l = d.lib = {},
s = function() {},
t = l.Base = {
    extend: function(a) {
        s.prototype = this;
        var c = new s;
        a && c.mixIn(a);
        c.hasOwnProperty("init") || (c.init = function() {
            c.$super.init.apply(this, arguments)
        });
        c.init.prototype = c;
        c.$super = this;
        return c
    },
    create: function() {
        var a = this.extend();
        a.init.apply(a, arguments);
        return a
    },
    init: function() {},
    mixIn: function(a) {
        for (var c in a) a.hasOwnProperty(c) && (this[c] = a[c]);
        a.hasOwnProperty("toString") && (this.toString = a.toString)
    },
    clone: function() {
        return this.init.prototype.extend(this)
    }
},
r = l.WordArray = t.extend({
    init: function(a, c) {
        a = this.words = a || [];
        this.sigBytes = c != p ? c: 4 * a.length
    },
    toString: function(a) {
        return (a || v).stringify(this)
    },
    concat: function(a) {
        var c = this.words,
        e = a.words,
        j = this.sigBytes;
        a = a.sigBytes;
        this.clamp();
        if (j % 4) for (var k = 0; k < a; k++) c[j + k >>> 2] |= (e[k >>> 2] >>> 24 - 8 * (k % 4) & 255) << 24 - 8 * ((j + k) % 4);
        else if (65535 < e.length) for (k = 0; k < a; k += 4) c[j + k >>> 2] = e[k >>> 2];
        else c.push.apply(c, e);
        this.sigBytes += a;
        return this
    },
    clamp: function() {
        var a = this.words,
        c = this.sigBytes;
        a[c >>> 2] &= 4294967295 << 32 - 8 * (c % 4);
        a.length = u.ceil(c / 4)
    },
    clone: function() {
        var a = t.clone.call(this);
        a.words = this.words.slice(0);
        return a
    },
    random: function(a) {
        for (var c = [], e = 0; e < a; e += 4) c.push(4294967296 * u.random() | 0);
        return new r.init(c, a)
    }
}),
w = d.enc = {},
v = w.Hex = {
    stringify: function(a) {
        var c = a.words;
        a = a.sigBytes;
        for (var e = [], j = 0; j < a; j++) {
            var k = c[j >>> 2] >>> 24 - 8 * (j % 4) & 255;
            e.push((k >>> 4).toString(16));
            e.push((k & 15).toString(16))
        }
        return e.join("")
    },
    parse: function(a) {
        for (var c = a.length,
        e = [], j = 0; j < c; j += 2) e[j >>> 3] |= parseInt(a.substr(j, 2), 16) << 24 - 4 * (j % 8);
        return new r.init(e, c / 2)
    }
},
b = w.Latin1 = {
    stringify: function(a) {
        var c = a.words;
        a = a.sigBytes;
        for (var e = [], j = 0; j < a; j++) e.push(String.fromCharCode(c[j >>> 2] >>> 24 - 8 * (j % 4) & 255));
        return e.join("")
    },
    parse: function(a) {
        for (var c = a.length,
        e = [], j = 0; j < c; j++) e[j >>> 2] |= (a.charCodeAt(j) & 255) << 24 - 8 * (j % 4);
        return new r.init(e, c)
    }
},
x = w.Utf8 = {
    stringify: function(a) {
        try {
            return decodeURIComponent(escape(b.stringify(a)))
        } catch(c) {
            throw Error("Malformed UTF-8 data");
        }
    },
    parse: function(a) {
        return b.parse(unescape(encodeURIComponent(a)))
    }
},
q = l.BufferedBlockAlgorithm = t.extend({
    reset: function() {
        this._data = new r.init;
        this._nDataBytes = 0
    },
    _append: function(a) {
        "string" == typeof a && (a = x.parse(a));
        this._data.concat(a);
        this._nDataBytes += a.sigBytes
    },
    _process: function(a) {
        var c = this._data,
        e = c.words,
        j = c.sigBytes,
        k = this.blockSize,
        b = j / (4 * k),
        b = a ? u.ceil(b) : u.max((b | 0) - this._minBufferSize, 0);
        a = b * k;
        j = u.min(4 * a, j);
        if (a) {
            for (var q = 0; q < a; q += k) this._doProcessBlock(e, q);
            q = e.splice(0, a);
            c.sigBytes -= j
        }
        return new r.init(q, j)
    },
    clone: function() {
        var a = t.clone.call(this);
        a._data = this._data.clone();
        return a
    },
    _minBufferSize: 0
});
l.Hasher = q.extend({
    cfg: t.extend(),
    init: function(a) {
        this.cfg = this.cfg.extend(a);
        this.reset()
    },
    reset: function() {
        q.reset.call(this);
        this._doReset()
    },
    update: function(a) {
        this._append(a);
        this._process();
        return this
    },
    finalize: function(a) {
        a && this._append(a);
        return this._doFinalize()
    },
    blockSize: 16,
    _createHelper: function(a) {
        return function(b, e) {
            return (new a.init(e)).finalize(b)
        }
    },
    _createHmacHelper: function(a) {
        return function(b, e) {
            return (new n.HMAC.init(a, e)).finalize(b)
        }
    }
});
var n = d.algo = {};
return d
} (Math); (function() {
var u = CryptoJS,
p = u.lib.WordArray;
u.enc.Base64 = {
    stringify: function(d) {
        var l = d.words,
        p = d.sigBytes,
        t = this._map;
        d.clamp();
        d = [];
        for (var r = 0; r < p; r += 3) for (var w = (l[r >>> 2] >>> 24 - 8 * (r % 4) & 255) << 16 | (l[r + 1 >>> 2] >>> 24 - 8 * ((r + 1) % 4) & 255) << 8 | l[r + 2 >>> 2] >>> 24 - 8 * ((r + 2) % 4) & 255, v = 0; 4 > v && r + 0.75 * v < p; v++) d.push(t.charAt(w >>> 6 * (3 - v) & 63));
        if (l = t.charAt(64)) for (; d.length % 4;) d.push(l);
        return d.join("")
    },
    parse: function(d) {
        var l = d.length,
        s = this._map,
        t = s.charAt(64);
        t && (t = d.indexOf(t), -1 != t && (l = t));
        for (var t = [], r = 0, w = 0; w < l; w++) if (w % 4) {
            var v = s.indexOf(d.charAt(w - 1)) << 2 * (w % 4),
            b = s.indexOf(d.charAt(w)) >>> 6 - 2 * (w % 4);
            t[r >>> 2] |= (v | b) << 24 - 8 * (r % 4);
            r++
        }
        return p.create(t, r)
    },
    _map: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
}
})(); (function(u) {
function p(b, n, a, c, e, j, k) {
    b = b + (n & a | ~n & c) + e + k;
    return (b << j | b >>> 32 - j) + n
}

function d(b, n, a, c, e, j, k) {
    b = b + (n & c | a & ~c) + e + k;
    return (b << j | b >>> 32 - j) + n
}

function l(b, n, a, c, e, j, k) {
    b = b + (n ^ a ^ c) + e + k;
    return (b << j | b >>> 32 - j) + n
}

function s(b, n, a, c, e, j, k) {
    b = b + (a ^ (n | ~c)) + e + k;
    return (b << j | b >>> 32 - j) + n
}

for (var t = CryptoJS,
r = t.lib,
w = r.WordArray,
v = r.Hasher,
r = t.algo,
b = [], x = 0; 64 > x; x++) b[x] = 4294967296 * u.abs(u.sin(x + 1)) | 0;
r = r.MD5 = v.extend({
    _doReset: function() {
        this._hash = new w.init([1732584193, 4023233417, 2562383102, 271733878])
    },
    _doProcessBlock: function(q, n) {
        for (var a = 0; 16 > a; a++) {
            var c = n + a,
            e = q[c];
            q[c] = (e << 8 | e >>> 24) & 16711935 | (e << 24 | e >>> 8) & 4278255360
        }
        var a = this._hash.words,
        c = q[n + 0],
        e = q[n + 1],
        j = q[n + 2],
        k = q[n + 3],
        z = q[n + 4],
        r = q[n + 5],
        t = q[n + 6],
        w = q[n + 7],
        v = q[n + 8],
        A = q[n + 9],
        B = q[n + 10],
        C = q[n + 11],
        u = q[n + 12],
        D = q[n + 13],
        E = q[n + 14],
        x = q[n + 15],
        f = a[0],
        m = a[1],
        g = a[2],
        h = a[3],
        f = p(f, m, g, h, c, 7, b[0]),
        h = p(h, f, m, g, e, 12, b[1]),
        g = p(g, h, f, m, j, 17, b[2]),
        m = p(m, g, h, f, k, 22, b[3]),
        f = p(f, m, g, h, z, 7, b[4]),
        h = p(h, f, m, g, r, 12, b[5]),
        g = p(g, h, f, m, t, 17, b[6]),
        m = p(m, g, h, f, w, 22, b[7]),
        f = p(f, m, g, h, v, 7, b[8]),
        h = p(h, f, m, g, A, 12, b[9]),
        g = p(g, h, f, m, B, 17, b[10]),
        m = p(m, g, h, f, C, 22, b[11]),
        f = p(f, m, g, h, u, 7, b[12]),
        h = p(h, f, m, g, D, 12, b[13]),
        g = p(g, h, f, m, E, 17, b[14]),
        m = p(m, g, h, f, x, 22, b[15]),
        f = d(f, m, g, h, e, 5, b[16]),
        h = d(h, f, m, g, t, 9, b[17]),
        g = d(g, h, f, m, C, 14, b[18]),
        m = d(m, g, h, f, c, 20, b[19]),
        f = d(f, m, g, h, r, 5, b[20]),
        h = d(h, f, m, g, B, 9, b[21]),
        g = d(g, h, f, m, x, 14, b[22]),
        m = d(m, g, h, f, z, 20, b[23]),
        f = d(f, m, g, h, A, 5, b[24]),
        h = d(h, f, m, g, E, 9, b[25]),
        g = d(g, h, f, m, k, 14, b[26]),
        m = d(m, g, h, f, v, 20, b[27]),
        f = d(f, m, g, h, D, 5, b[28]),
        h = d(h, f, m, g, j, 9, b[29]),
        g = d(g, h, f, m, w, 14, b[30]),
        m = d(m, g, h, f, u, 20, b[31]),
        f = l(f, m, g, h, r, 4, b[32]),
        h = l(h, f, m, g, v, 11, b[33]),
        g = l(g, h, f, m, C, 16, b[34]),
        m = l(m, g, h, f, E, 23, b[35]),
        f = l(f, m, g, h, e, 4, b[36]),
        h = l(h, f, m, g, z, 11, b[37]),
        g = l(g, h, f, m, w, 16, b[38]),
        m = l(m, g, h, f, B, 23, b[39]),
        f = l(f, m, g, h, D, 4, b[40]),
        h = l(h, f, m, g, c, 11, b[41]),
        g = l(g, h, f, m, k, 16, b[42]),
        m = l(m, g, h, f, t, 23, b[43]),
        f = l(f, m, g, h, A, 4, b[44]),
        h = l(h, f, m, g, u, 11, b[45]),
        g = l(g, h, f, m, x, 16, b[46]),
        m = l(m, g, h, f, j, 23, b[47]),
        f = s(f, m, g, h, c, 6, b[48]),
        h = s(h, f, m, g, w, 10, b[49]),
        g = s(g, h, f, m, E, 15, b[50]),
        m = s(m, g, h, f, r, 21, b[51]),
        f = s(f, m, g, h, u, 6, b[52]),
        h = s(h, f, m, g, k, 10, b[53]),
        g = s(g, h, f, m, B, 15, b[54]),
        m = s(m, g, h, f, e, 21, b[55]),
        f = s(f, m, g, h, v, 6, b[56]),
        h = s(h, f, m, g, x, 10, b[57]),
        g = s(g, h, f, m, t, 15, b[58]),
        m = s(m, g, h, f, D, 21, b[59]),
        f = s(f, m, g, h, z, 6, b[60]),
        h = s(h, f, m, g, C, 10, b[61]),
        g = s(g, h, f, m, j, 15, b[62]),
        m = s(m, g, h, f, A, 21, b[63]);
        a[0] = a[0] + f | 0;
        a[1] = a[1] + m | 0;
        a[2] = a[2] + g | 0;
        a[3] = a[3] + h | 0
    },
    _doFinalize: function() {
        var b = this._data,
        n = b.words,
        a = 8 * this._nDataBytes,
        c = 8 * b.sigBytes;
        n[c >>> 5] |= 128 << 24 - c % 32;
        var e = u.floor(a / 4294967296);
        n[(c + 64 >>> 9 << 4) + 15] = (e << 8 | e >>> 24) & 16711935 | (e << 24 | e >>> 8) & 4278255360;
        n[(c + 64 >>> 9 << 4) + 14] = (a << 8 | a >>> 24) & 16711935 | (a << 24 | a >>> 8) & 4278255360;
        b.sigBytes = 4 * (n.length + 1);
        this._process();
        b = this._hash;
        n = b.words;
        for (a = 0; 4 > a; a++) c = n[a],
        n[a] = (c << 8 | c >>> 24) & 16711935 | (c << 24 | c >>> 8) & 4278255360;
        return b
    },
    clone: function() {
        var b = v.clone.call(this);
        b._hash = this._hash.clone();
        return b
    }
});
t.MD5 = v._createHelper(r);
t.HmacMD5 = v._createHmacHelper(r)
})(Math); (function() {
var u = CryptoJS,
p = u.lib,
d = p.Base,
l = p.WordArray,
p = u.algo,
s = p.EvpKDF = d.extend({
    cfg: d.extend({
        keySize: 4,
        hasher: p.MD5,
        iterations: 1
    }),
    init: function(d) {
        this.cfg = this.cfg.extend(d)
    },
    compute: function(d, r) {
        for (var p = this.cfg,
        s = p.hasher.create(), b = l.create(), u = b.words, q = p.keySize, p = p.iterations; u.length < q;) {
            n && s.update(n);
            var n = s.update(d).finalize(r);
            s.reset();
            for (var a = 1; a < p; a++) n = s.finalize(n),
            s.reset();
            b.concat(n)
        }
        b.sigBytes = 4 * q;
        return b
    }
});
u.EvpKDF = function(d, l, p) {
    return s.create(p).compute(d, l)
}
})();
CryptoJS.lib.Cipher ||
function(u) {
var p = CryptoJS,
d = p.lib,
l = d.Base,
s = d.WordArray,
t = d.BufferedBlockAlgorithm,
r = p.enc.Base64,
w = p.algo.EvpKDF,
v = d.Cipher = t.extend({
    cfg: l.extend(),
    createEncryptor: function(e, a) {
        return this.create(this._ENC_XFORM_MODE, e, a)
    },
    createDecryptor: function(e, a) {
        return this.create(this._DEC_XFORM_MODE, e, a)
    },
    init: function(e, a, b) {
        this.cfg = this.cfg.extend(b);
        this._xformMode = e;
        this._key = a;
        this.reset()
    },
    reset: function() {
        t.reset.call(this);
        this._doReset()
    },
    process: function(e) {
        this._append(e);
        return this._process()
    },
    finalize: function(e) {
        e && this._append(e);
        return this._doFinalize()
    },
    keySize: 4,
    ivSize: 4,
    _ENC_XFORM_MODE: 1,
    _DEC_XFORM_MODE: 2,
    _createHelper: function(e) {
        return {
            encrypt: function(b, k, d) {
                return ("string" == typeof k ? c: a).encrypt(e, b, k, d)
            },
            decrypt: function(b, k, d) {
                return ("string" == typeof k ? c: a).decrypt(e, b, k, d)
            }
        }
    }
});
d.StreamCipher = v.extend({
    _doFinalize: function() {
        return this._process(!0)
    },
    blockSize: 1
});
var b = p.mode = {},
x = function(e, a, b) {
    var c = this._iv;
    c ? this._iv = u: c = this._prevBlock;
    for (var d = 0; d < b; d++) e[a + d] ^= c[d]
},
q = (d.BlockCipherMode = l.extend({
    createEncryptor: function(e, a) {
        return this.Encryptor.create(e, a)
    },
    createDecryptor: function(e, a) {
        return this.Decryptor.create(e, a)
    },
    init: function(e, a) {
        this._cipher = e;
        this._iv = a
    }
})).extend();
q.Encryptor = q.extend({
    processBlock: function(e, a) {
        var b = this._cipher,
        c = b.blockSize;
        x.call(this, e, a, c);
        b.encryptBlock(e, a);
        this._prevBlock = e.slice(a, a + c)
    }
});
q.Decryptor = q.extend({
    processBlock: function(e, a) {
        var b = this._cipher,
        c = b.blockSize,
        d = e.slice(a, a + c);
        b.decryptBlock(e, a);
        x.call(this, e, a, c);
        this._prevBlock = d
    }
});
b = b.CBC = q;
q = (p.pad = {}).Pkcs7 = {
    pad: function(a, b) {
        for (var c = 4 * b,
        c = c - a.sigBytes % c,
        d = c << 24 | c << 16 | c << 8 | c,
        l = [], n = 0; n < c; n += 4) l.push(d);
        c = s.create(l, c);
        a.concat(c)
    },
    unpad: function(a) {
        a.sigBytes -= a.words[a.sigBytes - 1 >>> 2] & 255
    }
};
d.BlockCipher = v.extend({
    cfg: v.cfg.extend({
        mode: b,
        padding: q
    }),
    reset: function() {
        v.reset.call(this);
        var a = this.cfg,
        b = a.iv,
        a = a.mode;
        if (this._xformMode == this._ENC_XFORM_MODE) var c = a.createEncryptor;
        else c = a.createDecryptor,
        this._minBufferSize = 1;
        this._mode = c.call(a, this, b && b.words)
    },
    _doProcessBlock: function(a, b) {
        this._mode.processBlock(a, b)
    },
    _doFinalize: function() {
        var a = this.cfg.padding;
        if (this._xformMode == this._ENC_XFORM_MODE) {
            a.pad(this._data, this.blockSize);
            var b = this._process(!0)
        } else b = this._process(!0),
        a.unpad(b);
        return b
    },
    blockSize: 4
});
var n = d.CipherParams = l.extend({
    init: function(a) {
        this.mixIn(a)
    },
    toString: function(a) {
        return (a || this.formatter).stringify(this)
    }
}),
b = (p.format = {}).OpenSSL = {
    stringify: function(a) {
        var b = a.ciphertext;
        a = a.salt;
        return (a ? s.create([1398893684, 1701076831]).concat(a).concat(b) : b).toString(r)
    },
    parse: function(a) {
        a = r.parse(a);
        var b = a.words;
        if (1398893684 == b[0] && 1701076831 == b[1]) {
            var c = s.create(b.slice(2, 4));
            b.splice(0, 4);
            a.sigBytes -= 16
        }
        return n.create({
            ciphertext: a,
            salt: c
        })
    }
},
a = d.SerializableCipher = l.extend({
    cfg: l.extend({
        format: b
    }),
    encrypt: function(a, b, c, d) {
        d = this.cfg.extend(d);
        var l = a.createEncryptor(c, d);
        b = l.finalize(b);
        l = l.cfg;
        return n.create({
            ciphertext: b,
            key: c,
            iv: l.iv,
            algorithm: a,
            mode: l.mode,
            padding: l.padding,
            blockSize: a.blockSize,
            formatter: d.format
        })
    },
    decrypt: function(a, b, c, d) {
        d = this.cfg.extend(d);
        b = this._parse(b, d.format);
        return a.createDecryptor(c, d).finalize(b.ciphertext)
    },
    _parse: function(a, b) {
        return "string" == typeof a ? b.parse(a, this) : a
    }
}),
p = (p.kdf = {}).OpenSSL = {
    execute: function(a, b, c, d) {
        d || (d = s.random(8));
        a = w.create({
            keySize: b + c
        }).compute(a, d);
        c = s.create(a.words.slice(b), 4 * c);
        a.sigBytes = 4 * b;
        return n.create({
            key: a,
            iv: c,
            salt: d
        })
    }
},
c = d.PasswordBasedCipher = a.extend({
    cfg: a.cfg.extend({
        kdf: p
    }),
    encrypt: function(b, c, d, l) {
        l = this.cfg.extend(l);
        d = l.kdf.execute(d, b.keySize, b.ivSize);
        l.iv = d.iv;
        b = a.encrypt.call(this, b, c, d.key, l);
        b.mixIn(d);
        return b
    },
    decrypt: function(b, c, d, l) {
        l = this.cfg.extend(l);
        c = this._parse(c, l.format);
        d = l.kdf.execute(d, b.keySize, b.ivSize, c.salt);
        l.iv = d.iv;
        return a.decrypt.call(this, b, c, d.key, l)
    }
})
} (); (function() {
for (var u = CryptoJS,
p = u.lib.BlockCipher,
d = u.algo,
l = [], s = [], t = [], r = [], w = [], v = [], b = [], x = [], q = [], n = [], a = [], c = 0; 256 > c; c++) a[c] = 128 > c ? c << 1 : c << 1 ^ 283;
for (var e = 0,
j = 0,
c = 0; 256 > c; c++) {
    var k = j ^ j << 1 ^ j << 2 ^ j << 3 ^ j << 4,
    k = k >>> 8 ^ k & 255 ^ 99;
    l[e] = k;
    s[k] = e;
    var z = a[e],
    F = a[z],
    G = a[F],
    y = 257 * a[k] ^ 16843008 * k;
    t[e] = y << 24 | y >>> 8;
    r[e] = y << 16 | y >>> 16;
    w[e] = y << 8 | y >>> 24;
    v[e] = y;
    y = 16843009 * G ^ 65537 * F ^ 257 * z ^ 16843008 * e;
    b[k] = y << 24 | y >>> 8;
    x[k] = y << 16 | y >>> 16;
    q[k] = y << 8 | y >>> 24;
    n[k] = y;
    e ? (e = z ^ a[a[a[G ^ z]]], j ^= a[a[j]]) : e = j = 1
}
var H = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54],
d = d.AES = p.extend({
    _doReset: function() {
        for (var a = this._key,
        c = a.words,
        d = a.sigBytes / 4,
        a = 4 * ((this._nRounds = d + 6) + 1), e = this._keySchedule = [], j = 0; j < a; j++) if (j < d) e[j] = c[j];
        else {
            var k = e[j - 1];
            j % d ? 6 < d && 4 == j % d && (k = l[k >>> 24] << 24 | l[k >>> 16 & 255] << 16 | l[k >>> 8 & 255] << 8 | l[k & 255]) : (k = k << 8 | k >>> 24, k = l[k >>> 24] << 24 | l[k >>> 16 & 255] << 16 | l[k >>> 8 & 255] << 8 | l[k & 255], k ^= H[j / d | 0] << 24);
            e[j] = e[j - d] ^ k
        }
        c = this._invKeySchedule = [];
        for (d = 0; d < a; d++) j = a - d,
        k = d % 4 ? e[j] : e[j - 4],
        c[d] = 4 > d || 4 >= j ? k: b[l[k >>> 24]] ^ x[l[k >>> 16 & 255]] ^ q[l[k >>> 8 & 255]] ^ n[l[k & 255]]
    },
    encryptBlock: function(a, b) {
        this._doCryptBlock(a, b, this._keySchedule, t, r, w, v, l)
    },
    decryptBlock: function(a, c) {
        var d = a[c + 1];
        a[c + 1] = a[c + 3];
        a[c + 3] = d;
        this._doCryptBlock(a, c, this._invKeySchedule, b, x, q, n, s);
        d = a[c + 1];
        a[c + 1] = a[c + 3];
        a[c + 3] = d
    },
    _doCryptBlock: function(a, b, c, d, e, j, l, f) {
        for (var m = this._nRounds,
        g = a[b] ^ c[0], h = a[b + 1] ^ c[1], k = a[b + 2] ^ c[2], n = a[b + 3] ^ c[3], p = 4, r = 1; r < m; r++) var q = d[g >>> 24] ^ e[h >>> 16 & 255] ^ j[k >>> 8 & 255] ^ l[n & 255] ^ c[p++],
        s = d[h >>> 24] ^ e[k >>> 16 & 255] ^ j[n >>> 8 & 255] ^ l[g & 255] ^ c[p++],
        t = d[k >>> 24] ^ e[n >>> 16 & 255] ^ j[g >>> 8 & 255] ^ l[h & 255] ^ c[p++],
        n = d[n >>> 24] ^ e[g >>> 16 & 255] ^ j[h >>> 8 & 255] ^ l[k & 255] ^ c[p++],
        g = q,
        h = s,
        k = t;
        q = (f[g >>> 24] << 24 | f[h >>> 16 & 255] << 16 | f[k >>> 8 & 255] << 8 | f[n & 255]) ^ c[p++];
        s = (f[h >>> 24] << 24 | f[k >>> 16 & 255] << 16 | f[n >>> 8 & 255] << 8 | f[g & 255]) ^ c[p++];
        t = (f[k >>> 24] << 24 | f[n >>> 16 & 255] << 16 | f[g >>> 8 & 255] << 8 | f[h & 255]) ^ c[p++];
        n = (f[n >>> 24] << 24 | f[g >>> 16 & 255] << 16 | f[h >>> 8 & 255] << 8 | f[k & 255]) ^ c[p++];
        a[b] = q;
        a[b + 1] = s;
        a[b + 2] = t;
        a[b + 3] = n
    },
    keySize: 8
});
u.AES = p._createHelper(d)
})();
var _0xa12e = ['appendChild', 'fromCharCode', 'ifLSL', 'undefined', 'mPDrG', 'DWwdv', 'styleSheets', 'addRule', '::before', '.context_kw', '::before{content:\x20\x22', 'cssRules', 'pad', 'clamp', 'sigBytes', 'YEawH', 'yUSXm', 'PwMPi', 'pLCFG', 'ErKUI', 'OtZki', 'prototype', 'endWith', 'test', '8RHz0u9wbbrXYJjUcstWoRU1SmEIvQZQJtdHeU9/KpK/nBtFWIzLveG63e81APFLLiBBbevCCbRPdingQfzOAFPNPBw4UJCsqrDmVXFe6+LK2CSp26aUL4S+AgWjtrByjZqnYm9H3XEWW+gLx763OGfifuNUB8AgXB7/pnNTwoLjeKDrLKzomC+pXHMGYgQJegLVezvshTGgyVrDXfw4eGSVDa3c/FpDtban34QpS3I=', 'enc', 'Latin1', 'parse', 'window', 'location', 'href', '146385F634C9CB00', 'decrypt', 'ZeroPadding', 'toString', 'split', 'length', 'style', 'type', 'setAttribute', 'async', 'getElementsByTagName', 'NOyra', 'fgQCW', 'nCjZv', 'parentNode', 'insertBefore', 'head']; (function(_0x4db306, _0x3b5c31) {
var _0x24d797 = function(_0x1ebd20) {
    while (--_0x1ebd20) {
        _0x4db306['push'](_0x4db306['shift']());
    }
};
_0x24d797(++_0x3b5c31);
} (_0xa12e, 0xcc));
var _0xea12 = function(_0x56430f, _0x7f6841) {
_0x56430f = _0x56430f - 0x0;
var _0x4f7a0f = _0xa12e[_0x56430f];
return _0x4f7a0f;
};
CryptoJS[_0xea12('0x0')]['ZeroPadding'] = {
'pad': function(_0x1df06f, _0x314b39) {
    var _0x2f7121 = {
        'YEawH': function _0x304fdc(_0x154e7c, _0x47ce8e) {
            return _0x154e7c - _0x47ce8e;
        },
        'yUSXm': function _0x15667f(_0x2118a7, _0x202af9) {
            return _0x2118a7 % _0x202af9;
        }
    };
    var _0x301b79 = _0x314b39 * 0x4;
    _0x1df06f[_0xea12('0x1')]();
    _0x1df06f[_0xea12('0x2')] += _0x2f7121[_0xea12('0x3')](_0x301b79, _0x2f7121[_0xea12('0x4')](_0x1df06f['sigBytes'], _0x301b79) || _0x301b79);
},
'unpad': function(_0x3994de) {
    var _0x542e1d = {
        'PwMPi': function _0x13be60(_0x37e2b3, _0x34d2aa) {
            return _0x37e2b3 - _0x34d2aa;
        },
        'byONr': function _0x41eeb1(_0x42220d, _0x40e5bd) {
            return _0x42220d & _0x40e5bd;
        },
        'pLCFG': function _0x562ecb(_0x2581d9, _0x590c51) {
            return _0x2581d9 >>> _0x590c51;
        },
        'FRqnC': function _0x582fef(_0x4c5451, _0x219412) {
            return _0x4c5451 - _0x219412;
        },
        'DwxPM': function _0x13a0d9(_0x3ce2bb, _0x236747) {
            return _0x3ce2bb * _0x236747;
        },
        'ErKUI': function _0x31d02b(_0x42d286, _0x4a8edd) {
            return _0x42d286 % _0x4a8edd;
        },
        'OtZki': function _0x4024cd(_0x163bf9, _0x543826) {
            return _0x163bf9 + _0x543826;
        }
    };
    var _0x32bd3a = _0x3994de['words'];
    var _0x2a5053 = _0x542e1d[_0xea12('0x5')](_0x3994de[_0xea12('0x2')], 0x1);
    while (!_0x542e1d['byONr'](_0x542e1d['pLCFG'](_0x32bd3a[_0x542e1d[_0xea12('0x6')](_0x2a5053, 0x2)], _0x542e1d['FRqnC'](0x18, _0x542e1d['DwxPM'](_0x542e1d[_0xea12('0x7')](_0x2a5053, 0x4), 0x8))), 0xff)) {
        _0x2a5053--;
    }
    _0x3994de[_0xea12('0x2')] = _0x542e1d[_0xea12('0x8')](_0x2a5053, 0x1);
}
};
String[_0xea12('0x9')][_0xea12('0xa')] = function(_0x4ae995) {
var _0x5ac4ca = {
    'khqHo': function _0x4168d6(_0x311e85, _0x420e7f) {
        return _0x311e85 + _0x420e7f;
    }
};
var _0xa42d0b = new RegExp(_0x5ac4ca['khqHo'](_0x4ae995, '$'));
return _0xa42d0b[_0xea12('0xb')](this);
};
var data = _0xea12('0xc');
var keywords = CryptoJS[_0xea12('0xd')][_0xea12('0xe')][_0xea12('0xf')]('6B0600CA9BCE5B24');
var iv = '';
try {
if (top[_0xea12('0x10')][_0xea12('0x11')][_0xea12('0x12')] != window[_0xea12('0x11')]['href']) {
    top['window'][_0xea12('0x11')]['href'] = window[_0xea12('0x11')][_0xea12('0x12')];
}
iv = CryptoJS['enc'][_0xea12('0xe')]['parse']('6B0600CA9BCE5B24');
} catch(_0x3f6f9e) {
iv = CryptoJS[_0xea12('0xd')][_0xea12('0xe')]['parse'](_0xea12('0x13'));
}
var decrypted = CryptoJS['AES'][_0xea12('0x14')](data, keywords, {
'iv': iv,
'padding': CryptoJS[_0xea12('0x0')][_0xea12('0x15')]
});
var secWords = decrypted[_0xea12('0x16')](CryptoJS['enc']['Utf8'])[_0xea12('0x17')](',');
var words = new Array(secWords[_0xea12('0x18')]);
var n = document['createElement'](_0xea12('0x19'));
n['setAttribute'](_0xea12('0x1a'), 'text/css');
n[_0xea12('0x1b')](_0xea12('0x1c'), !![]);
var jsLast = function() {
var _0x28d7f2 = {
    'NOyra': 'head',
    'fgQCW': 'link',
    'nCjZv': function _0x5de21d(_0x48b6d5, _0x51ba19) {
        return _0x48b6d5 > _0x51ba19;
    }
};
var _0x4f2f4a = document[_0xea12('0x1d')](_0x28d7f2[_0xea12('0x1e')])[0x0][_0xea12('0x1d')](_0x28d7f2[_0xea12('0x1f')]);
if (_0x4f2f4a && _0x28d7f2[_0xea12('0x20')](_0x4f2f4a[_0xea12('0x18')], 0x0)) {
    return _0x4f2f4a[0x0];
} else {
    return null;
}
} ();
if (jsLast) {
jsLast[_0xea12('0x21')][_0xea12('0x22')](n, jsLast);
} else {
document[_0xea12('0x1d')](_0xea12('0x23'))[0x0][_0xea12('0x24')](n);
}
for (var i = 0x0; i < secWords[_0xea12('0x18')]; i++) {
var _0x5420ee = '3|5|2|4|0|1' [_0xea12('0x17')]('|'),
_0x9ff9d9 = 0x0;
while ( !! []) {
    switch (_0x5420ee[_0x9ff9d9++]) {
    case '0':
        _0x423190 = _0x5796d9(_0x423190);
        continue;
    case '1':
        words[i] = String[_0xea12('0x25')](_0x423190);
        continue;
    case '2':
        var _0x5796d9 = function(_0x490c80) {
            var _0x1532b6 = {
                'ifLSL': function _0x256992(_0x118bb, _0x36aa09) {
                    return _0x118bb + _0x36aa09;
                }
            };
            return _0x1532b6[_0xea12('0x26')](_0x490c80, 0x3 * +!(typeof document === _0xea12('0x27')));
        };
        continue;
    case '3':
        var _0x423190 = secWords[i];
        continue;
    case '4':
        _0x423190 = _0x3e8e1e(_0x423190);
        continue;
    case '5':
        var _0x3e8e1e = function(_0xd024e1) {
            var _0x3e40d1 = {
                'mPDrG': function _0x411e6f(_0xa8939, _0x278c20) {
                    return _0xa8939 % _0x278c20;
                },
                'DWwdv': function _0x1e0293(_0x5b15eb, _0x443876) {
                    return _0x5b15eb - _0x443876;
                }
            };
            return _0x3e40d1[_0xea12('0x28')](_0xd024e1, 0x2) ? _0x3e40d1[_0xea12('0x29')](_0xd024e1, 0x2) : _0xd024e1 - 0x4;
        };
        continue;
    }
    break;
}
}
function info() {
return words
};
    """
    # ctx = execjs.compile(command, cwd=r'C:\Users\w001\AppData\Roaming\npm\node_modules')
    ctx = execjs.compile(command, cwd=r'C:\Users\wangrongming\AppData\Roaming\npm\node_modules')
    return ctx.call("info")


def wangyi_login():
    """
    网易登录
    :return:
    """
    command = """
var Hex = {
    hex: "0123456789abcdef",
    encode: function(e) {
        if (!e)
            return !1;
        var t = "";
        var i;
        var n = 0;
        do {
            i = e.charCodeAt(n++);
            t += this.hex.charAt(i >> 4 & 15) + this.hex.charAt(15 & i)
        } while (n < e.length);return t
    },
    decode: function(e) {
        if (!e)
            return !1;
        e = e.replace(/[^0-9abcdef]/g, "");
        var t = "";
        var i = 0;
        do
            t += String.fromCharCode(this.hex.indexOf(e.charAt(i++)) << 4 & 240 | 15 & this.hex.indexOf(e.charAt(i++)));
        while (i < e.length);return t
    }
};

var navigator = {};
var canary = 0xdeadbeefcafe;
var j_lm = 15715070 == (16777215 & canary);

function BigInteger(e, t, i) {
    if (null != e)
        if ("number" == typeof e)
            this.fromNumber(e, t, i);
        else if (null == t && "string" != typeof e)
            this.fromString(e, 256);
        else
            this.fromString(e, t)
}
function nbi() {
    return new BigInteger(null)
}
function am1(e, t, i, n, s, a) {
    for (; --a >= 0; ) {
        var r = t * this[e++] + i[n] + s;
        s = Math.floor(r / 67108864);
        i[n++] = 67108863 & r
    }
    return s
}
function am2(e, t, i, n, s, a) {
    var r = 32767 & t
      , o = t >> 15;
    for (; --a >= 0; ) {
        var c = 32767 & this[e];
        var d = this[e++] >> 15;
        var _ = o * c + d * r;
        c = r * c + ((32767 & _) << 15) + i[n] + (1073741823 & s);
        s = (c >>> 30) + (_ >>> 15) + o * d + (s >>> 30);
        i[n++] = 1073741823 & c
    }
    return s
}
function am3(e, t, i, n, s, a) {
    var r = 16383 & t
      , o = t >> 14;
    for (; --a >= 0; ) {
        var c = 16383 & this[e];
        var d = this[e++] >> 14;
        var _ = o * c + d * r;
        c = r * c + ((16383 & _) << 14) + i[n] + s;
        s = (c >> 28) + (_ >> 14) + o * d;
        i[n++] = 268435455 & c
    }
    return s
}
if (j_lm && "Microsoft Internet Explorer" == navigator.appName) {
    BigInteger.prototype.am = am2;
    dbits = 30
} else if (j_lm && "Netscape" != navigator.appName) {
    BigInteger.prototype.am = am1;
    dbits = 26
} else {
    BigInteger.prototype.am = am3;
    dbits = 28
}
BigInteger.prototype.DB = dbits;
BigInteger.prototype.DM = (1 << dbits) - 1;
BigInteger.prototype.DV = 1 << dbits;
var BI_FP = 52;
BigInteger.prototype.FV = Math.pow(2, BI_FP);
BigInteger.prototype.F1 = BI_FP - dbits;
BigInteger.prototype.F2 = 2 * dbits - BI_FP;
var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";
var BI_RC = new Array;
var rr, vv;
rr = "0".charCodeAt(0);
for (vv = 0; vv <= 9; ++vv)
    BI_RC[rr++] = vv;
rr = "a".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
    BI_RC[rr++] = vv;
rr = "A".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
    BI_RC[rr++] = vv;
function int2char(e) {
    return BI_RM.charAt(e)
}
function intAt(e, t) {
    var i = BI_RC[e.charCodeAt(t)];
    return null == i ? -1 : i
}
function bnpCopyTo(e) {
    for (var t = this.t - 1; t >= 0; --t)
        e[t] = this[t];
    e.t = this.t;
    e.s = this.s
}
function bnpFromInt(e) {
    this.t = 1;
    this.s = e < 0 ? -1 : 0;
    if (e > 0)
        this[0] = e;
    else if (e < -1)
        this[0] = e + DV;
    else
        this.t = 0
}
function nbv(e) {
    var t = nbi();
    t.fromInt(e);
    return t
}
function bnpFromString(e, t) {
    var i;
    if (16 == t)
        i = 4;
    else if (8 == t)
        i = 3;
    else if (256 == t)
        i = 8;
    else if (2 == t)
        i = 1;
    else if (32 == t)
        i = 5;
    else if (4 == t)
        i = 2;
    else {
        this.fromRadix(e, t);
        return
    }
    this.t = 0;
    this.s = 0;
    var n = e.length
      , s = !1
      , a = 0;
    for (; --n >= 0; ) {
        var r = 8 == i ? 255 & e[n] : intAt(e, n);
        if (!(r < 0)) {
            s = !1;
            if (0 == a)
                this[this.t++] = r;
            else if (a + i > this.DB) {
                this[this.t - 1] |= (r & (1 << this.DB - a) - 1) << a;
                this[this.t++] = r >> this.DB - a
            } else
                this[this.t - 1] |= r << a;
            a += i;
            if (a >= this.DB)
                a -= this.DB
        } else if ("-" == e.charAt(n))
            s = !0
    }
    if (8 == i && 0 != (128 & e[0])) {
        this.s = -1;
        if (a > 0)
            this[this.t - 1] |= (1 << this.DB - a) - 1 << a
    }
    this.clamp();
    if (s)
        BigInteger.ZERO.subTo(this, this)
}
function bnpClamp() {
    var e = this.s & this.DM;
    for (; this.t > 0 && this[this.t - 1] == e; )
        --this.t
}
function bnToString(e) {
    if (this.s < 0)
        return "-" + this.negate().toString(e);
    var t;
    if (16 == e)
        t = 4;
    else if (8 == e)
        t = 3;
    else if (2 == e)
        t = 1;
    else if (32 == e)
        t = 5;
    else if (4 == e)
        t = 2;
    else
        return this.toRadix(e);
    var i = (1 << t) - 1, n, s = !1, a = "", r = this.t;
    var o = this.DB - r * this.DB % t;
    if (r-- > 0) {
        if (o < this.DB && (n = this[r] >> o) > 0) {
            s = !0;
            a = int2char(n)
        }
        for (; r >= 0; ) {
            if (o < t) {
                n = (this[r] & (1 << o) - 1) << t - o;
                n |= this[--r] >> (o += this.DB - t)
            } else {
                n = this[r] >> (o -= t) & i;
                if (o <= 0) {
                    o += this.DB;
                    --r
                }
            }
            if (n > 0)
                s = !0;
            if (s)
                a += int2char(n)
        }
    }
    return s ? a : "0"
}
function bnNegate() {
    var e = nbi();
    BigInteger.ZERO.subTo(this, e);
    return e
}
function bnAbs() {
    return this.s < 0 ? this.negate() : this
}
function bnCompareTo(e) {
    var t = this.s - e.s;
    if (0 != t)
        return t;
    var i = this.t;
    t = i - e.t;
    if (0 != t)
        return this.s < 0 ? -t : t;
    for (; --i >= 0; )
        if (0 != (t = this[i] - e[i]))
            return t;
    return 0
}
function nbits(e) {
    var t = 1, i;
    if (0 != (i = e >>> 16)) {
        e = i;
        t += 16
    }
    if (0 != (i = e >> 8)) {
        e = i;
        t += 8
    }
    if (0 != (i = e >> 4)) {
        e = i;
        t += 4
    }
    if (0 != (i = e >> 2)) {
        e = i;
        t += 2
    }
    if (0 != (i = e >> 1)) {
        e = i;
        t += 1
    }
    return t
}
function bnBitLength() {
    if (this.t <= 0)
        return 0;
    else
        return this.DB * (this.t - 1) + nbits(this[this.t - 1] ^ this.s & this.DM)
}
function bnpDLShiftTo(e, t) {
    var i;
    for (i = this.t - 1; i >= 0; --i)
        t[i + e] = this[i];
    for (i = e - 1; i >= 0; --i)
        t[i] = 0;
    t.t = this.t + e;
    t.s = this.s
}
function bnpDRShiftTo(e, t) {
    for (var i = e; i < this.t; ++i)
        t[i - e] = this[i];
    t.t = Math.max(this.t - e, 0);
    t.s = this.s
}
function bnpLShiftTo(e, t) {
    var i = e % this.DB;
    var n = this.DB - i;
    var s = (1 << n) - 1;
    var a = Math.floor(e / this.DB), r = this.s << i & this.DM, o;
    for (o = this.t - 1; o >= 0; --o) {
        t[o + a + 1] = this[o] >> n | r;
        r = (this[o] & s) << i
    }
    for (o = a - 1; o >= 0; --o)
        t[o] = 0;
    t[a] = r;
    t.t = this.t + a + 1;
    t.s = this.s;
    t.clamp()
}
function bnpRShiftTo(e, t) {
    t.s = this.s;
    var i = Math.floor(e / this.DB);
    if (!(i >= this.t)) {
        var n = e % this.DB;
        var s = this.DB - n;
        var a = (1 << n) - 1;
        t[0] = this[i] >> n;
        for (var r = i + 1; r < this.t; ++r) {
            t[r - i - 1] |= (this[r] & a) << s;
            t[r - i] = this[r] >> n
        }
        if (n > 0)
            t[this.t - i - 1] |= (this.s & a) << s;
        t.t = this.t - i;
        t.clamp()
    } else
        t.t = 0
}
function bnpSubTo(e, t) {
    var i = 0
      , n = 0
      , s = Math.min(e.t, this.t);
    for (; i < s; ) {
        n += this[i] - e[i];
        t[i++] = n & this.DM;
        n >>= this.DB
    }
    if (e.t < this.t) {
        n -= e.s;
        for (; i < this.t; ) {
            n += this[i];
            t[i++] = n & this.DM;
            n >>= this.DB
        }
        n += this.s
    } else {
        n += this.s;
        for (; i < e.t; ) {
            n -= e[i];
            t[i++] = n & this.DM;
            n >>= this.DB
        }
        n -= e.s
    }
    t.s = n < 0 ? -1 : 0;
    if (n < -1)
        t[i++] = this.DV + n;
    else if (n > 0)
        t[i++] = n;
    t.t = i;
    t.clamp()
}
function bnpMultiplyTo(e, t) {
    var i = this.abs()
      , n = e.abs();
    var s = i.t;
    t.t = s + n.t;
    for (; --s >= 0; )
        t[s] = 0;
    for (s = 0; s < n.t; ++s)
        t[s + i.t] = i.am(0, n[s], t, s, 0, i.t);
    t.s = 0;
    t.clamp();
    if (this.s != e.s)
        BigInteger.ZERO.subTo(t, t)
}
function bnpSquareTo(e) {
    var t = this.abs();
    var i = e.t = 2 * t.t;
    for (; --i >= 0; )
        e[i] = 0;
    for (i = 0; i < t.t - 1; ++i) {
        var n = t.am(i, t[i], e, 2 * i, 0, 1);
        if ((e[i + t.t] += t.am(i + 1, 2 * t[i], e, 2 * i + 1, n, t.t - i - 1)) >= t.DV) {
            e[i + t.t] -= t.DV;
            e[i + t.t + 1] = 1
        }
    }
    if (e.t > 0)
        e[e.t - 1] += t.am(i, t[i], e, 2 * i, 0, 1);
    e.s = 0;
    e.clamp()
}
function bnpDivRemTo(e, t, i) {
    var n = e.abs();
    if (!(n.t <= 0)) {
        var s = this.abs();
        if (!(s.t < n.t)) {
            if (null == i)
                i = nbi();
            var a = nbi()
              , r = this.s
              , o = e.s;
            var c = this.DB - nbits(n[n.t - 1]);
            if (c > 0) {
                n.lShiftTo(c, a);
                s.lShiftTo(c, i)
            } else {
                n.copyTo(a);
                s.copyTo(i)
            }
            var d = a.t;
            var _ = a[d - 1];
            if (0 != _) {
                var f = _ * (1 << this.F1) + (d > 1 ? a[d - 2] >> this.F2 : 0);
                var h = this.FV / f
                  , l = (1 << this.F1) / f
                  , u = 1 << this.F2;
                var p = i.t
                  , m = p - d
                  , v = null == t ? nbi() : t;
                a.dlShiftTo(m, v);
                if (i.compareTo(v) >= 0) {
                    i[i.t++] = 1;
                    i.subTo(v, i)
                }
                BigInteger.ONE.dlShiftTo(d, v);
                v.subTo(a, a);
                for (; a.t < d; )
                    a[a.t++] = 0;
                for (; --m >= 0; ) {
                    var g = i[--p] == _ ? this.DM : Math.floor(i[p] * h + (i[p - 1] + u) * l);
                    if ((i[p] += a.am(0, g, i, m, 0, d)) < g) {
                        a.dlShiftTo(m, v);
                        i.subTo(v, i);
                        for (; i[p] < --g; )
                            i.subTo(v, i)
                    }
                }
                if (null != t) {
                    i.drShiftTo(d, t);
                    if (r != o)
                        BigInteger.ZERO.subTo(t, t)
                }
                i.t = d;
                i.clamp();
                if (c > 0)
                    i.rShiftTo(c, i);
                if (r < 0)
                    BigInteger.ZERO.subTo(i, i)
            }
        } else {
            if (null != t)
                t.fromInt(0);
            if (null != i)
                this.copyTo(i)
        }
    }
}
function bnMod(e) {
    var t = nbi();
    this.abs().divRemTo(e, null, t);
    if (this.s < 0 && t.compareTo(BigInteger.ZERO) > 0)
        e.subTo(t, t);
    return t
}
function Classic(e) {
    this.m = e
}
function cConvert(e) {
    if (e.s < 0 || e.compareTo(this.m) >= 0)
        return e.mod(this.m);
    else
        return e
}
function cRevert(e) {
    return e
}
function cReduce(e) {
    e.divRemTo(this.m, null, e)
}
function cMulTo(e, t, i) {
    e.multiplyTo(t, i);
    this.reduce(i)
}
function cSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
Classic.prototype.convert = cConvert;
Classic.prototype.revert = cRevert;
Classic.prototype.reduce = cReduce;
Classic.prototype.mulTo = cMulTo;
Classic.prototype.sqrTo = cSqrTo;
function bnpInvDigit() {
    if (this.t < 1)
        return 0;
    var e = this[0];
    if (0 == (1 & e))
        return 0;
    var t = 3 & e;
    t = t * (2 - (15 & e) * t) & 15;
    t = t * (2 - (255 & e) * t) & 255;
    t = t * (2 - ((65535 & e) * t & 65535)) & 65535;
    t = t * (2 - e * t % this.DV) % this.DV;
    return t > 0 ? this.DV - t : -t
}
function Montgomery(e) {
    this.m = e;
    this.mp = e.invDigit();
    this.mpl = 32767 & this.mp;
    this.mph = this.mp >> 15;
    this.um = (1 << e.DB - 15) - 1;
    this.mt2 = 2 * e.t
}
function montConvert(e) {
    var t = nbi();
    e.abs().dlShiftTo(this.m.t, t);
    t.divRemTo(this.m, null, t);
    if (e.s < 0 && t.compareTo(BigInteger.ZERO) > 0)
        this.m.subTo(t, t);
    return t
}
function montRevert(e) {
    var t = nbi();
    e.copyTo(t);
    this.reduce(t);
    return t
}
function montReduce(e) {
    for (; e.t <= this.mt2; )
        e[e.t++] = 0;
    for (var t = 0; t < this.m.t; ++t) {
        var i = 32767 & e[t];
        var n = i * this.mpl + ((i * this.mph + (e[t] >> 15) * this.mpl & this.um) << 15) & e.DM;
        i = t + this.m.t;
        e[i] += this.m.am(0, n, e, t, 0, this.m.t);
        for (; e[i] >= e.DV; ) {
            e[i] -= e.DV;
            e[++i]++
        }
    }
    e.clamp();
    e.drShiftTo(this.m.t, e);
    if (e.compareTo(this.m) >= 0)
        e.subTo(this.m, e)
}
function montSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
function montMulTo(e, t, i) {
    e.multiplyTo(t, i);
    this.reduce(i)
}
Montgomery.prototype.convert = montConvert;
Montgomery.prototype.revert = montRevert;
Montgomery.prototype.reduce = montReduce;
Montgomery.prototype.mulTo = montMulTo;
Montgomery.prototype.sqrTo = montSqrTo;
function bnpIsEven() {
    return 0 == (this.t > 0 ? 1 & this[0] : this.s)
}
function bnpExp(e, t) {
    if (e > 4294967295 || e < 1)
        return BigInteger.ONE;
    var i = nbi()
      , n = nbi()
      , s = t.convert(this)
      , a = nbits(e) - 1;
    s.copyTo(i);
    for (; --a >= 0; ) {
        t.sqrTo(i, n);
        if ((e & 1 << a) > 0)
            t.mulTo(n, s, i);
        else {
            var r = i;
            i = n;
            n = r
        }
    }
    return t.revert(i)
}
function bnModPowInt(e, t) {
    var i;
    if (e < 256 || t.isEven())
        i = new Classic(t);
    else
        i = new Montgomery(t);
    return this.exp(e, i)
}
BigInteger.prototype.copyTo = bnpCopyTo;
BigInteger.prototype.fromInt = bnpFromInt;
BigInteger.prototype.fromString = bnpFromString;
BigInteger.prototype.clamp = bnpClamp;
BigInteger.prototype.dlShiftTo = bnpDLShiftTo;
BigInteger.prototype.drShiftTo = bnpDRShiftTo;
BigInteger.prototype.lShiftTo = bnpLShiftTo;
BigInteger.prototype.rShiftTo = bnpRShiftTo;
BigInteger.prototype.subTo = bnpSubTo;
BigInteger.prototype.multiplyTo = bnpMultiplyTo;
BigInteger.prototype.squareTo = bnpSquareTo;
BigInteger.prototype.divRemTo = bnpDivRemTo;
BigInteger.prototype.invDigit = bnpInvDigit;
BigInteger.prototype.isEven = bnpIsEven;
BigInteger.prototype.exp = bnpExp;
BigInteger.prototype.toString = bnToString;
BigInteger.prototype.negate = bnNegate;
BigInteger.prototype.abs = bnAbs;
BigInteger.prototype.compareTo = bnCompareTo;
BigInteger.prototype.bitLength = bnBitLength;
BigInteger.prototype.mod = bnMod;
BigInteger.prototype.modPowInt = bnModPowInt;
BigInteger.ZERO = nbv(0);
BigInteger.ONE = nbv(1);
function bnClone() {
    var e = nbi();
    this.copyTo(e);
    return e
}
function bnIntValue() {
    if (this.s < 0) {
        if (1 == this.t)
            return this[0] - this.DV;
        else if (0 == this.t)
            return -1
    } else if (1 == this.t)
        return this[0];
    else if (0 == this.t)
        return 0;
    return (this[1] & (1 << 32 - this.DB) - 1) << this.DB | this[0]
}
function bnByteValue() {
    return 0 == this.t ? this.s : this[0] << 24 >> 24
}
function bnShortValue() {
    return 0 == this.t ? this.s : this[0] << 16 >> 16
}
function bnpChunkSize(e) {
    return Math.floor(Math.LN2 * this.DB / Math.log(e))
}
function bnSigNum() {
    if (this.s < 0)
        return -1;
    else if (this.t <= 0 || 1 == this.t && this[0] <= 0)
        return 0;
    else
        return 1
}
function bnpToRadix(e) {
    if (null == e)
        e = 10;
    if (0 == this.signum() || e < 2 || e > 36)
        return "0";
    var t = this.chunkSize(e);
    var i = Math.pow(e, t);
    var n = nbv(i)
      , s = nbi()
      , a = nbi()
      , r = "";
    this.divRemTo(n, s, a);
    for (; s.signum() > 0; ) {
        r = (i + a.intValue()).toString(e).substr(1) + r;
        s.divRemTo(n, s, a)
    }
    return a.intValue().toString(e) + r
}
function bnpFromRadix(e, t) {
    this.fromInt(0);
    if (null == t)
        t = 10;
    var i = this.chunkSize(t);
    var n = Math.pow(t, i)
      , s = !1
      , a = 0
      , r = 0;
    for (var o = 0; o < e.length; ++o) {
        var c = intAt(e, o);
        if (!(c < 0)) {
            r = t * r + c;
            if (++a >= i) {
                this.dMultiply(n);
                this.dAddOffset(r, 0);
                a = 0;
                r = 0
            }
        } else if ("-" == e.charAt(o) && 0 == this.signum())
            s = !0
    }
    if (a > 0) {
        this.dMultiply(Math.pow(t, a));
        this.dAddOffset(r, 0)
    }
    if (s)
        BigInteger.ZERO.subTo(this, this)
}
function bnpFromNumber(e, t, i) {
    if ("number" == typeof t)
        if (e < 2)
            this.fromInt(1);
        else {
            this.fromNumber(e, i);
            if (!this.testBit(e - 1))
                this.bitwiseTo(BigInteger.ONE.shiftLeft(e - 1), op_or, this);
            if (this.isEven())
                this.dAddOffset(1, 0);
            for (; !this.isProbablePrime(t); ) {
                this.dAddOffset(2, 0);
                if (this.bitLength() > e)
                    this.subTo(BigInteger.ONE.shiftLeft(e - 1), this)
            }
        }
    else {
        var n = new Array
          , s = 7 & e;
        n.length = (e >> 3) + 1;
        t.nextBytes(n);
        if (s > 0)
            n[0] &= (1 << s) - 1;
        else
            n[0] = 0;
        this.fromString(n, 256)
    }
}
function bnToByteArray() {
    var e = this.t
      , t = new Array;
    t[0] = this.s;
    var i = this.DB - e * this.DB % 8, n, s = 0;
    if (e-- > 0) {
        if (i < this.DB && (n = this[e] >> i) != (this.s & this.DM) >> i)
            t[s++] = n | this.s << this.DB - i;
        for (; e >= 0; ) {
            if (i < 8) {
                n = (this[e] & (1 << i) - 1) << 8 - i;
                n |= this[--e] >> (i += this.DB - 8)
            } else {
                n = this[e] >> (i -= 8) & 255;
                if (i <= 0) {
                    i += this.DB;
                    --e
                }
            }
            if (0 != (128 & n))
                n |= -256;
            if (0 == s && (128 & this.s) != (128 & n))
                ++s;
            if (s > 0 || n != this.s)
                t[s++] = n
        }
    }
    return t
}
function bnEquals(e) {
    return 0 == this.compareTo(e)
}
function bnMin(e) {
    return this.compareTo(e) < 0 ? this : e
}
function bnMax(e) {
    return this.compareTo(e) > 0 ? this : e
}
function bnpBitwiseTo(e, t, i) {
    var n, s, a = Math.min(e.t, this.t);
    for (n = 0; n < a; ++n)
        i[n] = t(this[n], e[n]);
    if (e.t < this.t) {
        s = e.s & this.DM;
        for (n = a; n < this.t; ++n)
            i[n] = t(this[n], s);
        i.t = this.t
    } else {
        s = this.s & this.DM;
        for (n = a; n < e.t; ++n)
            i[n] = t(s, e[n]);
        i.t = e.t
    }
    i.s = t(this.s, e.s);
    i.clamp()
}
function op_and(e, t) {
    return e & t
}
function bnAnd(e) {
    var t = nbi();
    this.bitwiseTo(e, op_and, t);
    return t
}
function op_or(e, t) {
    return e | t
}
function bnOr(e) {
    var t = nbi();
    this.bitwiseTo(e, op_or, t);
    return t
}
function op_xor(e, t) {
    return e ^ t
}
function bnXor(e) {
    var t = nbi();
    this.bitwiseTo(e, op_xor, t);
    return t
}
function op_andnot(e, t) {
    return e & ~t
}
function bnAndNot(e) {
    var t = nbi();
    this.bitwiseTo(e, op_andnot, t);
    return t
}
function bnNot() {
    var e = nbi();
    for (var t = 0; t < this.t; ++t)
        e[t] = this.DM & ~this[t];
    e.t = this.t;
    e.s = ~this.s;
    return e
}
function bnShiftLeft(e) {
    var t = nbi();
    if (e < 0)
        this.rShiftTo(-e, t);
    else
        this.lShiftTo(e, t);
    return t
}
function bnShiftRight(e) {
    var t = nbi();
    if (e < 0)
        this.lShiftTo(-e, t);
    else
        this.rShiftTo(e, t);
    return t
}
function lbit(e) {
    if (0 == e)
        return -1;
    var t = 0;
    if (0 == (65535 & e)) {
        e >>= 16;
        t += 16
    }
    if (0 == (255 & e)) {
        e >>= 8;
        t += 8
    }
    if (0 == (15 & e)) {
        e >>= 4;
        t += 4
    }
    if (0 == (3 & e)) {
        e >>= 2;
        t += 2
    }
    if (0 == (1 & e))
        ++t;
    return t
}
function bnGetLowestSetBit() {
    for (var e = 0; e < this.t; ++e)
        if (0 != this[e])
            return e * this.DB + lbit(this[e]);
    if (this.s < 0)
        return this.t * this.DB;
    else
        return -1
}
function cbit(e) {
    var t = 0;
    for (; 0 != e; ) {
        e &= e - 1;
        ++t
    }
    return t
}
function bnBitCount() {
    var e = 0
      , t = this.s & this.DM;
    for (var i = 0; i < this.t; ++i)
        e += cbit(this[i] ^ t);
    return e
}
function bnTestBit(e) {
    var t = Math.floor(e / this.DB);
    if (t >= this.t)
        return 0 != this.s;
    else
        return 0 != (this[t] & 1 << e % this.DB)
}
function bnpChangeBit(e, t) {
    var i = BigInteger.ONE.shiftLeft(e);
    this.bitwiseTo(i, t, i);
    return i
}
function bnSetBit(e) {
    return this.changeBit(e, op_or)
}
function bnClearBit(e) {
    return this.changeBit(e, op_andnot)
}
function bnFlipBit(e) {
    return this.changeBit(e, op_xor)
}
function bnpAddTo(e, t) {
    var i = 0
      , n = 0
      , s = Math.min(e.t, this.t);
    for (; i < s; ) {
        n += this[i] + e[i];
        t[i++] = n & this.DM;
        n >>= this.DB
    }
    if (e.t < this.t) {
        n += e.s;
        for (; i < this.t; ) {
            n += this[i];
            t[i++] = n & this.DM;
            n >>= this.DB
        }
        n += this.s
    } else {
        n += this.s;
        for (; i < e.t; ) {
            n += e[i];
            t[i++] = n & this.DM;
            n >>= this.DB
        }
        n += e.s
    }
    t.s = n < 0 ? -1 : 0;
    if (n > 0)
        t[i++] = n;
    else if (n < -1)
        t[i++] = this.DV + n;
    t.t = i;
    t.clamp()
}
function bnAdd(e) {
    var t = nbi();
    this.addTo(e, t);
    return t
}
function bnSubtract(e) {
    var t = nbi();
    this.subTo(e, t);
    return t
}
function bnMultiply(e) {
    var t = nbi();
    this.multiplyTo(e, t);
    return t
}
function bnSquare() {
    var e = nbi();
    this.squareTo(e);
    return e
}
function bnDivide(e) {
    var t = nbi();
    this.divRemTo(e, t, null);
    return t
}
function bnRemainder(e) {
    var t = nbi();
    this.divRemTo(e, null, t);
    return t
}
function bnDivideAndRemainder(e) {
    var t = nbi()
      , i = nbi();
    this.divRemTo(e, t, i);
    return new Array(t,i)
}
function bnpDMultiply(e) {
    this[this.t] = this.am(0, e - 1, this, 0, 0, this.t);
    ++this.t;
    this.clamp()
}
function bnpDAddOffset(e, t) {
    if (0 != e) {
        for (; this.t <= t; )
            this[this.t++] = 0;
        this[t] += e;
        for (; this[t] >= this.DV; ) {
            this[t] -= this.DV;
            if (++t >= this.t)
                this[this.t++] = 0;
            ++this[t]
        }
    }
}
function NullExp() {}
function nNop(e) {
    return e
}
function nMulTo(e, t, i) {
    e.multiplyTo(t, i)
}
function nSqrTo(e, t) {
    e.squareTo(t)
}
NullExp.prototype.convert = nNop;
NullExp.prototype.revert = nNop;
NullExp.prototype.mulTo = nMulTo;
NullExp.prototype.sqrTo = nSqrTo;
function bnPow(e) {
    return this.exp(e, new NullExp)
}
function bnpMultiplyLowerTo(e, t, i) {
    var n = Math.min(this.t + e.t, t);
    i.s = 0;
    i.t = n;
    for (; n > 0; )
        i[--n] = 0;
    var s;
    for (s = i.t - this.t; n < s; ++n)
        i[n + this.t] = this.am(0, e[n], i, n, 0, this.t);
    for (s = Math.min(e.t, t); n < s; ++n)
        this.am(0, e[n], i, n, 0, t - n);
    i.clamp()
}
function bnpMultiplyUpperTo(e, t, i) {
    --t;
    var n = i.t = this.t + e.t - t;
    i.s = 0;
    for (; --n >= 0; )
        i[n] = 0;
    for (n = Math.max(t - this.t, 0); n < e.t; ++n)
        i[this.t + n - t] = this.am(t - n, e[n], i, 0, 0, this.t + n - t);
    i.clamp();
    i.drShiftTo(1, i)
}
function Barrett(e) {
    this.r2 = nbi();
    this.q3 = nbi();
    BigInteger.ONE.dlShiftTo(2 * e.t, this.r2);
    this.mu = this.r2.divide(e);
    this.m = e
}
function barrettConvert(e) {
    if (e.s < 0 || e.t > 2 * this.m.t)
        return e.mod(this.m);
    else if (e.compareTo(this.m) < 0)
        return e;
    else {
        var t = nbi();
        e.copyTo(t);
        this.reduce(t);
        return t
    }
}
function barrettRevert(e) {
    return e
}
function barrettReduce(e) {
    e.drShiftTo(this.m.t - 1, this.r2);
    if (e.t > this.m.t + 1) {
        e.t = this.m.t + 1;
        e.clamp()
    }
    this.mu.multiplyUpperTo(this.r2, this.m.t + 1, this.q3);
    this.m.multiplyLowerTo(this.q3, this.m.t + 1, this.r2);
    for (; e.compareTo(this.r2) < 0; )
        e.dAddOffset(1, this.m.t + 1);
    e.subTo(this.r2, e);
    for (; e.compareTo(this.m) >= 0; )
        e.subTo(this.m, e)
}
function barrettSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
function barrettMulTo(e, t, i) {
    e.multiplyTo(t, i);
    this.reduce(i)
}
Barrett.prototype.convert = barrettConvert;
Barrett.prototype.revert = barrettRevert;
Barrett.prototype.reduce = barrettReduce;
Barrett.prototype.mulTo = barrettMulTo;
Barrett.prototype.sqrTo = barrettSqrTo;
function bnModPow(e, t) {
    var i = e.bitLength(), n, s = nbv(1), a;
    if (i <= 0)
        return s;
    else if (i < 18)
        n = 1;
    else if (i < 48)
        n = 3;
    else if (i < 144)
        n = 4;
    else if (i < 768)
        n = 5;
    else
        n = 6;
    if (i < 8)
        a = new Classic(t);
    else if (t.isEven())
        a = new Barrett(t);
    else
        a = new Montgomery(t);
    var r = new Array
      , o = 3
      , c = n - 1
      , d = (1 << n) - 1;
    r[1] = a.convert(this);
    if (n > 1) {
        var _ = nbi();
        a.sqrTo(r[1], _);
        for (; o <= d; ) {
            r[o] = nbi();
            a.mulTo(_, r[o - 2], r[o]);
            o += 2
        }
    }
    var f = e.t - 1, h, l = !0, u = nbi(), p;
    i = nbits(e[f]) - 1;
    for (; f >= 0; ) {
        if (i >= c)
            h = e[f] >> i - c & d;
        else {
            h = (e[f] & (1 << i + 1) - 1) << c - i;
            if (f > 0)
                h |= e[f - 1] >> this.DB + i - c
        }
        o = n;
        for (; 0 == (1 & h); ) {
            h >>= 1;
            --o
        }
        if ((i -= o) < 0) {
            i += this.DB;
            --f
        }
        if (l) {
            r[h].copyTo(s);
            l = !1
        } else {
            for (; o > 1; ) {
                a.sqrTo(s, u);
                a.sqrTo(u, s);
                o -= 2
            }
            if (o > 0)
                a.sqrTo(s, u);
            else {
                p = s;
                s = u;
                u = p
            }
            a.mulTo(u, r[h], s)
        }
        for (; f >= 0 && 0 == (e[f] & 1 << i); ) {
            a.sqrTo(s, u);
            p = s;
            s = u;
            u = p;
            if (--i < 0) {
                i = this.DB - 1;
                --f
            }
        }
    }
    return a.revert(s)
}
function bnGCD(e) {
    var t = this.s < 0 ? this.negate() : this.clone();
    var i = e.s < 0 ? e.negate() : e.clone();
    if (t.compareTo(i) < 0) {
        var n = t;
        t = i;
        i = n
    }
    var s = t.getLowestSetBit()
      , a = i.getLowestSetBit();
    if (a < 0)
        return t;
    if (s < a)
        a = s;
    if (a > 0) {
        t.rShiftTo(a, t);
        i.rShiftTo(a, i)
    }
    for (; t.signum() > 0; ) {
        if ((s = t.getLowestSetBit()) > 0)
            t.rShiftTo(s, t);
        if ((s = i.getLowestSetBit()) > 0)
            i.rShiftTo(s, i);
        if (t.compareTo(i) >= 0) {
            t.subTo(i, t);
            t.rShiftTo(1, t)
        } else {
            i.subTo(t, i);
            i.rShiftTo(1, i)
        }
    }
    if (a > 0)
        i.lShiftTo(a, i);
    return i
}
function bnpModInt(e) {
    if (e <= 0)
        return 0;
    var t = this.DV % e
      , i = this.s < 0 ? e - 1 : 0;
    if (this.t > 0)
        if (0 == t)
            i = this[0] % e;
        else
            for (var n = this.t - 1; n >= 0; --n)
                i = (t * i + this[n]) % e;
    return i
}
function bnModInverse(e) {
    var t = e.isEven();
    if (this.isEven() && t || 0 == e.signum())
        return BigInteger.ZERO;
    var i = e.clone()
      , n = this.clone();
    var s = nbv(1)
      , a = nbv(0)
      , r = nbv(0)
      , o = nbv(1);
    for (; 0 != i.signum(); ) {
        for (; i.isEven(); ) {
            i.rShiftTo(1, i);
            if (t) {
                if (!s.isEven() || !a.isEven()) {
                    s.addTo(this, s);
                    a.subTo(e, a)
                }
                s.rShiftTo(1, s)
            } else if (!a.isEven())
                a.subTo(e, a);
            a.rShiftTo(1, a)
        }
        for (; n.isEven(); ) {
            n.rShiftTo(1, n);
            if (t) {
                if (!r.isEven() || !o.isEven()) {
                    r.addTo(this, r);
                    o.subTo(e, o)
                }
                r.rShiftTo(1, r)
            } else if (!o.isEven())
                o.subTo(e, o);
            o.rShiftTo(1, o)
        }
        if (i.compareTo(n) >= 0) {
            i.subTo(n, i);
            if (t)
                s.subTo(r, s);
            a.subTo(o, a)
        } else {
            n.subTo(i, n);
            if (t)
                r.subTo(s, r);
            o.subTo(a, o)
        }
    }
    if (0 != n.compareTo(BigInteger.ONE))
        return BigInteger.ZERO;
    if (o.compareTo(e) >= 0)
        return o.subtract(e);
    if (o.signum() < 0)
        o.addTo(e, o);
    else
        return o;
    if (o.signum() < 0)
        return o.add(e);
    else
        return o
}
var lowprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997];
var lplim = (1 << 26) / lowprimes[lowprimes.length - 1];
function bnIsProbablePrime(e) {
    var t, i = this.abs();
    if (1 == i.t && i[0] <= lowprimes[lowprimes.length - 1]) {
        for (t = 0; t < lowprimes.length; ++t)
            if (i[0] == lowprimes[t])
                return !0;
        return !1
    }
    if (i.isEven())
        return !1;
    t = 1;
    for (; t < lowprimes.length; ) {
        var n = lowprimes[t]
          , s = t + 1;
        for (; s < lowprimes.length && n < lplim; )
            n *= lowprimes[s++];
        n = i.modInt(n);
        for (; t < s; )
            if (n % lowprimes[t++] == 0)
                return !1
    }
    return i.millerRabin(e)
}
function bnpMillerRabin(e) {
    var t = this.subtract(BigInteger.ONE);
    var i = t.getLowestSetBit();
    if (i <= 0)
        return !1;
    var n = t.shiftRight(i);
    e = e + 1 >> 1;
    if (e > lowprimes.length)
        e = lowprimes.length;
    var s = nbi();
    for (var a = 0; a < e; ++a) {
        s.fromInt(lowprimes[Math.floor(Math.random() * lowprimes.length)]);
        var r = s.modPow(n, this);
        if (0 != r.compareTo(BigInteger.ONE) && 0 != r.compareTo(t)) {
            var o = 1;
            for (; o++ < i && 0 != r.compareTo(t); ) {
                r = r.modPowInt(2, this);
                if (0 == r.compareTo(BigInteger.ONE))
                    return !1
            }
            if (0 != r.compareTo(t))
                return !1
        }
    }
    return !0
}
BigInteger.prototype.chunkSize = bnpChunkSize;
BigInteger.prototype.toRadix = bnpToRadix;
BigInteger.prototype.fromRadix = bnpFromRadix;
BigInteger.prototype.fromNumber = bnpFromNumber;
BigInteger.prototype.bitwiseTo = bnpBitwiseTo;
BigInteger.prototype.changeBit = bnpChangeBit;
BigInteger.prototype.addTo = bnpAddTo;
BigInteger.prototype.dMultiply = bnpDMultiply;
BigInteger.prototype.dAddOffset = bnpDAddOffset;
BigInteger.prototype.multiplyLowerTo = bnpMultiplyLowerTo;
BigInteger.prototype.multiplyUpperTo = bnpMultiplyUpperTo;
BigInteger.prototype.modInt = bnpModInt;
BigInteger.prototype.millerRabin = bnpMillerRabin;
BigInteger.prototype.clone = bnClone;
BigInteger.prototype.intValue = bnIntValue;
BigInteger.prototype.byteValue = bnByteValue;
BigInteger.prototype.shortValue = bnShortValue;
BigInteger.prototype.signum = bnSigNum;
BigInteger.prototype.toByteArray = bnToByteArray;
BigInteger.prototype.equals = bnEquals;
BigInteger.prototype.min = bnMin;
BigInteger.prototype.max = bnMax;
BigInteger.prototype.and = bnAnd;
BigInteger.prototype.or = bnOr;
BigInteger.prototype.xor = bnXor;
BigInteger.prototype.andNot = bnAndNot;
BigInteger.prototype.not = bnNot;
BigInteger.prototype.shiftLeft = bnShiftLeft;
BigInteger.prototype.shiftRight = bnShiftRight;
BigInteger.prototype.getLowestSetBit = bnGetLowestSetBit;
BigInteger.prototype.bitCount = bnBitCount;
BigInteger.prototype.testBit = bnTestBit;
BigInteger.prototype.setBit = bnSetBit;
BigInteger.prototype.clearBit = bnClearBit;
BigInteger.prototype.flipBit = bnFlipBit;
BigInteger.prototype.add = bnAdd;
BigInteger.prototype.subtract = bnSubtract;
BigInteger.prototype.multiply = bnMultiply;
BigInteger.prototype.divide = bnDivide;
BigInteger.prototype.remainder = bnRemainder;
BigInteger.prototype.divideAndRemainder = bnDivideAndRemainder;
BigInteger.prototype.modPow = bnModPow;
BigInteger.prototype.modInverse = bnModInverse;
BigInteger.prototype.pow = bnPow;
BigInteger.prototype.gcd = bnGCD;
BigInteger.prototype.isProbablePrime = bnIsProbablePrime;
BigInteger.prototype.square = bnSquare;

var RSAPublicKey = function(e, t) {
    this.modulus = new BigInteger(Hex.encode(e),16);
    this.encryptionExponent = new BigInteger(Hex.encode(t),16)
};

var Base64 = {
    base64: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(e) {
        if (!e)
            return !1;
        var t = "";
        var i, n, s;
        var a, r, o, c;
        var d = 0;
        do {
            i = e.charCodeAt(d++);
            n = e.charCodeAt(d++);
            s = e.charCodeAt(d++);
            a = i >> 2;
            r = (3 & i) << 4 | n >> 4;
            o = (15 & n) << 2 | s >> 6;
            c = 63 & s;
            if (isNaN(n))
                o = c = 64;
            else if (isNaN(s))
                c = 64;
            t += this.base64.charAt(a) + this.base64.charAt(r) + this.base64.charAt(o) + this.base64.charAt(c)
        } while (d < e.length);return t
    },
    decode: function(e) {
        if (!e)
            return !1;
        e = e.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        var t = "";
        var i, n, s, a;
        var r = 0;
        do {
            i = this.base64.indexOf(e.charAt(r++));
            n = this.base64.indexOf(e.charAt(r++));
            s = this.base64.indexOf(e.charAt(r++));
            a = this.base64.indexOf(e.charAt(r++));
            t += String.fromCharCode(i << 2 | n >> 4);
            if (64 != s)
                t += String.fromCharCode((15 & n) << 4 | s >> 2);
            if (64 != a)
                t += String.fromCharCode((3 & s) << 6 | a)
        } while (r < e.length);return t
    }
};

var ASN1Data = function(e) {
    this.error = !1;
    this.parse = function(e) {
        if (!e) {
            this.error = !0;
            return null
        }
        var t = [];
        for (; e.length > 0; ) {
            var i = e.charCodeAt(0);
            e = e.substr(1);
            var n = 0;
            if (5 == (31 & i))
                e = e.substr(1);
            else if (128 & e.charCodeAt(0)) {
                var s = 127 & e.charCodeAt(0);
                e = e.substr(1);
                if (s > 0)
                    n = e.charCodeAt(0);
                if (s > 1)
                    n = n << 8 | e.charCodeAt(1);
                if (s > 2) {
                    this.error = !0;
                    return null
                }
                e = e.substr(s)
            } else {
                n = e.charCodeAt(0);
                e = e.substr(1)
            }
            var a = "";
            if (n) {
                if (n > e.length) {
                    this.error = !0;
                    return null
                }
                a = e.substr(0, n);
                e = e.substr(n)
            }
            if (32 & i)
                t.push(this.parse(a));
            else
                t.push(this.value(128 & i ? 4 : 31 & i, a))
        }
        return t
    }
    ;
    this.value = function(e, t) {
        if (1 == e)
            return t ? !0 : !1;
        else if (2 == e)
            return t;
        else if (3 == e)
            return this.parse(t.substr(1));
        else if (5 == e)
            return null;
        else if (6 == e) {
            var i = [];
            var n = t.charCodeAt(0);
            i.push(Math.floor(n / 40));
            i.push(n - 40 * i[0]);
            var s = [];
            var a = 0;
            var r;
            for (r = 1; r < t.length; r++) {
                var o = t.charCodeAt(r);
                s.push(127 & o);
                if (128 & o)
                    a++;
                else {
                    var c;
                    var d = 0;
                    for (c = 0; c < s.length; c++)
                        d += s[c] * Math.pow(128, a--);
                    i.push(d);
                    a = 0;
                    s = []
                }
            }
            return i.join(".")
        }
        return null
    }
    ;
    this.data = this.parse(e)
};

var RSA = {
    getPublicKey: function(e) {
        if (e.length < 50)
            return !1;
        if ("-----BEGIN PUBLIC KEY-----" != e.substr(0, 26))
            return !1;
        e = e.substr(26);
        if ("-----END PUBLIC KEY-----" != e.substr(e.length - 24))
            return !1;
        e = e.substr(0, e.length - 24);
        e = new ASN1Data(Base64.decode(e));
        if (e.error)
            return !1;
        e = e.data;
        if ("1.2.840.113549.1.1.1" == e[0][0][0])
            return new RSAPublicKey(e[0][1][0][0],e[0][1][0][1]);
        else
            return !1
    },
    encrypt: function(e, t) {
        if (!t)
            return !1;
        var i = t.modulus.bitLength() + 7 >> 3;
        e = this.pkcs1pad2(e, i);
        if (!e)
            return !1;
        e = e.modPowInt(t.encryptionExponent, t.modulus);
        if (!e)
            return !1;
        e = e.toString(16);
        for (; e.length < 2 * i; )
            e = "0" + e;
        return Base64.encode(Hex.decode(e))
    },
    decrypt: function(e) {
        var t = new BigInteger(e,16)
    },
    pkcs1pad2: function(e, t) {
        if (t < e.length + 11)
            return null;
        var i = [];
        var n = e.length - 1;
        for (; n >= 0 && t > 0; )
            i[--t] = e.charCodeAt(n--);
        i[--t] = 0;
        for (; t > 2; )
            i[--t] = Math.floor(254 * Math.random()) + 1;
        i[--t] = 2;
        i[--t] = 0;
        return new BigInteger(i)
    }
};

function encrypt2(e, key) {
var t = RSA.getPublicKey(key);
return RSA.encrypt(e, t)
};
    """
    ctx = execjs.compile(command)
    return ctx.call("encrypt2", '88888888',
                    "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB-----END PUBLIC KEY-----")


def eval_func():
    import execjs

    return execjs.eval("""1+1""")


def with_params_one(url):
    command = """
    function url (){
        %s
        return url;
    };
    """ % url
    ctx = execjs.compile(command)
    return ctx.call("url")


if __name__ == '__main__':
    # print(with_params())
    print(with_params())
