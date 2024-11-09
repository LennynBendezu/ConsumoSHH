from flask import Flask, jsonify, send_file
import paramiko
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def descargar_excel():
    # SSH
    hostname = 'ssh-natureza.alwaysdata.net'
    port = 22
    username = 'natureza_anon'
    password = '(123456)'
    remote_path = 'Bendezu.xlsx'

    try:
        # Conectar al servidor
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        # Descargar
        sftp = ssh.open_sftp()
        excel_buffer = BytesIO()
        with sftp.open(remote_path, 'rb') as remote_file:
            excel_buffer.write(remote_file.read())
        excel_buffer.seek(0)
        sftp.close()
        ssh.close()

        # ENVIO COMO RESPUESTA
        return send_file(excel_buffer, download_name="Bendezu.xlsx", as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
