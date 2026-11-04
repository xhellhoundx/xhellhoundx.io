#!/usr/bin/env python3

import base64 as b64


key = b'-VkgXhFf6sAEcAwrC6YR-SZbiuSb8ABXeQuvhcGSQzY='
key_str = key.decode()
decoded = b64.urlsafe_b64decode(key_str)

print(decoded.hex())
