import re
import uuid
from urllib.parse import unquote, quote
import streamlit as st

# ---------------------------------- CONFIG ---------------------------------- #
st.set_page_config(
    page_title="Carrinho de Compras | Sicredi Soma",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700&display=swap');

:root {
  --linha-width: 100%;
  --linha-height: 3px;
  --linha-color: rgba(255,255,255,.63);
  --titulo-font-size: 3.1rem;
  --icone-size: 54px;
  --icone-stroke: #FFFFFF;            /* ÍCONE BRANCO */
  --icone-bg: transparent;
  --gap-icon-text: 14px;
  --conteudo-max-width: 960px;
  --padding-lateral: 2rem;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background:#5A645A !important;
  margin:0 !important;
  padding:0 !important;
  scroll-behavior:smooth;
  font-family:'Exo 2', sans-serif !important;
  -webkit-text-size-adjust: 100%;
}

#MainMenu, header, footer {display:none !important;}

.block-container {
  padding: 1.6rem var(--padding-lateral) 2.2rem var(--padding-lateral) !important;
  max-width: var(--conteudo-max-width) !important;
  width: 100% !important;
}

* {
  font-family:'Exo 2',sans-serif !important;
  color:#FFF;
  box-sizing:border-box;
  -webkit-font-smoothing: antialiased;
}

.titulo-area {
  display:flex;
  flex-direction:column;
  align-items:flex-start;
  margin:0 0 2.0rem 0;
}

.titulo-linha-row {
  display:flex;
  align-items:center;
  gap: var(--gap-icon-text);
  margin:0;
  padding:0;
  line-height:1;
  position:relative;
}

.titulo-linha-row h1 {
  font-size: var(--titulo-font-size);
  font-weight:700;
  margin:0;
  padding:0;
  line-height:1.1;
  white-space:nowrap;
  display:flex;
  align-items:center;
  letter-spacing:.5px;
}

.heading-line {
  width: 100%;
  height: 0;
  border-top: 2px solid rgba(255,255,255,.35);
  margin-top: 1.05rem;
  border-radius: 0;
  background: none;
}

/* GRID DE ITENS (100% controlado por CSS, sem st.columns) */
.item-grid {
  display:grid;
  grid-template-columns: 1fr 160px 54px; /* nome | preço | ação */
  column-gap: 0.75rem;
  align-items:center;
  padding: .95rem 0 .8rem 0;
  font-size:1.07rem;
  border-bottom:1px solid rgba(255,255,255,.18);
}

.item-grid:last-of-type {
  border-bottom:2px solid rgba(255,255,255,.34);
}

.col-nome {
  min-width: 0;
  overflow-wrap: anywhere;
}

.col-preco {
  text-align:right;
  font-variant-numeric: tabular-nums;
  letter-spacing:.5px;
  white-space: nowrap;
}

.col-acoes {
  display:flex;
  justify-content:flex-end;
}

/* Botão de remover como link estilizado (mesma cor de antes) */
.btn-x,
.btn-x:link,
.btn-x:visited,
.btn-x:hover,
.btn-x:active,
.btn-x:focus {
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:44px;
  height:44px;
  background:#0B1014 !important;                 /* como antes */
  border:1px solid rgba(255,255,255,0.30) !important;  /* como antes */
  color:#FFF !important;                          /* mantém o “X” branco */
  border-radius:10px;
  text-decoration:none !important;                /* remove sublinhado/estilo de link */
  font-size:18px;
  line-height:1;
  transition: background .25s ease, border-color .25s ease, transform .1s ease;
  outline: none !important;
}

.btn-x:hover {
  background:#b62828 !important;                  /* hover vermelho, como antes */
  border-color:#b62828 !important;
  color:#FFF !important;
}

.btn-x:active {
  transform: scale(0.97);
}

/* Opcional: tamanho no mobile, se você estiver usando @media */
@media (max-width: 780px) {
  .btn-x,
  .btn-x:link,
  .btn-x:visited,
  .btn-x:hover,
  .btn-x:active,
  .btn-x:focus {
    width:40px; height:40px; font-size:17px;
  }
}

/* TOTAIS */
.totais {
  margin-top:2.0rem;
  font-weight:700;
  font-size:1.07rem;
  border-top:2px solid rgba(255,255,255,.35);
  padding-top:1.25rem;
  display:flex;
  flex-direction:column;
  gap:.65rem;
}

.total-row {
  display:grid;
  grid-template-columns: 1fr 180px;
  align-items:center;
  font-variant-numeric: tabular-nums;
  letter-spacing:.5px;
}
.total-row span:last-child {
  text-align:right;
}

/* Bloco de dicas de URL e quebras longas no mobile */
.url-tip {
  margin-top:2.0rem;
  font-size:.80rem;
  opacity:.88;
  border-top:1px dashed rgba(255,255,255,.30);
  padding-top:.85rem;
  letter-spacing:.3px;
  width:var(--linha-width);
  overflow-wrap:anywhere;
}
.url-tip code {
  background: rgba(0,0,0,.25);
  padding: .12rem .34rem;
  border-radius: .35rem;
  white-space: pre-wrap;
  word-break: break-word;
}

/* MOBILE */
@media (max-width: 780px) {
  :root {
    --titulo-font-size: 2.2rem;
    --icone-size: 42px;
    --linha-width: 100%;
  }

  .block-container {
    padding: 1.2rem 1.0rem 1.6rem 1.0rem !important;
  }

  .item-grid {
    grid-template-columns: 1fr auto 44px;  /* preço encolhe conforme necessário */
    column-gap: .5rem;
    font-size:1.0rem;
    padding: .75rem 0 .65rem 0;
  }

  .col-preco {
    font-size:1.02rem;
  }

  .btn-x {
    width:40px; height:40px; font-size:17px;
  }

  .total-row {
    grid-template-columns: 1fr auto;
  }

  .url-tip {
    font-size:.78rem;
  }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -------------------------- CATÁLOGO (exemplo) --------------------------- #
CATALOGO = {
    # "codigo": {"nome": "Nome do produto", "preco": 0.00}
    "89": {"nome": "Prato", "preco": 95.90},
    "50": {"nome": "Camiseta", "preco": 20.55},
    # adicione aqui: "COD": {"nome": "Produto", "preco": 12.34}
}

# ---------------------- STORE COMPARTILHADO (persistência) ----------------- #
@st.cache_resource
def _cart_store():
    # Em memória do servidor enquanto o processo estiver ativo
    # Estrutura: { cid: { "Nome": {"preco": float, "qtd": int}, ... } }
    return {}

def _get_cid():
    cid = st.query_params.get("cid")
    if isinstance(cid, list):
        cid = cid[0]
    cid = (cid or "").strip() or None
    return cid

def _load_cart_from_store_once():
    # Carrega para a sessão atual o carrinho do cid (se houver)
    cid = _get_cid()
    if cid and not st.session_state.get("_loaded_from_store"):
        stored = _cart_store().get(cid, {})
        st.session_state.carrinho = {k: dict(v) for k, v in stored.items()}
        st.session_state._loaded_from_store = True

def _persist_cart_to_store():
    # Garante que exista um cid; cria um se necessário e o mantém na URL
    cid = _get_cid()
    if not cid:
        cid = st.session_state.get("_cid") or uuid.uuid4().hex[:8]
        st.session_state._cid = cid
        st.query_params["cid"] = cid
    _cart_store()[cid] = st.session_state.carrinho

# --------------------------- ESTADO INICIAL ------------------------------- #
if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}

# Se houver cid na URL, carrega o carrinho correspondente
_load_cart_from_store_once()

# ------------------------------ HELPERS ---------------------------------- #
def _normalize_key(k: str) -> str:
    return k.lower().replace("+", "").replace(" ", "")

def _get_param(qp, accepted_names: set):
    for k in qp.keys():
        if _normalize_key(k) in accepted_names:
            v = qp[k]
            if isinstance(v, list):
                v = v[0]
            return v, k
    return None, None

def _to_int(val, default=1):
    if val is None:
        return default
    try:
        return int(val)
    except Exception:
        m = re.search(r"-?\d+", str(val))
        if m:
            try:
                return int(m.group(0))
            except Exception:
                return default
        return default

def _add_item(nome: str, preco, qtd=1):
    if not nome:
        return
    try:
        preco = float(str(preco).replace(",", "."))
    except Exception:
        return
    try:
        qtd = int(qtd)
    except Exception:
        qtd = 1

    cart = st.session_state.carrinho
    if nome in cart:
        cart[nome]["qtd"] += qtd
        cart[nome]["preco"] = preco
    else:
        cart[nome] = {"preco": preco, "qtd": qtd}

def _add_code(codigo: str, qtd=1):
    if not codigo:
        return
    codigo = unquote(str(codigo)).strip()
    qtd = _to_int(qtd, 1)
    item = CATALOGO.get(codigo)
    if not item:
        return
    _add_item(item["nome"], item["preco"], qtd)

# ---------------------------- VIA URL ------------------------------------ #
def via_url():
    qp = st.query_params
    changed = False

    # limpar carrinho: ?clear=1
    if qp.get("clear"):
        st.session_state.carrinho = {}
        changed = True

    # remover item por nome ou código: ?rm=Camiseta  ou  ?rm=50
    rm_val, _ = _get_param(qp, {"rm", "remove", "del"})
    if rm_val:
        key = unquote(str(rm_val)).strip()
        # tenta por nome
        if key in st.session_state.carrinho:
            del st.session_state.carrinho[key]
            changed = True
        else:
            # tenta por código -> mapeia para nome
            item = CATALOGO.get(key)
            if item and item["nome"] in st.session_state.carrinho:
                del st.session_state.carrinho[item["nome"]]
                changed = True

    # múltiplos códigos: ?codes=89|2;50|1
    codes_val, _ = _get_param(qp, {"codes", "itens", "items", "codigos"})
    if codes_val:
        for chunk in str(codes_val).split(";"):
            if not chunk.strip():
                continue
            parts = [p.strip() for p in chunk.split("|")]
            if len(parts) == 1:
                _add_code(parts[0], 1)
            else:
                _add_code(parts[0], parts[1])
            changed = True

    # único código: aceita Codigo, codigo, code, cod, sku, id
    code_val, _ = _get_param(qp, {"codigo", "code", "cod", "sku", "id"})
    if code_val is not None:
        qty_val, _ = _get_param(qp, {"quantidade", "qty", "q"})
        _add_code(code_val, qty_val if qty_val is not None else 1)
        changed = True

    # compat: formato antigo ?produto=Nome&preco=9,90&quantidade=2
    if "produto" in qp and "preco" in qp:
        nome = qp["produto"]
        preco = qp["preco"]
        qtd = qp.get("quantidade", 1)
        if isinstance(nome, list): nome = nome[0]
        if isinstance(preco, list): preco = preco[0]
        if isinstance(qtd, list): qtd = qtd[0]
        _add_item(unquote(nome), preco, qtd)
        changed = True

    if changed:
        # salva no store (gera cid se não existir)
        _persist_cart_to_store()

        # limpa a URL, mas preserva o cid
        cid = _get_cid() or st.session_state.get("_cid")
        st.query_params.clear()
        if cid:
            st.query_params["cid"] = cid

        st.rerun()

via_url()

# --------------------------- UI: Título ---------------------------------- #
st.markdown("""
<div class="titulo-area">
  <div class="titulo-linha-row">
    <h1>
      Carrinho de Compras
      <span class="cart-icon" aria-hidden="true" title="Carrinho">
        <svg viewBox="0 0 24 24" width="0" height="0" style="position:absolute;opacity:0;"></svg>
      </span>
    </h1>
  </div>
  <div class="heading-line"></div>
</div>
""", unsafe_allow_html=True)

# ------------------------ Listagem dos Itens ----------------------------- #
total = 0.0
cid_current = _get_cid() or st.session_state.get("_cid")

if st.session_state.carrinho:
    for produto, info in list(st.session_state.carrinho.items()):
        subtotal = info["preco"] * info["qtd"]
        total += subtotal
        rm_href = "#"
        if cid_current:
            rm_href = f"?cid={quote(cid_current)}&rm={quote(produto)}"
        else:
            rm_href = f"?rm={quote(produto)}"

        st.markdown(
            f"""
<div class="item-grid">
  <div class="col-nome">{produto} × {info['qtd']}</div>
  <div class="col-preco">R$ {subtotal:.2f}</div>
  <div class="col-acoes"><a class="btn-x" href="{rm_href}" title="Remover {produto}">✕</a></div>
</div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Carrinho vazio")

# ------------------------------- Totais ---------------------------------- #
if st.session_state.carrinho:
    capital = total / 2
    st.markdown(f"""
<div class="totais">
  <div class="total-row"><span>Total Geral:</span><span>R$ {total:.2f}</span></div>
  <div class="total-row"><span>Total Capital:</span><span>R$ {capital:.2f}</span></div>
</div>
    """, unsafe_allow_html=True)

# ------------------------------- Dica URL -------------------------------- #
cid_tip = cid_current or "meu123"
st.markdown(f"""
<div class="url-tip">
<b>Adicionar por CÓDIGO via URL</b><br>
• Um item (mantendo o mesmo carrinho): <code>?cid={cid_tip}&Codigo=89&quantidade=1</code><br>
• Também funciona: <code>?cid={cid_tip}&codigo=50&q=3</code> ou <code>?cid={cid_tip}&code=50&qty=3</code><br>
• Vários itens: <code>?cid={cid_tip}&codes=89|2;50|1</code><br>
• Remover item: <code>?cid={cid_tip}&rm=Camiseta</code> ou <code>?cid={cid_tip}&rm=50</code><br>
• Limpar carrinho: <code>?cid={cid_tip}&clear=1</code><br><br>
Todos os direitos reservados Sicredi Soma
</div>
""", unsafe_allow_html=True)