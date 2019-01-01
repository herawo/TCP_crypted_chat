# TCP_crypted_chat

TCP_crypted_chat

## Requirements

- python 3.6
- pip
- virtulenv
- more than 2 brain cells

## Installation
```
git clone https://github.com/herawo/TCP_crypted_chat
cd TCP_crypted_chat
virtualenv venv
source venv/bin/activate
pip install requirements.txt
```

## Usage

For simple usage 
`./TCP_client.py X.X.X.X my_pseudo`

For usage with the ability to use AES
`./TCP_client.py X.X.X.X my_pseudo my_passphrase`

Write your messages prefixed by "[AES]" to make it encrypted

For only AES usage
`./TCP_client.py X.X.X.X my_pseudo my_passphrase -c`

> note : the last one will automatically crash because the server send un-crypted messages :(
