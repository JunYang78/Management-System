from flask import Flask, render_template, request
from cryptography.fernet import Fernet

app = Flask(__name__)

@app.route('/') #Render html page
def index():
    return render_template('index.html')

@app.route('/encryptor', methods=['GET', 'POST'])
def encryptor():
    usertext=""
    password=""
    encText=""
    if request.method == 'POST':
        password = request.form['password']
        usertext = request.form['usertext']
        if usertext and password != "":
            encText = textEncryption(usertext,password).decode('utf-8')

        return render_template('encryptor.html', encText=encText)
    
    return render_template('encryptor.html')

@app.route('/decryptor', methods=['GET', 'POST'])
def decryptor():
    usertext=""
    password=""
    decText=""
    if request.method == 'POST':
        password = request.form['password']
        usertext = request.form['usertext']
        if usertext and password != "":
            try:
                decText = textDecryption(usertext, password)
            except:
                decText = "Incorrect Cipher text format."

        return render_template('encryptor.html', decText=decText)
    
    return render_template('encryptor.html')

def textEncryption(text, password):
    fulltext= text + password
    key = "F97H8ULMT0X6_H3_Tlu4tu2zD1WS175etwxs5fqDV6g="
    fernet = Fernet(key)
    encText = fernet.encrypt(fulltext.encode())
    return encText

def textDecryption(text, password):
    key = "F97H8ULMT0X6_H3_Tlu4tu2zD1WS175etwxs5fqDV6g="
    fernet = Fernet(key)
    decText = fernet.decrypt(text).decode()

    if password in decText:
        passcount = len(password)
        decText = decText[:-passcount]  # Remove the password from the decrypted text
        return decText
    else: 
        decText = "Error. Password is Wrong."
        return decText
    
@app.route('/ipdomaincheck')
def ipdomaincheck():
    return render_template('ipdomaincheck.html')

if __name__ == '__main__':

    try:

        app.run(host='0.0.0.0', port='5000', debug=True)

    except KeyboardInterrupt:

        print('Interrupted')


