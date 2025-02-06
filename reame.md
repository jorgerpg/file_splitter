Aqui está um exemplo de **README.md** para o seu sistema:

# Sistema de Upload e Download de Arquivos

Este é um sistema simples de upload e download de arquivos, desenvolvido utilizando Flask. Ele permite que os usuários façam login, realizem o upload de arquivos, visualizem os arquivos enviados e façam o download via `curl`.

## Funcionalidades

1. **Login**: Usuários podem acessar o sistema utilizando um nome de usuário e senha.
2. **Upload de Arquivos**: Os usuários podem enviar arquivos, que são divididos em partes de acordo com a quantidade especificada.
3. **Visualização de Arquivos**: A página de arquivos lista os arquivos e pastas armazenados no servidor.
4. **Download via `curl`**: Usuários podem baixar os arquivos via `curl`.

---

## Como Usar

### 1. Acessar o Sistema

Para acessar o sistema, abra seu navegador e vá para a URL:

```
http://jojisdomain.ddns.net:5000
```

### 2. Fazer Login

Na tela de login, insira as credenciais fornecidas:

- **Usuário**: `cimatec`
- **Senha**: `cimatec`

Após inserir as informações corretamente, clique no botão **Entrar** para ser redirecionado para a página de upload de arquivos.

### 3. Fazer Upload de Arquivos

Na página de upload:

1. **Selecione o Arquivo**: Clique no botão de escolha de arquivo para selecionar o arquivo que deseja enviar.
2. **Número de Partes**: Insira o número de partes em que o arquivo será dividido.
3. Clique no botão **Enviar** para realizar o upload do arquivo.

O arquivo será enviado e dividido nas partes especificadas.

### 4. Verificar Arquivos Enviados

Após o upload, para visualizar os arquivos enviados, acesse:

```
http://jojisdomain.ddns.net:5000/files
```

A página exibirá uma lista dos arquivos e pastas, incluindo os arquivos divididos em partes.

### 5. Fazer Download de Arquivos

Para fazer o download de um arquivo enviado, use o seguinte comando `curl`:

```bash
curl -O http://jojisdomain.ddns.net:5000/files/arquivo/...
```

Substitua `http://jojisdomain.ddns.net:5000/files/arquivo/...` pela URL do arquivo desejado. O parâmetro `-O` faz com que o arquivo seja salvo localmente com o nome original.

Se desejar salvar o arquivo com outro nome, use:

```bash
curl -o nome_do_arquivo_desejado.ext http://jojisdomain.ddns.net:5000/files/arquivo/...
```

### 6. Logout

Para sair do sistema, clique no link **Logout** na página de upload.

---

## Tecnologias Utilizadas

- **Flask**: Framework para o backend.
- **SQLite**: Banco de dados para autenticação de usuários.
- **HTML/CSS**: Para o frontend simples.

---

## Como Rodar o Sistema Localmente

### Pré-requisitos

1. Python 3.x
2. Flask
3. SQLite

### Instalar Dependências

Clone este repositório e instale as dependências:

```bash
git clone <URL do repositório>
cd <diretório do repositório>
pip install -r requirements.txt
```

### Rodar o Sistema

1. Crie o banco de dados SQLite:

```bash
python create_db.py
```

2. Inicie o servidor Flask:

```bash
python app.py
```

O sistema será iniciado em `http://127.0.0.1:5000`.

---

## Contribuindo

Se você deseja contribuir para este projeto, siga os seguintes passos:

1. Faça um fork deste repositório.
2. Crie uma branch para sua alteração (`git checkout -b feature/nome-da-alteracao`).
3. Realize suas alterações.
4. Commit suas mudanças (`git commit -am 'Adicionando nova feature'`).
5. Envie para o repositório remoto (`git push origin feature/nome-da-alteracao`).
6. Abra um Pull Request.

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
```

Esse **README.md** inclui informações sobre como usar o sistema, rodá-lo localmente, as tecnologias utilizadas, e contribuições para o projeto. Certifique-se de preencher o `<URL do repositório>` com o link real do seu repositório, caso queira disponibilizar esse repositório no GitHub.