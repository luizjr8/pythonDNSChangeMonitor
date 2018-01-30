# cli-domain-monitor
# @luizjr8
# 2018-01-30

# Libs
import argparse
from threading import Timer,Thread,Event
import dns.resolver
import socket

# Argumentos
args = argparse.ArgumentParser()

args.add_argument('domain')
args.add_argument('entry')
args.add_argument('--new', '-n')

class DomainChecker(Thread):
	max_tentativas = 500
	tempo_tentativas = 5
	dns_root = "google-public-dns-a.google.com"

	def __init__(self, dominio, entrada, valor):
		# Setup
		self.dominio = dominio
		self.entrada = entrada
		self.valor = valor
		self.tentativas = 0
		self.ultimo_valor = None
		
		# Executa ação
		self.thread = Timer(self.tempo_tentativas,self.checarDominio)
		self.thread.start()
		
	def checarDominio(self):
		print("Checando mudança entrada %s no domínio %s." % (self.entrada, self.dominio))
		self.tentativas += 1

		resolver = dns.resolver.Resolver()
		resolver.nameservers=[socket.gethostbyname(self.dns_root)]
		
		try:
			for data in resolver.query(self.dominio, self.entrada):
				# Primeiro Valor
				if(self.ultimo_valor == None):
					self.ultimo_valor = data

				# Checa se o valor do DNS mudou	
				if(data != self.ultimo_valor or data == self.valor):
						print("DNS atualizado!")

			self.ultimo_valor = data
		except Exception as e:
			print("Erro:",e)
		
		if(self.tentativas < self.max_tentativas):
			self.thread = Timer(self.tempo_tentativas,self.checarDominio)
			self.thread.start()	

if __name__ == '__main__':
		# Argumentos
		args = args.parse_args()
		
		# Valores
		dominio = args.domain
		entrada = args.entry
		valor = args.new
		
		# Output
		print("Checar a entrada %s no domínio %s (Valor antigo: %s)" % (args.entry,args.domain,args.new))

		# Executa
		monitor = DomainChecker(dominio,entrada,valor)