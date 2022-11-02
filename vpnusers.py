#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------
# Сбор статистики в файле о подключённых пользователях и их ip из OpenVPN
#------------------------------------------------------------------------------------------------

import os, sys
openvpn_status_file = '/etc/openvpn/openvpn-status.log'
openvpn_log_file = '/var/log/openvpn.log'
result_log_file = '/var/log/vpnusers.log'

#------------------------------------------------------------------------------------------------

# Функция работы с файлами OpenVPN
def run():
  users = []
  # Получение списка ip адресов пользователей и времени их сеанса (текущие подключения)
  if os.path.isfile(openvpn_status_file):
    for line in list(open(openvpn_status_file)):
      if line.find('ROUTING') != -1: break;
      if line.find('UNDEF') != -1:
        users.append(' ' + ((line.split(',')[1]).split(':')[0]) + ' ' + (line.split(',')[4]).replace("\n",""))
    else: sys.exit(0)

  # Получение имён пользователей по их ip адресу из лога
  i = len(users)
  if os.path.isfile(openvpn_log_file):
    for line in reversed(list(open(openvpn_log_file))):
      if i == 0: break;
      if line.find('TLS: Username/Password authentication succeeded') != -1:
        log_ip = ((line.split(' ')[2]).split(':')[0])
        for num in range(len(users)):
          if log_ip == users[num].split(' ')[1] and users[num].split(' ')[0] == '':
            i = i - 1
            users[num] = (line.split(' ')[9]).replace("'",'') + users[num]
            break
    else: sys.exit(0)

  # Вывод результата в лог
  with open(result_log_file,'w') as logfile:
    for num in range(len(users)):
      if users[num].split(' ')[0] != '':
        logfile.write(users[num]+'\n')

#------------------------------------------------------------------------------------------------

# Запуск программы
if __name__ =='__main__':
  run()
