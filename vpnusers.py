#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------
# Сбор статистики в файле о подключённых пользователях и их ip из OpenVPN
#------------------------------------------------------------------------------------------------

import os, sys

#------------------------------------------------------------------------------------------------

# Функция работы с файлами OpenVPN
def run():
  users = []
  # Получение списка ip адресов пользователей и времени их сеанса (текущие подключения)
  if os.path.isfile('/etc/openvpn/openvpn-status.log'):
    for line in list(open('/etc/openvpn/openvpn-status.log')):
      if line.find('ROUTING') != -1: break;
      if line.find('UNDEF') != -1:
        users.append(' ' + ((line.split(',')[1]).split(':')[0]) + ' ' + (line.split(',')[4]).replace("\n",""))

  # Получение имён пользователей по их ip адресу из лога
  i = len(users)
  if os.path.isfile('/var/log/openvpn.log'):
    for line in reversed(list(open('/var/log/openvpn.log'))):
      if i == 0: break;
      if line.find('TLS: Username/Password authentication succeeded') != -1:
        log_ip = ((line.split(' ')[2]).split(':')[0])
        for num in range(len(users)):
          if log_ip == users[num].split(' ')[1]:
            i = i - 1
            users[num] = (line.split(' ')[9]).replace("'",'') + users[num]
            break

  # Вывод результата
  for num in range(len(users)):
    print(users[num])

#------------------------------------------------------------------------------------------------

# Запуск программы
if __name__ =='__main__':
  run()
