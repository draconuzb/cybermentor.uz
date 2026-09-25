import base64

a1_b64 = "8XUCieZ6cewjgneCoC0aeuKvvQE1QUU4lD2v4pGO9atX9r/YrtC+rbhXjeBmZppLipd+8c7mt8gWn3IOLVq1zQNZRfT/mUv4F3khZtqEaIHQUDuI0KmV2jCJtN4uBmLm7Pt3/ipz1HnIXcPWilT7/bD5GamaKGeb2rOp7MKA9/ZHbR09ztEJutdDL4SLMbp2nC5g6lZMp+t3INREsq7d/g=="
a2_b64 = "638Y4OJ9a5g3hH7usEJxfvfD1AFBQ0U3oBGdoZqjis5C3N6Z2pLV0ohg/cgVdqwy/KMRkM7lvMQK83YGJj/A1wJIWPTpmUjjF2JYFceLb5O8PS2P0a2c2EThtL9AYmKVmJoZmkgK1B+nL8Oi+DWdm9maGcT7QQnvu9rH7LH0hZ8kGR1Pr7Vg1dcwRujuX9kTnFsOnj8gp40CUqAs19zdkA=="

a1 = base64.b64decode(a1_b64)
a2 = base64.b64decode(a2_b64)
print("len a1:", len(a1), "len a2:", len(a2))

crib = b"NET CONTROL TO ALL STATIONS THIS IS A ROUTINE RADIO CHECK ALL UNITS REPORT SIGNAL STRENGTH AND STANDBY FOR TRAFFIC MAINTAIN STRICT RADIO SILENCE UNTIL FURTHER NOTICE"
print("crib len:", len(crib))

padded_crib = crib + b" " * (len(a1) - len(crib))
keystream = bytes(a ^ b for a, b in zip(a1, padded_crib))

pt2 = bytes(c ^ k for c, k in zip(a2, keystream))
print("A2 plaintext:", pt2)
