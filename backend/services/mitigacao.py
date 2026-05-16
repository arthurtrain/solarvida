import sqlite3
import unittest

# ==========================================
# 1. CÓDIGO DA APLICAÇÃO (O "Antes" e "Depois")
# ==========================================

def get_user_vulnerable(cursor, username):
    """
    CENÁRIO VULNERÁVEL: Uso de concatenação de strings.
    O input do usuário faz parte da sintaxe SQL.
    """
    query = f"SELECT id, username, password FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

def get_user_secure(cursor, username):
    """
    CENÁRIO SEGURO: Uso de Query Parametrizada (Prepared Statement).
    Utilizamos o placeholder `?` e passamos a variável como uma tupla.
    """
    query = "SELECT id, username, password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchall()

# ==========================================
# 2. SUÍTE DE TESTES (Validando os Critérios de Pronto)
# ==========================================

class TestSQLInjectionMitigation(unittest.TestCase):
    
    def setUp(self):
        """Configura um banco de dados em memória para os testes com dados fictícios."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
        
        # Inserindo usuários legítimos
        self.cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'senha_super_secreta')")
        self.cursor.execute("INSERT INTO users (username, password) VALUES ('joao', 'senha123')")
        self.cursor.execute("INSERT INTO users (username, password) VALUES ('maria', 'abc987')")
        self.conn.commit()

    def tearDown(self):
        """Fecha a conexão após cada teste."""
        self.conn.close()

    # --- Teste 1: Confirmando o Funcionamento Normal ---
    def test_funcionamento_query_parametrizada(self):
        """Verifica se a query parametrizada funciona corretamente para inputs válidos."""
        resultados = get_user_secure(self.cursor, 'admin')
        
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0][1], 'admin')
        print("\n[OK] Query parametrizada funcionou corretamente para usuário legítimo.")

    # --- Teste 2: A Ameaça (Demonstrando a falha no código antigo) ---
    def test_sql_injection_sucesso_na_vulneravel(self):
        """Demonstra que o código antigo permite o roubo de dados."""
        # O atacante envia uma string que altera a lógica do SQL
        malicious_payload = "admin' OR '1'='1" 
        
        # Na query concatenada, isso vira: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
        resultados = get_user_vulnerable(self.cursor, malicious_payload)
        
        # O ataque funcionou: em vez de 1 usuário, retornou TODOS os usuários do banco
        self.assertTrue(len(resultados) > 1)
        print(f"[ALERTA] SQL Injection funcionou na função vulnerável! {len(resultados)} registros vazados.")

    # --- Teste 3: Tentativa de SQL Injection Bloqueada ---
    def test_sql_injection_bloqueada_na_segura(self):
        """Verifica se a query parametrizada bloqueia o ataque."""
        malicious_payload = "admin' OR '1'='1"
        
        # Na query parametrizada, o banco procura literalmente por um usuário 
        # cujo nome seja a string exata "admin' OR '1'='1"
        resultados = get_user_secure(self.cursor, malicious_payload)
        
        # O ataque foi neutralizado: nenhum dado é retornado
        self.assertEqual(len(resultados), 0)
        print("[SEGURO] SQL Injection bloqueada! A query parametrizada tratou o payload apenas como texto.")

if __name__ == '__main__':
    # Executa os testes
    unittest.main(argv=['first-arg-is-ignored'], exit=False)