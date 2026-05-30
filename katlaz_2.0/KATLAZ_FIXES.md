# Katlaz / KatlazApp - pacote revisado

## Principais correções

- Corrigidos imports quebrados do pacote `katlaz` (`version`/`katlazcc` inexistentes).
- Adicionados wrappers no pacote principal para `katlaz.parser`, `katlaz.codegen`, etc.
- Parser Katlaz refeito com Lark embutido e imports relativos corretos.
- Geração C recebeu compatibilidade com `FuncDef`, `Print`, `Return`, `If` e `While`.
- Bridge `katlazapp.runtime.bridge` ficou universal: aceita `str`, `bytes` e `dict` e devolve resposta serializável.
- Servidor visual (`runtime/app.py`) revisado: resolve arquivos dentro de `app/`, serve `app.html`, corrige MIME types, API `/api` e path traversal.
- Runtime `core.py` revisado: rotas mais seguras, normalização de retorno e erros melhores.
- Tipagem runtime revisada: `int`, `float`, `string/str`, `bool`, `any`.

## Novos poderes adicionados

### Integração com Python

No KatlazApp agora é possível chamar funções Python:

```katlaz
route raiz(x:int):
    py.call "math.sqrt" ${x}
```

O formato `${x}` passa a variável Katlaz gerada no Python. Sem `${}`, o valor é tratado como literal.

### Integração com C/C++

Use bibliotecas compartilhadas com funções exportadas em ABI C:

```cpp
extern "C" long long add(long long a, long long b) {
    return a + b;
}
```

Compile, por exemplo:

```bash
g++ -shared -fPIC demo.cpp -o libdemo.so
```

E chame no KatlazApp:

```katlaz
route soma_nativa:
    cpp.call "./libdemo.so" "add" 2 3
```

### Bridge da janela visual

O bridge continua aceitando mensagens do JavaScript/WebView:

```js
katlaz.call("hello", {name: "Igor"})
```

E no Katlaz:

```katlaz
route hello(name:string):
    emit "notify", "Olá " + name
```

## Como testar KatlazApp

```bash
cd katlazapp
python -m pip install -e .
katlazapp create meu_app
cd meu_app
katlazapp build main.katlaz
katlazapp serve
```

Abra:

```text
http://localhost:3000
```

## Observação

A compilação desktop com WebKitGTK ainda depende de bibliotecas do sistema (`gtk+-3.0`, `webkit2gtk` e `python3-dev`). O caminho mais estável para desenvolvimento é `katlazapp serve`, pois usa o mesmo bridge HTTP da janela visual.
