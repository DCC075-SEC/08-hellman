# Diffie-Hellman (DH) em Python

Implementação simples do protocolo Diffie-Hellman para compartilhamento de um segredo `s` entre Alice e Bob por um canal inseguro.

## Como o algoritmo funciona

O DH não criptografa mensagens. Ele serve para **trocar chaves**: duas partes chegam ao mesmo valor secreto `s` sem nunca enviá-lo pela rede.

A segurança vem do **problema do logaritmo discreto**: dado `p`, `g` e `A = g^a mod p`, calcular `g^a mod p` é fácil, mas descobrir `a` a partir de `A` é computacionalmente inviável quando `p` é grande.

### Passo a passo

1. Alice e Bob combinam, publicamente, um primo `p` e uma raiz primitiva `g` módulo `p`.
2. Alice escolhe um segredo `a` e envia `A = g^a mod p`.
3. Bob escolhe um segredo `b` e envia `B = g^b mod p`.
4. Alice calcula `s = B^a mod p`.
5. Bob calcula `s = A^b mod p`.

Os dois chegam ao mesmo valor porque:

```
B^a = (g^b)^a = g^(a*b) = (g^a)^b = A^b   (mod p)
```

### O que é público e o que é secreto

| Valor | Quem conhece |
|-------|--------------|
| `p`, `g` | todos (inclusive o atacante) |
| `A`, `B` | todos (trafegam pelo canal) |
| `a` | só Alice |
| `b` | só Bob |
| `s` | só Alice e Bob |

Quem intercepta `p`, `g`, `A` e `B` não consegue calcular `s` sem resolver o logaritmo discreto.

### Exemplo pequeno 

`p = 23`, `g = 5`, `a = 6`, `b = 15`

- `A = 5^6 mod 23 = 8`
- `B = 5^15 mod 23 = 19`
- Alice: `s = 19^6 mod 23 = 2`
- Bob: `s = 8^15 mod 23 = 2`

### Por que `g` precisa ser raiz primitiva?

Uma raiz primitiva módulo `p` gera, ao ser elevada a 1, 2, ..., p-1, todos os valores de 1 a p-1. Assim `A` e `B` podem assumir qualquer valor do grupo, o que dificulta ao atacante restringir as possibilidades de `a` e `b`.

## Como o código funciona

Arquivo: `diffie_hellman.py` (só usa a biblioteca padrão `random`).

### `eh_primo(n)`
Teste de primalidade de Miller-Rabin (probabilístico, 20 rodadas). Primeiro descarta divisores pequenos, depois escreve `n-1 = 2^r * d` e testa bases aleatórias.

### `gera_p(bits)`
Gera um **primo seguro**: `p = 2*q + 1`, com `q` também primo. Sorteia `q` até que `q` e `p` passem no teste de primalidade.

### `acha_g(p, q)`
Procura a raiz primitiva. Como `p - 1 = 2 * q`, os únicos divisores de `p - 1` são `1, 2, q` e `p - 1`. Logo `g` é raiz primitiva se:

- `g^2 mod p != 1` e
- `g^q mod p != 1`

Testa `g = 2, 3, 4, ...` até satisfazer isso. Por isso o primo seguro é usado: sem ele seria preciso fatorar `p - 1`.

### Programa principal

```python
p, q = gera_p(256)          # primo de 256 bits
g = acha_g(p, q)            # raiz primitiva
a = random.randrange(2, p - 1)   # segredo de Alice
b = random.randrange(2, p - 1)   # segredo de Bob
A = pow(g, a, p)            # Alice envia A
B = pow(g, b, p)            # Bob envia B
s_alice = pow(B, a, p)      # Alice calcula s
s_bob = pow(A, b, p)        # Bob calcula s
```

No final o programa imprime `p, g, a, b, A, B` e os dois `s`, e confere se são iguais.

## Como executar

Requisito: Python 3.

```bash
python3 hellman.py
```

A execução leva alguns segundos, por causa da busca pelo primo seguro.

### Saída esperada

```
p = ...
g = ...
a = ...
b = ...
A = ...
B = ...
s (Alice) = ...
s (Bob)   = ...
Segredos iguais? True
```

Os valores mudam a cada execução, pois `p`, `a` e `b` são sorteados.

### Valores de uma execução (exemplo)

```
p = 71383160871998726450917259608350984357581216942915066793561007200753889460027
g = 2
a = 883446059525858574541171815421473654804978905057362350082583821027748045403
b = 30022707895164411594265870387548111900082499979959480368276068877653265648991
A = 21599735708963375132357397216042157981091922982931812091222780173007975226017
B = 16698379601346977033485062529886371462611566253575071981891863279900473313479
s = 2053388436161120405656843939799696127231954602269813560720744482815531656484
```

### Mudar o tamanho do primo

Em `diffie_hellman.py`, altere o argumento de `gera_p`:

```python
p, q = gera_p(256)   # troque 256 por 512, 1024...
```

Quanto maior, mais seguro e mais demorado para gerar.
