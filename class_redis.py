import redis
# r is the class instance

r = redis.Redis()
# return is bytes not string
# print(r.mset({'pranav':'banglore','grey':'denM'}))
# print(type(r.get('pranav'))) #class bytes
# print(type(r.get('pranav').decode("utf-8"))) #it helps to convert string

# print(r.get('pranav').decode("utf-8"))

# print(r.ping())
# print(r.hgetall('pranav'))
# One thing that’s worth knowing is that redis-py requires that you pass it
#  keys that are bytes, str, int, or float.
#  (It will convert the last 3 of these types to bytes before sending them 
#  off to the server.)

import datetime

today = datetime.date.today()
# print('Hello',type(today))
visitors= {"tintu","soman","sasi"}
# print(r.sadd(today, *visitors))
stoday = today.isoformat()
# print(type(stoday))
# print('date',stoday)

# print(r.sadd(stoday, *visitors))
# print(r.smembers(stoday))

a = r.smembers(stoday)
# print(type(a))

# print(r.scard(today.isoformat()))

import random

hats = {f"hat:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,  
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    },
    {
        "shop": "NPS",
        "year": 1986,
        "style": "software",
        "staffs": 6,
        "npurchased": 1984,
    
})
}
# print(hats)
r = redis.Redis(db=1)
# print(r.__dict__)
# assert(isinstance, r, redis.client.Redis)
# then i think it will be use like r.____ because its a class method 
# print(r.ping)
with r.pipeline() as pipe:
    for h_id, hat in hats.items():
        print(h_id, hat)
        # pipe.hmset(h_id, hat)
    print(pipe.execute())

# print(r.bgsave())
import pprint as _
    
# _.pprint(r.hgetall("hat:2374350161"))
_.pprint(r.hgetall("hat:347882626"))
# _.pprint(r.hgetall("hat:3036312521"))
# _.pprint(r.hgetall("hat:1310202501"))
# _.pprint(r.keys())

"""
The first thing that we want to simulate is what happens when a user clicks Purchase.
If the item is in stock, increase its npurchased by 1 and decrease its quantity 
(inventory) by 1. You can use .hincrby() to do this:
"""

# print(r.hincrby("hat:347882626", "quantity", -5))
# _.pprint(r.hget("hat:347882626", "quantity"))
# budg1 = r.hget("hat:347882626", "quantity")
# print(type(budg1))
# convert to string
# bt_str = budg1.decode("utf-8")
# print(type(bt_str))
# print(bt_str)

# decreasing purchase
# r.hincrby("hat:347882626", "npurchased", -100)
# increasing purchse
r.hincrby("hat:347882626", "npurchased", '1000')

new_purchase = r.hget("hat:347882626","npurchased")
print(new_purchase)
new_purchase_str = new_purchase.decode("utf-8")

# _.pprint(r.hgetall("hat:347882626"))
# assert(type(new_purchase), int)

# _.pprint(type(hats))

# find a particular shop name in hats:
# for c, d in hats.items():
#     for x in d:
#         if x == 'shop':
#             print('shop catched:',d)

"""
Step 1: Check if the item is in stock, or otherwise raise an exception on the backend.
Step 2: If it is in stock, then execute the transaction, decrease the quantity field, and increase the npurchased field.
Step 3: Be alert for any changes that alter the inventory in between the first two steps (a race condition).
"""

# In Redis, a transaction starts with MULTI and ends with EXEC:

# 127.0.0.1:6379> MULTI
# 127.0.0.1:6379> HINCRBY 56854717 quantity -1
# 127.0.0.1:6379> HINCRBY 56854717 npurchased 1
# 127.0.0.1:6379> EXEC

import logging

logging.basicConfig()

class OutOfStockError(Exception):
    """Raised when pyHats.com is all out of today's hottest Hat."""
    pass

def buyitem(r: redis.Redis, itemid: int) -> None:
    with r.pipeline() as pipe:
        error_count = 0
        while True:
            try:
                # Get available inventory, watching for changes
                # related to this itemid before the transaction
                pipe.watch(itemid)
                nleft: bytes = r.hget(itemid, "quantity")
                print(nleft)
                if nleft > b"0":
                    pipe.multi()
                    # some one who buy product quantity will decrement,
                    # And purchased will b increase.
                    pipe.hincrby(itemid, "quantity", -1)
                    pipe.hincrby(itemid, "npurchased", 1)
                    pipe.execute()
                    break
                else:
                    # stop watching the itemid and raise to break out
                    pipe.unwatch()
                    raise OutOfStockError(
                        f"{itemid} out of stock!"
                    )
            except redis.WatchError:
                # Log total num. of errors by this user to buy this item,
                # then try the same process again of WATCH/HGET/MULTI/EXEC
                error_count+=1
                logging.warning(
                    "WatchError #%d: %s; retrying",
                    error_count, itemid
                )
    return None

# buyitem(r, "hat:347882626")

# print(r.hmget("hat:347882626", "quantity", "npurchased"))
# print(r.hgetall("hat:347882626"))
# # r.hincrby("hat:347882626", "quantity", 2000)
# print(r.hgetall("hat:347882626"))
# buyitem(r, "hat:347882626")
# print(r.hgetall("hat:347882626"))

# for _ in range(4000):
#     buyitem(r, "hat:347882626")
# print(r.hmget("hat:347882626", "quantity", "npurchased"))

# Using Key Expiry
from datetime import timedelta

# setex: "SET" with expiration
r.setex("runner", timedelta(minutes=1), value="now you see me")

print("minutes:",r.ttl("runner")) #show in minutes
print("milliseconds", r.pttl("runner"))

print(r.get("runner"))
print(r.expire("runner", timedelta(seconds=3)))
print(r.exists("runner"))

r = redis.Redis(db=5)
r.lpush("ips", "51.218.112.236")
r.lpush("ips", "90.213.45.98")
r.lpush("ips", "115.215.230.176")
req = r.lpush("ips", "51.218.112.236")
print(req,type(req))



"""
while True loop and does a blocking left-pop 
BLPOP call on the ips list, processing each address:
"""
print(r.expire("runner",timedelta(seconds=3)))
print(r.time())

from datetime import datetime

print(r.time()[0])

print(datetime.utcfromtimestamp(r.time()[0]).strftime('%Y-%m-%d %H:%M:%S'))

# New shell window or tab

for x in range(1,15):
    print(r.lpush("ips", "51.218.112.236"))

# import datetime
# import ipaddress

# import redis

# # Where we put all the bad egg IP addresses
# blacklist = set()
# MAXVISITS = 15

# ipwatcher = redis.Redis(db=5)

# while True:
#     _, addr = ipwatcher.blpop("ips")
#     addr = ipaddress.ip_address(addr.decode("utf-8"))
#     now = datetime.datetime.utcnow()
#     addrts = f"{addr}:{now.minute}"
#     n = ipwatcher.incrby(addrts, 1)
#     if n >= MAXVISITS:
#         print(f'Hat bot detected: {addr}')
#         blacklist.add(addr)
#     else:
#         print(f"{now}: saw {addr}")
#     _ = ipwatcher.expire(addrts, 60)

# print(f'blacklist : {blacklist}')

print(r.lastsave())

r.hset("mykey", "field1", "value1")
restaurant_484272 = {
    "name": "Ravagh",
    "type": "Persian",
    "address": {
        "street": {
            "line1": "11 E 30th St",
            "line2": "APT 1",
        },
        "city": "New York",
        "state": "NY",
        "zip": 10016,
    }
}

import json
r.set(484272, json.dumps(restaurant_484272))

_.pprint(json.loads(r.get(484272)))

# _.pprint(yaml.dump(restaurant_484272))

# We want to get it into this form:

# {
#     "484272:name":                     "Ravagh",
#     "484272:type":                     "Persian",
#     "484272:address:street:line1":     "11 E 30th St",
#     "484272:address:street:line2":     "APT 1",
#     "484272:address:city":             "New York",
#     "484272:address:state":            "NY",
#     "484272:address:zip":              "10016",
# }

from collections.abc import MutableMapping

def setflat_skeys(
    r: redis.Redis,
    obj: dict,
    prefix: str,
    delim: str = ":",
    *,
    _autofix=""
) -> None:
    allowed_types = (str, bytes, float, int)
    for key, value in obj.items():
        key = _autofix + key
        if isinstance(value, allowed_types):
            r.set(f'{prefix}{delim}{key}', value)
        elif isinstance(value, MutableMapping):
            setflat_skeys(
                r, value, prefix, delim, _autofix=f"{key}{delim}"
            )
        else:
            raise TypeError(f"Unsupported value type :", {type(value)})

# r.flushdb()
setflat_skeys(r, restaurant_484272, 484272)
for key in sorted(r.keys("484272*")):
    print(f"{repr(key):35}{repr(r.get(key)):15}")
print(r.get("484272:address:zip"))
"""
$ python -m pip install cryptography
To illustrate, pretend that you have some sensitive cardholder data (CD)
that you never want to have sitting around in plaintext on any server,
no matter what. Before 
caching it in Redis, you can serialize the data and then encrypt the 
serialized string using Fernet:
"""

import json
from cryptography.fernet import Fernet

cipher = Fernet(Fernet.generate_key())
info = {
    "cardnum": 22132323232344,
    "exp": [2020, 9],
    "cv2": 842,
}

r.set(
    "user:1000",
    cipher.encrypt(json.dumps(info).encode('utf-8'))
)

print(r.get('user:1000'))

print(cipher.decrypt(r.get('user:1000')))
print(json.loads(cipher.decrypt(r.get('user:1000'))))

"""
Compression
One last quick optimization is compression. If bandwidth is a 
concern or you’re cost-conscious, you can implement a lossless 
compression and decompression scheme when you send and receive
data from Redis. Here’s an example using the bzip2 compression
algorithm, which in this extreme case cuts down on
the number of bytes sent across the connection by a factor of 
over 2,000:
"""

import bz2

blob = "i have a lot to talk about" * 10000
len(blob.encode("utf-8"))

r.set("msg:500", bz2.compress(blob.encode("utf-8")))
print(r.get("msg:500"))
print(len(r.get("msg:500")))

# 260_000 / 122  # Magnitude of savings
# 2131.1475409836066

# Get and decompress the value, then confirm it's equal
#  to the original

rblob = bz2.decompress(r.get("msg:500")).decode("utf-8")
print(rblob==blob)

"""
What you’re actually installing here is hiredis-py, which is 
a Python wrapper for a portion of the hiredis C library.

The nice thing is that you don’t really need to call hiredis 
yourself. Just pip install it, and this will let 
redis-py see that it’s available and use its HiredisParser
 instead of PythonParser.

Internally, redis-py will attempt to import hiredis, and use a
 HiredisParser class to match it, but will fall back to its
  PythonParser instead, which may be slower in some cases:
"""
# utils.py
# redis/utils.py
try:
    import hiredis
    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False


# # redis/connection.py
# if HIREDIS_AVAILABLE:
#     DefaultParser = HiredisParser
# else:
#     DefaultParser = PythonParser

