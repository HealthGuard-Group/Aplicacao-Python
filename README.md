# Python - HealthGuard


<h1>Repositório para guardar nossos Scripts de captura de dados dos componentes das máquinas de despacho em Python</h1>

<h2>Sobre o Projeto</h2>
<p>Este projeto é dedicado ao monitoramento de peças vitais de máquinas de despacho que fazem parte do sistema DAC (Despacho Assistido por Computador).</p>

<h2>Justificativa</h2>
<ul>
    <li>
        <strong>Vidas estão em jogo:</strong> Qualquer atraso na máquina de despacho devido falhas de hardware inesperadas impacta diretamente em vidas.
    </li>
    <li>
        <strong>Falta de monitoramento ativo:</strong> Atualmente, não existem soluções integradas com o sistema de DAC para assegurar e notificar o suporte de TI das centrais de atendimento do SAMU no caso de falhas de hardware.
    </li>

</ul>
<h2>Funcionalidades</h2>
<p>O site oferece as seguintes funcionalidades:</p>
<ul>
    <li>
        <strong>Funcionalidade 1:</strong> Coleta de métricas de hardware
    </li>
    <li>
        <strong>Funcionalidade 2:</strong> Geração de logs históricos
    </li>
    <li>
        <strong>Funcionalidade 3:</strong> Detecção de falhas ou comportamento anômalo
    </li>
    <li>
        <strong>Funcionalidade 4:</strong> Customização e configuração de métricas
    </li>
    <li>
        <strong>Funcionalidade 5:</strong> Alertas preditivos usando histórico
    </li>

</ul>

<h2>Tecnologia Utilizada</h2>


![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)


## Como executar o monitoramento:

1º - Abra um terminal no seu computador, e rode esse comando no seu terminal:
 



```bash
  git clone https://github.com/HealthGuard-Group/Aplicacao-Python.git
```
Caso você não saiba abrir o terminal vá a apêndice 1. Caso não tenha o git instalado na sua máquina vá a apêndice 2.

2º - Após executar o comando, entre no repositório Aplicacao-Python e execute esse comando no seu terminal:
```bash
  bash init.sh
```
Caso o terminal volte o erro de comando desconhecido vá a apêndice 3. 

3º - Ao executar o script é necessário que você insira as suas crendeciais do banco, e logo após indetificar se o seu Sistema Operacional é windows ou linux. *Rejeite a opção de iniciar o programa(Opção em Manutenção)*

4º - Após a execução do script o rode o arquivo chamado ScriptCapturaPython.py. Caso não consiga executar vá a apêndice 4.

5º - Quando rodar o arquivo Python insira o código da configuração disponibilizado no site da HealthGuard após criar uma máquina



## Apêndice

*Apêndice 1* - Para abrir o terminal no windows, use o comando Crtl + R, executando esse comando irá aparecer um janela como o nome executar, digite "cmd" nessa janela, após isso o terminal irá ser aberto na sua tela. Se você tiver um Linux faça o comando Crtl + alt + T, e irá aparecer o terminal na sua tela.

*Apêndice 2* - Para baixar o git acesse o site abaixo:

- https://git-scm.com/install/windows

E siga o passo a passo, caso tenha dúvida utilize esse vídeo de apoio:
*Windows*
- https://www.youtube.com/watch?v=Am46OOLgV4s
*Linux*
- Já vem instalado padrão

*Apêndice 3* - Se der esse erro no terminal, abra o terminal com o git:

- Windows 10
Clique com o botão direito, no explorador de arquivos(Clique na janela aberta) após isso clique em abrir com o git bash
- Windows 11
Clique com o botão direito, no explorador de arquivos(Clique na janela aberta) após isso clique exibir mais opções, e logo após clique em abrir com git bash

Após isso prosiga com o passo no qual deu erro

*Apêndice 4* - Caso não consiga executar o arquivo, você pode não ter instalado o python, nesse caso siga esse tutorial

*Para Windows*
- https://www.youtube.com/watch?v=nM1QSFT4QR4

*Para Linux*
- https://www.youtube.com/watch?v=fVihVKJaTgw



<h2>Autor</h2>
<p>O projeto foi desenvolvido pela HealthGuard.</p>
