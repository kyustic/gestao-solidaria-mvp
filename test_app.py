import pytest
from app import app, lotes, entregas_mes, validar_campos_operacao


@pytest.fixture
def client():
    app.config["TESTING"] = True
    lotes.clear()
    entregas_mes.clear()
    with app.test_client() as client:
        yield client


def test_validar_campos_operacao_unitario():
    assert validar_campos_operacao({"cpf": "12345678900", "item": "Arroz 5kg", "validade": "20/12/2026"}) is True
    assert validar_campos_operacao({"cpf": "12345678900", "item": ""}) is False


def test_login_sucesso_e_credenciais_invalidas(client):
    res_ok = client.post("/login", json={"email": "voluntario@mesa.org", "senha": "senha123"})
    assert res_ok.status_code == 200

    res_erro = client.post("/login", json={"email": "voluntario@mesa.org", "senha": "errada"})
    assert res_erro.status_code == 401


def test_operacao_campos_obrigatorios_ausentes(client):
    res = client.post("/operacao", json={"cpf": "12345678900"})
    assert res.status_code == 400


def test_fluxo_peps_e_bloqueio_duplicidade(client):
    res1 = client.post("/operacao", json={"cpf": "12345678900", "item": "Arroz 5kg", "validade": "20/12/2026"})
    assert res1.status_code == 201

    res_dup = client.post("/operacao", json={"cpf": "12345678900", "item": "Feijao 1kg", "validade": "10/11/2026"})
    assert res_dup.status_code == 409
