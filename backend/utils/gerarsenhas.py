#esse codigo nao deveria estar aqui, mas ficou bom para demonstração de como foi gerada as senhas.
import bcrypt

# Lista com 20 senhas
senhas = [
    "senha123", "admin!@#", "usuario2025", "meuCachorro42", "superSenha99",
    "segredoTop!", "qwertyuiop", "minhaSenhaSegura", "123456", "senhaFraca",
    "rootaccess", "liberdade789", "testeDeLogin", "senhaIncrivel@2025", "meuEmailSenha",
    "flor1234", "portalDoCliente", "verao2024!", "hackmepls", "sistemaSeguro!"
]

# Função para gerar hash
def gerar_hash_senha(senha: str) -> str:
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_senha.decode('utf-8')

# Armazenar os hashes
hashes = []

# Gerar e exibir os hashes
for senha in senhas:
    hash_gerado = gerar_hash_senha(senha)
    hashes.append(hash_gerado)
    print(f"Senha: {senha:<20} → Hash: {hash_gerado}")

# Verificação opcional
def verificar_senha(senha: str, hash_senha: str) -> bool:
    return bcrypt.checkpw(senha.encode('utf-8'), hash_senha.encode('utf-8'))

# Exemplo de verificação (verifica a senha 5)
print("\nVerificando senha:")
senha_teste = senhas[4]
hash_teste = hashes[4]
resultado = verificar_senha(senha_teste, hash_teste)
print(f"A senha '{senha_teste}' é válida? {resultado}")
