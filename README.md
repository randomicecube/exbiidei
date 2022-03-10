# DEIPaper

- [DEIPaper](#deipaper)
  - [Dependências](#dependências)
  - [Correr a aplicação](#correr-a-aplicação)
  - [Opções de desenho](#opções-de-desenho)

Projeto realizado no âmbito da candidatura à BII BL039/2022, tendo como objetivo implementar um sistema muito simples de gestão de publicações científicas para o DEI, sistema esse ligado à API [ISTPaper](https://aduck.rnl.tecnico.ulisboa.pt/istpaper/swagger-ui/index.html). Recorreu-se às _frameworks_ `Django` e `bootstrap` para a modelação do sistema.

## Dependências

Para correr a aplicação localmente, é necessária uma máquina equipada com:

  - `Django`, 4.0 ou superior;
  - `requests`, 2.27 ou superior;
  - `django-crispy-forms`, 1.14 ou superior.

De realçar que as versões acima mencionadas foram as utilizadas em desenvolvimento, pelo que é possível que versões mais antigas funcionem de igual forma.

Para as instalar, basta executar `pip install Django requests django-crispy-forms`.

Por fim, executar `pip freeze` e verificar se as dependências foram corretamente instaladas.

## Correr a aplicação

Instaladas as dependências, basta executar o comando `python manage.py runserver --insecure` na raiz deste repositório para correr a aplicação.  
Vale a penar notar que a flag `--insecure` é necessária para que o `Django` consiga disponibilizar os ficheiros estáticos sem a flag `Debug` ativa.

De seguida, poderá interagir com a aplicação através do browser, por exemplo, acedendo via http://localhost:8000/ ou http://127.0.0.1:8000.

`AUTH_TOKEN` deve estar definida como variável de ambiente do sistema para que a aplicação possa funcionar.

## Opções de desenho

- Foi decidido implementar um aspeto _dark mode_ por definição - com mais tempo, teria interessado implementar um _toggle_ que permitisse ao utilizador escolher entre visuais _light_ e _dark_, mas a ideia foi abandonada.

- Não foram colocadas as _views_ que permitem editar e eliminar publicações diretamente na _homepage_:

  - Editar publicações é possível através da página específica de cada publicação - desta forma, o utilizador pode facilmente ver todos os detalhes do _paper_ que pretende editar antes de o fazer, sendo porventura mais intuitivo do que um _form_ onde se permite editar qualquer _paper_ na _homepage_.

  - Remover publicações é possível, para além de na página específica de cada publicação, na secção de listagem de todas as publicações (associada ao _paper_ da linha em que o botão se encontra). O utilizador continua, tal como ao editar, a ter de **ver** a publicação antes de a poder remover.
  
  Ainda quanto à _homepage_, destacou-se a **listagem** da publicações em relação às outras opções apresentadas, por ser a operação que o utilizador comum provavelmente procurará realizar mais frequentemente.

- Foram utilizados [Modal Forms](https://getbootstrap.com/docs/4.3/components/modal/#varying-modal-content) em vez dos Forms padrão do `bootstrap`, com vista a evitar páginas cheias de formulários - um utilizador só vê um formulário quando diz que o quer ver (seja isso carregando num botão, aparecendo o tal Modal Form, ou quando o próprio formulário é todo o conteúdo da página).

- A paginação não apresenta qualquer opção de filtragem e/ou ordenação, visto que da forma como a API `ISTPaper` é implementada, só é possível obter `limit` publicações por vez - ora, sem saber o limite de publicações existentes, não podemos pedi-las todas de forma a realizar essas operações, pelo que a ideia foi abandonada.
