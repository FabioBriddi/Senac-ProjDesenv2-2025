import hashlib
import os
from typing import Optional
import sqlite3
from datetime import datetime

def hash_password(password: str) -> str:
    """
    Gera hash SHA256 da senha com salt
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash da senha
    """
    # Usa uma chave secreta como salt (pode ser configurada no .env)
    salt = os.getenv('SECRET_KEY', 'music_api_default_salt_2024')
    
    # Cria o hash com salt
    password_with_salt = f"{password}{salt}"
    return hashlib.sha256(password_with_salt.encode()).hexdigest()

def check_password(username: str, password: str) -> bool:
    """
    Verifica se a combinação usuário/senha está correta
    
    Args:
        username: Nome de usuário
        password: Senha em texto plano
        
    Returns:
        True se as credenciais estão corretas, False caso contrário
    """
    # Usuários padrão do sistema (hardcoded para facilitar)
    default_users = {
        'admin': hash_password('admin123'),
        'demo': hash_password('demo'),
        'user': hash_password('user123')
    }
    
    # Também verifica credenciais do arquivo .env se existirem
    env_username = os.getenv('ADMIN_USERNAME', '')
    env_password = os.getenv('ADMIN_PASSWORD', '')
    
    if env_username and env_password:
        default_users[env_username] = hash_password(env_password)
    
    # Gera o hash da senha fornecida
    password_hash = hash_password(password)
    
    # Verifica primeiro nos usuários padrão
    if username in default_users:
        return default_users[username] == password_hash
    
    # Tenta verificar no banco de dados (se existir)
    try:
        db_path = os.getenv('DATABASE_PATH', 'data/database.db')
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT password_hash FROM users 
                WHERE username = ?
            """, (username,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0] == password_hash
    except Exception as e:
        print(f"Erro ao verificar usuário no banco: {e}")
    
    return False

def create_user(username: str, password: str, email: Optional[str] = None,
               role: str = 'user') -> bool:
    """
    Cria um novo usuário no banco de dados
    
    Args:
        username: Nome de usuário (único)
        password: Senha em texto plano
        email: Email do usuário (opcional)
        role: Papel do usuário (admin, user, viewer)
        
    Returns:
        True se o usuário foi criado com sucesso, False caso contrário
    """
    try:
        # Importa Database apenas quando necessário
        from src.database import Database
        
        db = Database()
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Gera o hash da senha
        password_hash = hash_password(password)
        
        # Insere o novo usuário
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, email, role, datetime.now()))
        
        conn.commit()
        conn.close()
        
        print(f"Usuário '{username}' criado com sucesso!")
        return True
        
    except sqlite3.IntegrityError:
        print(f"Erro: Usuário '{username}' já existe!")
        return False
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False

def update_password(username: str, new_password: str) -> bool:
    """
    Atualiza a senha de um usuário existente
    
    Args:
        username: Nome de usuário
        new_password: Nova senha em texto plano
        
    Returns:
        True se a senha foi atualizada, False caso contrário
    """
    try:
        from src.database import Database
        
        db = Database()
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Gera o hash da nova senha
        password_hash = hash_password(new_password)
        
        # Atualiza a senha
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, updated_at = ?
            WHERE username = ?
        ''', (password_hash, datetime.now(), username))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            print(f"Senha do usuário '{username}' atualizada com sucesso!")
            return True
        else:
            conn.close()
            print(f"Usuário '{username}' não encontrado!")
            return False
            
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")
        return False

def delete_user(username: str) -> bool:
    """
    Remove um usuário do sistema
    
    Args:
        username: Nome de usuário a ser removido
        
    Returns:
        True se o usuário foi removido, False caso contrário
    """
    try:
        from src.database import Database
        
        db = Database()
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        # Remove o usuário
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            print(f"Usuário '{username}' removido com sucesso!")
            return True
        else:
            conn.close()
            print(f"Usuário '{username}' não encontrado!")
            return False
            
    except Exception as e:
        print(f"Erro ao remover usuário: {e}")
        return False

def list_users() -> list:
    """
    Lista todos os usuários cadastrados no sistema
    
    Returns:
        Lista de dicionários com informações dos usuários
    """
    users = []
    
    # Usuários padrão
    users.append({'username': 'admin', 'role': 'admin', 'source': 'default'})
    users.append({'username': 'demo', 'role': 'viewer', 'source': 'default'})
    
    # Busca usuários do banco
    try:
        from src.database import Database
        
        db = Database()
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT username, email, role, created_at 
            FROM users
            ORDER BY created_at DESC
        """)
        
        for row in cursor.fetchall():
            users.append({
                'username': row[0],
                'email': row[1],
                'role': row[2],
                'created_at': row[3],
                'source': 'database'
            })
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
    
    return users

def verify_role(username: str, required_role: str) -> bool:
    """
    Verifica se um usuário tem o papel necessário
    
    Args:
        username: Nome de usuário
        required_role: Papel necessário (admin, user, viewer)
        
    Returns:
        True se o usuário tem o papel necessário, False caso contrário
    """
    # Roles hierárquicos: admin > user > viewer
    role_hierarchy = {
        'admin': 3,
        'user': 2,
        'viewer': 1
    }
    
    # Usuários padrão e seus roles
    default_roles = {
        'admin': 'admin',
        'demo': 'viewer',
        'user': 'user'
    }
    
    # Verifica role do usuário
    user_role = None
    
    if username in default_roles:
        user_role = default_roles[username]
    else:
        # Busca no banco
        try:
            from src.database import Database
            
            db = Database()
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if result:
                user_role = result[0]
            
            conn.close()
            
        except Exception as e:
            print(f"Erro ao verificar role: {e}")
    
    # Compara roles hierarquicamente
    if user_role and user_role in role_hierarchy and required_role in role_hierarchy:
        return role_hierarchy[user_role] >= role_hierarchy[required_role]
    
    return False

# Função utilitária para criar usuário admin inicial
def create_admin_user():
    """
    Cria o usuário administrador inicial do sistema
    Útil para configuração inicial
    """
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@musicapi.com')
    
    if create_user(admin_username, admin_password, admin_email, 'admin'):
        print(f"""
        ✅ Usuário administrador criado com sucesso!
        
        Credenciais:
        - Usuário: {admin_username}
        - Senha: {admin_password}
        
        ⚠️ IMPORTANTE: Altere a senha após o primeiro login!
        """)
    else:
        print("⚠️ Usuário administrador já existe ou erro ao criar.")

# Se executado diretamente, cria usuário admin
if __name__ == "__main__":
    print("=== Sistema de Autenticação - Music API Manager ===")
    print("\n1. Criar usuário admin")
    print("2. Criar novo usuário")
    print("3. Listar usuários")
    print("4. Alterar senha")
    print("5. Remover usuário")
    
    choice = input("\nEscolha uma opção: ")
    
    if choice == "1":
        create_admin_user()
    
    elif choice == "2":
        username = input("Nome de usuário: ")
        password = input("Senha: ")
        email = input("Email (opcional): ")
        role = input("Role (admin/user/viewer): ") or "user"
        
        if create_user(username, password, email if email else None, role):
            print("✅ Usuário criado com sucesso!")
        else:
            print("❌ Erro ao criar usuário!")
    
    elif choice == "3":
        users = list_users()
        print("\n=== Usuários Cadastrados ===")
        for user in users:
            print(f"- {user['username']} ({user['role']}) - {user['source']}")
    
    elif choice == "4":
        username = input("Nome de usuário: ")
        new_password = input("Nova senha: ")
        
        if update_password(username, new_password):
            print("✅ Senha atualizada!")
        else:
            print("❌ Erro ao atualizar senha!")
    
    elif choice == "5":
        username = input("Nome de usuário a remover: ")
        confirm = input(f"Confirma remoção de '{username}'? (s/n): ")
        
        if confirm.lower() == 's':
            if delete_user(username):
                print("✅ Usuário removido!")
            else:
                print("❌ Erro ao remover usuário!")