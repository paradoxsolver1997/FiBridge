@echo off
REM Generate self-signed certificate key.pem and cert.pem
openssl genrsa -out key.pem 2048
openssl req -new -key key.pem -out cert.csr
openssl x509 -req -days 365 -in cert.csr -signkey key.pem -out cert.pem

del cert.csr

echo Certificates generated: key.pem, cert.pem
pause
