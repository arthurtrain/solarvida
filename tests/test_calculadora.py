import pytest
from services.calculadora_solar import CalculadoraSolar

def test_calculo_retorna_campos_esperados():
    r = CalculadoraSolar().calcular(300, 250)
    assert r["tamanho_sistema_kwp"] > 0
    assert "payback_anos" in r

def test_rejeita_consumo_abaixo_do_minimo():
    with pytest.raises(ValueError):
        CalculadoraSolar().calcular(10, 250)   # 10 < minimo (50)

def test_rejeita_fatura_acima_do_maximo():
    with pytest.raises(ValueError):
        CalculadoraSolar().calcular(300, 10_000_000)
