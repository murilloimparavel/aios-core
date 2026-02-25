# Guia de Configuração: API do Meta Ads

Para o squad de tráfego funcionar, o `TrafficManager`, `DataAnalyst` e `CreativeStrategist` precisam se comunicar com a Meta Marketing API. Para isso, você precisará configurar as variáveis de ambiente necessárias.

Um arquivo `.env.example` foi criado na pasta do squad (`/srv/projetos/mvp-system/squads/meta-ads-traffic/.env.example`). Renomeie-o para `.env` ou crie um novo `.env` com as informações abaixo:

## Passo a Passo para Obter as Credenciais

### 1. `META_APP_ID` e `META_APP_SECRET`
Estes são os dados do seu aplicativo na Meta.
1. Acesse o [Meta for Developers](https://developers.facebook.com/).
2. Faça login e vá em **Meus Aplicativos** (My Apps).
3. Clique em **Criar Aplicativo**, selecione a opção que inclui permissões de Negócios/API de Marketing (geralmente "Gerenciar integrações de negócios" ou "Outro").
4. Após criar, no painel do app, vá em **Configurações > Básico**.
5. Lá você encontrará o **ID do Aplicativo** (`META_APP_ID`) e a **Chave Secreta do Aplicativo** (`META_APP_SECRET`). Clique em "Mostrar" para copiar a chave secreta.

### 2. `META_ACCESS_TOKEN`
Este é o token de acesso de sistema que permite que os agentes façam alterações nas contas de anúncios de forma automatizada sem o login de um usuário humano expirar.
1. Acesse seu [Gerenciador de Negócios da Meta (Business Settings)](https://business.facebook.com/settings).
2. No menu à esquerda, expanda **Contas** e vá em **Aplicativos**. Adicione o aplicativo que você criou no passo anterior ao seu Gerenciador de Negócios.
3. Ainda no menu à esquerda, vá em **Usuários > Usuários do Sistema** (System Users). Se não existir nenhum, crie um novo Usuário do Sistema (dê permissão de Administrador do Sistema).
4. Adicione ativos ao seu Usuário do Sistema:
   - Clique em **Adicionar Ativos**.
   - Conceda a este usuário acesso à sua **Página**, sua **Conta de Anúncios** e seu **Pixel** (sempre marcando permissão total/controle administrativo).
5. Após adicionar os ativos, clique em **Gerar Novo Token**.
6. Selecione o Aplicativo criado.
7. O token *precisa* ter pelo menos as seguintes permissões selecionadas na lista:
   - `ads_management`
   - `ads_read`
   - `business_management`
8. Clique em gerar e **copie o Token gerado**. Ele será o seu `META_ACCESS_TOKEN`. Guarde-o em um local seguro, pois a Meta só o exibirá uma vez.

### 3. `META_AD_ACCOUNT_ID`
ID da sua Conta de Anúncios.
1. Acesse as **Configurações do Negócio** (Business Settings).
2. Vá em **Contas > Contas de Anúncios** (Ad Accounts).
3. Selecione a sua conta de anúncios de tráfego pago.
4. O ID da conta aparecerá embaixo do nome dela.
5. No arquivo `.env`, o padrão da Meta exige o prefixo `act_`. Por exemplo, se seu ID é `123456`, coloque: `META_AD_ACCOUNT_ID=act_123456`. (Nota: O arquivo `config.yaml` e as requisições API parecem tratar o ID dependendo de como está configurado, mas coloque *exatamente* como pede o `.env.example`, normalmente sem ou com `act_` dependendo da implementação que vimos no seu `meta-api-client.js`. Como no README está descrito `act_seu_account_id`, utilize esse formato).

### 4. `META_PAGE_ID`
ID da sua Página do Facebook.
1. Acesse **Contas > Páginas** no Gerenciador de Negócios.
2. O ID da página também está logo abaixo do nome dela. Copie e cole.

### 5. `META_PIXEL_ID`
ID do Pixel / Conjunto de Dados (Dataset).
1. Nas Configurações do Negócio, vá em **Fontes de Dados > Pixels** (ou **Conjuntos de dados / Datasets**, a nomenclatura da Meta mudou recentemente).
2. Selecione o pixel correspondente e copie a ID localizada abaixo de seu nome.

---

### Finalizando
Com todos esses 6 dados em mãos, cole tudo no arquivo `.env` dentro da pasta `squads/meta-ads-traffic` e estará tudo pronto para seu squad criar, escalar e monitorar campanhas de tráfego usando a estratégia Bid Cap.
