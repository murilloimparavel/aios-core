import os
import sys
import json
from datetime import datetime

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-auth-oauthlib",
#     "python-dotenv",
# ]
# ///

from dotenv import load_dotenv

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/chat.messages",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/script.projects",
    "https://www.googleapis.com/auth/script.deployments",
    "https://www.googleapis.com/auth/script.processes",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]

def main():
    load_dotenv()
    # Allow http://localhost for OAuth (required for headless auth)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    user_email = os.environ.get("USER_GOOGLE_EMAIL")

    if not client_id or not client_secret or not user_email:
         print("Erro: GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET ou USER_GOOGLE_EMAIL faltando no arquivo .env")
         sys.exit(1)

    client_config = {
        "installed": {
            "client_id": client_id,
            "project_id": "aios",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": client_secret,
            "redirect_uris": ["http://localhost"]
        }
    }

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Erro: Bibliotecas não encontradas. Por favor rode usando: uv run auth_vps.py")
        sys.exit(1)

    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    flow.redirect_uri = "http://localhost"
    
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
    
    print("\n" + "=" * 60)
    print("AIOS WORKSPACE - HEADLESS AUTHENTICATION")
    print("=" * 60)
    print("\n1. Abra este link no navegador da sua MÁQUINA LOCAL (Windows/Mac):\n")
    print(auth_url)
    print("\n2. Faça o login com a sua conta Google e permita todos os acessos")
    print("3. Você será redirecionado para uma URL que começa com 'http://localhost'")
    print("   👉 É NORMAL a página não carregar e dar 'Erro de Conexão'!")
    print("4. Copie a URL INTEIRA da barra de endereços do navegador que deu erro")
    print("   (Parece algo como: http://localhost/?state=...&code=4/0A...)")
    print("5. Cole essa URL inteira aqui no terminal e dê Enter:\n")
    
    redirect_response = input("Cole a URL inteira aqui: ").strip()
    
    print("\nProcessando código de autorização...")
    
    try:
        flow.fetch_token(authorization_response=redirect_response)
    except Exception as e:
        print(f"\n❌ Erro ao validar token. Você colou a URL correta? Detalhes: {e}")
        sys.exit(1)
        
    creds = flow.credentials

    # Definindo e gerando a pasta oficial de credenciais do workspace-mcp
    import pathlib
    home_dir = pathlib.Path.home()
    creds_dir = home_dir / ".google_workspace_mcp" / "credentials"
    creds_dir.mkdir(parents=True, exist_ok=True)
    
    creds_path = creds_dir / f"{user_email}.json"
    
    creds_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "expiry": creds.expiry.isoformat() + "Z" if creds.expiry else None,
    }
    
    with open(creds_path, "w") as f:
        json.dump(creds_data, f, indent=2)
        
    print(f"\n✅ Login bem-sucedido! Credenciais salvas para {user_email}")
    print(f"Arquivo gerado em: {creds_path}")
    print("\n🎉 Tudo pronto! Agora os servidores MCP do projeto reconhecerão sua conta.")

if __name__ == "__main__":
    main()
