import pytest
from app import app, lotes, entregas_mes

@pytest.fixture
def client():
    app.config["TESTING"] = True
    lotes.clear()
    entregas_mes.clear()
    with app.test_client() as client:
        yield client

def test_login_sucesso(client):
    res = client.post("/login", json={"email": "voluntario@mesa.org", "senha": "senha123"})
    assert res.status_code == 200

def test_fluxo_peps_e_bloqueio_duplicidade(client):
    res1 = client.post("/operacao", json={"cpf": "12345678900", "item": "Arroz 5kg", "validade": "20/12/2026"})
    assert res1.status_code == 201

    res_dup = client.post("/operacao", json={"cpf": "12345678900", "item": "Feijao 1kg", "validade": "10/11/2026"})
    assert res_dup.status_code == 409
