# sftppy
Copy file form Windows to Linux system by Python script

How to use
- Generate Pubkey and private key first
- Read config in python file

**Generate Pubkey and private key**
- Download puttyGen >> https://www.puttygen.com/
- Generate and save public key, private key
- Open up Linux system
- Following command
  - cd ~/.ssh
  - nano authorized_keys
  - Back in the shell type echo "pasted-public-key-from-windows" > authorized_keys
  - chmod 600 ~/.ssh/authorized_keys
  - If you need to know pubkey of Ubuntu host use this command >> ssh-keyscan "hostname"
  
  
