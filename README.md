# carregamento-inteligente-de-veiculos-eletricos
##### Johnny Araujo
##### Mauricio Santana Muniz

#### 1. Introdução
Considerando as vantagens que a IoT pode proporcionar às pessoas e meio ambiente, o problema proposto foi um sistema de comunicação inteligente, padronizado e em tempo real entre todos postos de recarga de carros elétricos. Nesse projeto temos uma aplicações que simulam carros, postos de carga, servidores onde recebem informações dos postos, onde todos se comunicam em rede remotamente e também online para realizar as operações de descarga, recarga, posto próximo, lotação de postos, troca de informações com servidor central. 

#### 2. Tecnologias utilizadas no desenvolvimento
- linguagem: python3.10.6 
- Ambiente de testes do cliente: Insomnia

O sistema foi desenvolvido na linguagem python, foi utilizado da framework Flask para fazer o gerenciamento de rotas e as requisições HTTP.

Foi utilizado também o mqtt que é um protocolo de comunicação leve e eficiente para fazer a comunicação de dispositos IoT.

<h4 align="center" href= "https://aws.amazon.com/what-is/mqtt/?nc1=h_ls">MQTT</h4>
O MQTT (Message Queuing Telemetry Transport) é um protocolo de transporte de mensagens em fila para atividades de telemetria. Ele foi projetado para o transporte de mensagens de publicação/assinatura extremamente leve, ideal para conectar dispositivos utilizando código reduzido e largura de banda de rede mínima. O MQTT é um protocolo de mensagens publish/subscribe, projetado para o transporte de telemetria em enfileiramento de mensagens simples e leve, com baixa largura de banda, e protocolo de conectividade machine-to-machine (M2M) ou “máquina para máquina”, que funciona no topo do protocolo TCP / IP.

O MQTT é amplamente utilizado em aplicações IoT (Internet das Coisas), onde a largura de banda da rede é limitada e a conectividade é intermitente. Ele é usado para enviar dados entre dispositivos IoT e servidores em nuvem.

<h4 align="center" href="https://www.treinaweb.com.br/blog/o-que-e-flask/">Flask</h4>
Flask é um pequeno framework web escrito em Python. É classificado como um microframework porque não requer ferramentas ou bibliotecas particulares, mantendo um núcleo simples, porém, extensível. O Flask é um micro-framework destinado principalmente a pequenas aplicações com requisitos mais simples, como por exemplo, a criação de um site básico. Ele é projetado para ser fácil de usar, rápido e flexível, e oferece uma grande variedade de recursos para construir aplicações web completas.

<h4 align="center" href="https://www.infonova.com.br/cloud/o-que-e-computacao-em-nevoa/">Núvem e Névoa</h4>

A computação em nuvem é o fornecimento de serviços de computação, incluindo servidores, armazenamento, bancos de dados, rede, software, análise e inteligência, pela Internet (“a nuvem”) para oferecer inovações mais rápidas, recursos flexíveis e economias de escala. Você normalmente paga apenas pelos serviços de nuvem que usa, ajudando a reduzir os custos operacionais, a executar sua infraestrutura com mais eficiência e a escalonar conforme as necessidades da sua empresa mudam.

A névoa é uma nuvem ao nível do solo. Logo, a computação em névoa é a aproximação da nuvem aos dispositivos que recolhem e transmitem dados. O termo computação em névoa ou fog computing foi introduzido pela Cisco em 2013. A computação em névoa é uma infraestrutura de computação descentralizada. Contudo, nela dados, computação, armazenamento e aplicativos estão localizados em algum lugar entre a fonte de dados e a nuvem.

#### 3. Desenvolvimento
O sistema foi desenvolvido na linguagem python, onde foi utilizado a framework flask, além do protocolo de comunicação mqtt. 
Essa imagem é uma representação gráfica de como foi pensado o posto.
![1.jpeg](https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos/blob/main/img/1.jpeg)

O sistema foi pensado da seguinte forma: temos um servidor central que é nossa núvem, e os brokers, que são mais do que brokers pois realizam algumas operações, esses assumem o papel da nossa névoa. Nos brokers temos informações que chegam dos carros e postos, essa comunicação é feita usando o protocolo mqtt. Os carros perguntam para o broker se o posto que está associado a ele tem vaga. O servidor central se comporta como um servidor-cliente, ele está escutando e mandando mensagens para outros brokers, essa comunicação é feita usando uma comunicação tcp com sockets.

![2.jpeg](https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos/blob/main/img/2.jpeg)

Se não tiver vagas, a mensagem é passada para a núvem e ele pergunta para o próximo nó da névoa se os postos ali tem vaga, se tiver insere o carro e a informação e retornada.

![4.jpeg](https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos/blob/main/img/4.jpeg)

Se não tiver vagas novamente, ele pergunta para o outro próximo nó da névoa se aquele posto que está associado a ele tem vagas

![3.jpeg](https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos/blob/main/img/3.jpeg)

A busca de postos nos nós da névoa foi feita usando uma lista circular, de como que sempre quando não encontrado vagas, ela vai perguntar no elemento seguinte se tem vagas, esse processo é feito até que não reste vagas

![5.jpeg](https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos/blob/main/img/5.jpeg)
#### 4. Intruções
##### 4.1 Clonar repositório
```
https://github.com/mauriciomuniz/carregamento-inteligente-de-veiculos-eletricos.git
```
##### 4.2 Executar os arquivos relacionados a broker,servidor central, estações elétricas, carro no diretório de sua pasta. Lembrando que o carro deve ser executado por último
```
python3 [nome do arquivo]
```

##### 4.3 Se utilizar o mesmo computador, pode usar o localhost, se utilizar de outros computadores, então Brokers, Eletric_stations, servers.json devem ser alterado o localhost para o seu hostname


