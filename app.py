from flask import Flask, request, jsonify
from datetime import datetime
import bcrypt

app = Flask(__name__)

# Base de dados simulada com hash seguro de senha (RNF01)
SENHA_HASH = bcrypt.hashpw(b"senha123", bcrypt.gensalt())
usuarios = {"voluntario@mesa.org": SENHA_HASH}
lotes = []
entregas_mes = set()


def validar_campos_operacao(dados):
    """Verifica se todos os campos obrigatorios foram preenchidos."""
    return all(dados.get(campo) for campo in ("cpf", "item", "validade"))


@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = dados.get("email", "")
    senha = dados.get("senha", "").encode("utf-8")

    hash_salvo = usuarios.get(email)
    if hash_salvo and bcrypt.checkpw(senha, hash_salvo):
        return jsonify({"status": "sucesso", "mensagem": "Autenticacao realizada com sucesso"}), 200
    return jsonify({"status": "erro", "mensagem": "Credenciais invalidas"}), 401


@app.route("/operacao", methods=["POST"])
def registrar_e_validar():
    dados = request.get_json() or {}
    if not validar_campos_operacao(dados):
        return jsonify({"status": "erro", "mensagem": "Campos obrigatorios ausentes"}), 400

    cpf = dados["cpf"]
    if cpf in entregas_mes:
        return jsonify({
            "status": "bloqueado",
            "alerta": "Alerta: Familia ja beneficiada no mes corrente. Entrega bloqueada!"
        }), 409

    lotes.append({"item": dados["item"], "validade": dados["validade"], "cpf_atendido": cpf})
    lotes.sort(key=lambda x: datetime.strptime(x["validade"], "%d/%m/%Y"))
    entregas_mes.add(cpf)

    return jsonify({
        "status": "sucesso",
        "mensagem": "Entrega validada e lote registado com regra PEPS",
        "lotes_ordenados": lotes
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
