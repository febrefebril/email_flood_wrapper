''' wrapper para flood de email '''
# -*- coding: utf-8 -*-
import argparse
import sys
# from subprocess import call, check_call
import subprocess

def verificaTamanhosMsg(tamanhoMax, tamanhoMin):
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


def checaParametro(parametros):
    verificaTamanhosMsg(parametros.tamanhoMaxMsg, parametros.tamanhoMinMsg)


def main():

    if len(sys.argv) == 1:
        # roda postal com valores pré-determinados
        servidor = "10.0.0.20"
        print "Será lançado um teste de flood de email com os seguintes", 
        "parametros:"
        print "Tamanho máximo da mensagem: 20 Mb"
        print "Usuários simultâneos (threads): 20"
        print "SSL: 50% das mensagens"
        print "servidor: %s" % servidor
        resposta = raw_input("Deseja rodar os testes contra esses valores?(s/N)")
        if resposta == 's':
            print "rodando o script"
            subprocess.check_call(["postal", "-m", "0", "-t", "20", "-c", "0",
                                   "-f", "templates/remetente.txt",
                                   servidor, "templates/destinatario.txt"])
        # call(["postal", "-m 0", "-t 20", "-c 0", "-s 50",
        #       "-f templates/remetente '10.0.0.20' templates/destinatario"])
        else:
            sys.exit("Boa escolha")
    else:
        # checa os parametros
        parser = argparse.ArgumentParser(
            description='Script usado para floodar email para testar o ASMG.'
            )

        parser.add_argument(  # m
            "-M",
            "--tamanhoMaxMsg",
            help="Tamanho máximo das mensagem em kb. Exemplo: -M 200"
            )

        parser.add_argument(  # M
            '-m',
            '--tamanhoMinMsg',
            help='Tamanho mínimo das mensagens em kb. Exemplo: -m 30'
            )

        parser.add_argument(  # thread
            '-u',
            '--usuariosSimultaneos',
            help='Quantidade de usuários simultâneos. Exemplo: -u 100'
            )

        parser.add_argument(
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

        parser.add_argument(
            '-mpm',
            '--mensagensPorMinuto',
            help='Quantidade de mensagens por minuto. Valor padrão 24000.'
            )

        parser.add_argument(
            '-s',
            '--sslPorcentagem',
            help='Valor da quantidade, em porcentagem, que serão de ssl.' +
            '0 = nenhuma conexão SSL, 100 = todas conexões serão SSL.' +
            'Valor padrão = 0'
            )
        parser.add_argument(
            '-d',
            '--debugEmUmArquivo',
            help='Permite ao usuário especificar um arquivo de debug. com :' +
            'separando os usuários (threads)'
            )
        parser.add_argument(
            '-D',
            '--debugEmUmArquivoPorUsuario',
            help='Permite debugar criando um arquivo por usuário (thread)'
            )
        parser.add_argument(
            '-lr',
            '--listaRemetente',
            help='Arquivo de usuário contendo os remetentes.'
            )

        parser.add_argument(
            '-ld',
            '--listaDestinatario',
            help='Arquivo contento os usuário para qual enviaremos email.'
            )

        parser.add_argument(
            '-srv',
            '--servidorSntp',
            help='Endereço do servidor SNMP que será testado'
            )
        p = parser.parse_args()  # pega os parametros escolhidos pelo usuario
        checaParametro(p)

        # roda postal com valores pré-determinados
        print "Será lançado um teste de flood de email com os seguintes", 
        "parametros:"
        print "tamanho máximo da mensagem: %s kb" % p.tamanhoMaxMsg if p.tamanhoMaxMsg is not None else 0
        print "tamanho mínimo da mensagem: %s kb" % p.tamanhoMinMsg if p.tamanhoMaxMsg is not None else 0 
        print "Usuários simultâneos (threads): %s" % p.usuariosSimultaneos if p.usuariosSimultaneos is not None else 0
        print "Quantidade de mensagens por conexão: %s" % p.mensagensPorConexao if p.mensagensPorConexao is not None else 0
        print "Quantidade de mensagens por minuto: %s" % p.mensagensPorMinuto if p.mensagensPorMinuto is not None else 0
        print "SSL: %s % das mensagens" % p.sslPorcentagem if p.sslPorcentagem is not None else 0
        print "Debug em arquivo unico" if p.debugEmUmArquivo is not None else 0
        print "Debug em vários arquivos" if p.debugEmUmArquivoPorUsuario is not None else 0
        print "Arquivo de remetente: %s" % p.listaRemetente if p.listaRemetente is not None else 0
        print "Arquivo de destinatario: %s" % p.listaDestinatario if p.listaDestinatario is not None else 0
        print "Servidor: %s" % p.servidorSntp if p.servidorSntp is not None else 0
        resposta = raw_input("Deseja rodar os testes contra esses valores?(s/N)")
        if resposta == 's':
            print "rodando o script"
            # subprocess.check_call(["postal", "-m", "0", "-t", "20", "-c", "0",
            #                        "-f", "templates/remetente.txt",
            #                        servidor, "templates/destinatario.txt"])
        else:
            sys.exit("Boa escolha")
main()
