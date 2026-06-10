from controllers.auth_controller import SENHA_REGEX

def test_senha_forte_aceita():
    assert SENHA_REGEX.match("Senha@123")

def test_senha_sem_simbolo_rejeitada():
    assert not SENHA_REGEX.match("Senha123")

def test_senha_curta_rejeitada():
    assert not SENHA_REGEX.match("Ab@1")
