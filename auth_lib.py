from cryptography.hazmat.primitives.hashes import Hash, BLAKE2b
import os

def secure_hash(msg: str, salt: str):
  hash = Hash(algorithm=BLAKE2b(digest_size=64))
  msg_with_salt = salt + msg 
  hash.update(msg_with_salt.encode())
  digested_msg = hash.finalize()
  return digested_msg.hex()

def generate_salt():
  return os.urandom(16).hex()
