# oci-fc-fn-monitor-adb-telegram
Function de Monitoramento de métricas para comunicar o funcionário de Plantão



# Monitorando OCI por escala utilizando Telegram

Está função foi criada para notificar apenas os funcionários de plantão quando ocorrer algo incomum no Autonomous Database da Oracle Cloud.

Para essa simulação foi adaptado uma aplicação em APEX desenvolvido durante o bootcamp de Oracle Cloud.

O sistema ficou com as seguintes tabelas:
- Funcionários (nome e telegram);
- Férias (quem nunca será notificado);
- Escala de Plantão (quem será notificado).

Em seguida desenvolvi uma Function (FaaS) na OCI em Python para notificar os funcionários utilizando o Telegram Messenger, seguindo as seguintes regras:
- Identificar os funcionários de plantão;
- Caso não encontre funcionários de plantão notificar todos que não estão de férias.

# Vídeo com uma mini apresentação:
https://www.linkedin.com/posts/gdcosta_oci-oraclecloud-oracle-activity-6790468462050447360-Z04-
