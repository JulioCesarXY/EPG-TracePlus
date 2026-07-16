# 📺 Trace Plus & EPG Automation

[![EPG e M3U Trace Plus](https://github.com/JulioCesarXY/EPG-TracePlus/actions/workflows/update_trace.yml/badge.svg)](https://github.com/JulioCesarXY/EPG-TracePlus/actions/workflows/update_trace.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Update Frequency](https://img.shields.io/badge/Atualização-A%20cada%204%20horas-cron-green)

Este projeto automatiza a captura, organização e geração da lista de canais (M3U) e da grade de programação integrada (EPG XMLTV) para toda a rede de canais **Trace Plus** (Trace Toca, Trace Brazuca, Trace Urban, etc.).

O pipeline é executado de forma 100% serverless através do GitHub Actions a cada 4 horas, garantindo que o seu player de IPTV sempre tenha a grade de programação em tempo real sem travamentos.

---

## ✨ Recursos Principais

* **Foco em Performance:** Une as 26 fontes oficiais de EPG da Trace em um único arquivo mestre de saída (`epg_final.xml`).
* **Sincronização Frequente:** Atualizações automáticas a cada 4 horas para acompanhar mudanças dinâmicas e alterações de última hora na programação de TV.
* **Logos Originais de Alta Qualidade:** Vincula cada canal à sua respectiva identidade visual hospedada diretamente no CDN da plataforma (Umbraco).
* **Tratamento de Dados:** * Normalização completa de datas e fusos horários para o padrão internacional XMLTV (`YYYYMMDDHHMMSS +0000`).
  * Expurgamento automático de entidades HTML corrompidas (`&quot;`, `\`, `"`) de dentro das tags de dados para evitar rejeição por parte de players exigentes.
* **Bypass de Bloqueio de Rede:** Playlist M3U gerada com propriedades `#EXTVLCOPT` embutidas (`User-Agent` e `Referer`), contornando erros do tipo `403 Forbidden` na reprodução dos streams.

---

## 🛠️ Como Funciona o Pipeline

```text
[Trace Source APIs] ──> [Python Script] ──> [Sanitização e Junção] ──> [Commit Automático] ──> [Arquivos Raw]
                              │                                                                    │
                 (Roda a cada 4h via Actions)                                              (Seu Player IPTV)
```

