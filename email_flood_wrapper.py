''' wrapper para flood de email '''
# -*- coding: utf-8 -*-
import argparse
import sys
# from subprocess import call, check_call
import subprocess
import os

def verificaTamanhosMsg(tamanhoMax, tamanhoMin):
    ''' verifica o tamanho dos parametros por possível erro '''
    if tamanhoMax is not None and tamanhoMin is not None:
        if tamanhoMax < tamanhoMin:
            sys.exit(
                'ERRO: tamanho máximo da mensagem não deve ser menor' +
                ' que o tamanho mínimo'
            )
        elif tamanhoMin > tamanhoMax:
            sys.exit(
                'ERRO: tamanho mínimo da mensagem não deve ser maior' +
                'que o tamanho máximo')


def configuraArgumentos(p):
    ''' Configura os argumentos do script '''
    p.add_argument(  # m
        "-M",
        "--tamanhoMaxMsg",
        help="Tamanho máximo das mensagem em kb. Exemplo: -M 200"
        )

    p.add_argument(  # M
        '-m',
        '--tamanhoMinMsg',
        help='Tamanho mínimo das mensagens em kb. Exemplo: -m 30'
        )

    p.add_argument(  # thread
        '-u',
        '--usuariosSimultaneos',
        help='Quantidade de usuários simultâneos. Exemplo: -u 100'
        )

    p.add_argument(
        '-mc',
        '--mensagensPorConexao',
        help='Para mandar mais de uma mensagem por conexão SMTP.' +
             'O valor default é 1. O valor -1 significa mandar' +
             'indefinitivamente(4 Bilhões). Se um valor > 1 ' +
             'é especificado, então a quantidade de envios por cada ' +
             'conexão é um número randomico entre 1 e o valor ' +
             'especificado. Para procurar bug use o valor 0 e ' +
             'deixe-o radando por uma semana. O valor 0 significa ' +
             'disconectar do servidor sem enviar mandar nenhuma mensagem'
        )

    p.add_argument(
        '-mpm',
        '--mensagensPorMinuto',
        help='Quantidade de mensagens por minuto. Valor padrão 24000.'
        )

    p.add_argument(
        '-s',
        '--sslPorcentagem',
        help='Valor da quantidade, em porcentagem, que serão de ssl.' +
        '0 = nenhuma conexão SSL, 100 = todas conexões serão SSL.' +
        'Valor padrão = 0'
        )
    p.add_argument(
        '-d',
        '--debugEmUmArquivo',
        action='store_true',
        default=False,
        help='Permite ao usuário especificar um arquivo de debug. com :' +
        'separando os usuários (threads)'
        )
    p.add_argument(
        '-D',
        '--debugEmUmArquivoPorUsuario',
        action='store_true',
        default=False,
        help='Permite debugar criando um arquivo por usuário (thread)'
        )
    p.add_argument(
        '-lr',
        '--listaRemetente',
        help='Arquivo de usuário contendo os remetentes.'
        )

    p.add_argument(
        '-ld',
        '--listaDestinatario',
        help='Arquivo contento os usuário para qual enviaremos email.'
        )

    p.add_argument(
        '-srv',
        '--servidorSntp',
        required=True,
        help='Endereço do servidor SNMP que será testado'
        )


def checaParametro(parametros):
    ''' Checa os parametros '''
    verificaTamanhosMsg(parametros.tamanhoMaxMsg, parametros.tamanhoMinMsg)
    # verifica existencia do servidor
    if parametros.servidorSntp is None:
        sys.exit("ERRO: Servidor sntp está faltando!" +
                 "único parametro necessário. Exemplo: -srv 10.0.0.20")
    # seta tamanho máximo da mensagem
    if parametros.tamanhoMaxMsg is None:
        parametros.tamanhoMaxMsg = 20480
    # seta tamanho mínimo da mensagem
    if parametros.tamanhoMinMsg is None:
        parametros.tamanhoMinMsg = 5
    # seta threads
    if parametros.usuariosSimultaneos is None:
        parametros.usuariosSimultaneos = 1
    # seta quantidade de mensagens por conexão
    if parametros.mensagensPorConexao is None:
        parametros.mensagensPorConexao = -1
    # seta quantidade de mensagens por minuto
    if parametros.mensagensPorMinuto is None:
        parametros.mensagensPorMinuto = 24000
    # seta lista de remetentes
    if parametros.listaRemetente is None:
        parametros.listaRemetente = 'templates/remetentes.txt'
    # seta lista de destinatários
    if parametros.listaDestinatario is None:
        parametros.listaDestinatario = 'templates/destinatario.txt'


def imprimeParametros(parametros):
    ''' Printa todos os parametros '''
    print "tamanho mínimo da mensagem: %s kb" % parametros.tamanhoMinMsg
    print "tamanho máximo da mensagem: %s kb" % parametros.tamanhoMaxMsg
    print "Usuários simultâneos (threads): %s" % parametros.usuariosSimultaneos
    print "Quantidade de mensagens por conexão: %s" % parametros.mensagensPorConexao
    print "Quantidade de mensagens por minuto: %s" % parametros.mensagensPorMinuto
    print "SSL: %s porcento das mensagens" % parametros.sslPorcentagem
    print "Arquivo de destinatario: %s" % parametros.listaDestinatario
    print "Arquivo de remetente: %s" % parametros.listaRemetente
    print "Servidor: %s" % parametros.servidorSntp


def main():

    euid = os.geteuid()
    if euid != 0:
        sys.exit("ERRO: este script deve ser usado com privilégio root :D")
    if len(sys.argv) == 1:
        sys.exit("ERRO: Servidor sntp está faltando! " +
        "Este é o único parametro necessário.\nExemplo:" +
        " python email_flood_wrapper -srv 10.0.0.20\n" +
        "para mais ajuda use: python email_flood_wrapper -h")
        # # roda postal com valores pré-determinados
        # servidor = "10.0.0.20"
        # print "Será lançado um teste de flood de email com os seguintes",
        # "parametros:"
        # print "Tamanho máximo da mensagem: 20 Mb"
        # print "Usuários simultâneos (threads): 20"
        # print "SSL: 50% das mensagens"
        # print "servidor: %s" % servidor
        # resposta = raw_input(
        #     "Deseja rodar os testes contra esses valores?(s/N)"
        #     )
        # if resposta == 's':
        #     print "rodando o script"
        #     subprocess.check_call(
        #         ["postal", "-m", "0", "-t", "20", "-c", "0",
        #          "-f", "templates/remetente.txt",
        #          servidor, "templates/destinatario.txt"]
        #         )
        # # call(["postal", "-m 0", "-t 20", "-c 0", "-s 50",
        # #       "-f templates/remetente '10.0.0.20' templates/destinatario"])
        # else:
        #     sys.exit("Boa escolha")
    else:
        # checa os parametros
        parser = argparse.ArgumentParser(
            description='Script usado para floodar email para testar o ASMG.',
            epilog="Parametros dentro de [] não são obrigatórios"
            )
        configuraArgumentos(parser)
        p = parser.parse_args()  # pega os parametros escolhidos pelo usuario
        checaParametro(p)
        imprimeParametros(p)
        resposta = raw_input("Deseja rodar os testes contra esses parametros?(s/N)")
        # roda postal com valores pré-determinados
        if resposta == 's':
            print "rodando o script"
            print p.servidorSntp
          #  subprocess.check_call(
          #      ["postal", "-m", "0", "-t", "20", "-c", "0",
          #       "-f", "templates/remetente.txt",
          #       p.servidorSntp, "templates/destinatario.txt"]
          #      )
            subprocess.check_call(
                ["postal",
                 "-m", str(p.tamanhoMaxMsg),
                 "-M", str(p.tamanhoMinMsg),
                 "-t", str(p.usuariosSimultaneos),
                 "-c", str(p.mensagensPorConexao),
                 "-f", str(p.listaRemetente),
                 str(p.servidorSntp), str(p.listaDestinatario)]
                )

        else:
            sys.exit("Boa escolha")
main()
