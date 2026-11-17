feat: implementa autenticacao, gestao de lotes PEPS e validacao de CPF.   
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de dados simulada em memória para o MVP
usuarios = {"voluntario@mesa.org": "senha123"}
lotes = []
entregas_mes = set()

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = dados.get("email")
    senha = dados.get("senha")
    if usuarios.get(email) == senha:
        return jsonify({"status": "sucesso", "mensagem": "Autenticacao realizada com sucesso"}), 200
    return jsonify({"status": "erro", "mensagem": "Credenciais invalidas"}), 401

@app.route("/operacao", methods=["POST"])
def registrar_e_validar():
    dados = request.get_json() or {}
    cpf = dados.get("cpf")
    item = dados.get("item")
    validade = dados.get("validade")

    if not cpf or not item or not validade:
        return jsonify({"status": "erro", "mensagem": "Campos obrigatorios ausentes"}), 400

    # RF03: Bloqueio de duplicidade de entrega no mesmo mês
    if cpf in entregas_mes:
        return jsonify({
            "status": "bloqueado",
            "alerta": "Alerta: Familia ja beneficiada no mes corrente. Entrega bloqueada!"
        }), 409

    # RF01: Registo de lote e ordenação por validade (PEPS)
    lotes.append({"item": item, "validade": validade, "cpf_atendido": cpf})
    lotes.sort(key=lambda x: datetime.strptime(x["validade"], "%d/%m/%Y"))
    entregas_mes.add(cpf)

    return jsonify({
        "status": "sucesso",
        "mensagem": "Entrega validada e lote registado com regra PEPS",
        "lotes_ordenados": lotes
    }), 201

if __name__ == "__main__":
    app.run(debug=True)
