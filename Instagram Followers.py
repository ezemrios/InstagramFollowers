# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:10:40 2020

@author: e.rios.kaliman
"""

import time
from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pandas import ExcelWriter

user=environ["USERPROFILE"]
ch_options=webdriver.ChromeOptions()
ch_options.add_argument("user-data-dir=" + user +
                     "\\AppData\\Local\\Google\\Chrome\\User Data")
driver=webdriver.Chrome(executable_path=r'C:\Users\e.rios.kaliman\Desktop\chromedriver.exe',
                          options=ch_options)

index = 0
lista_users=[[],[]]
lista_cuentas=[]
print("Se podran buscar dos cuentas de Instagram para comparar")

for i in range(2):
    usuario_buscar=input("Ingrese el nombre de usuario: ")
    lista_cuentas.append(usuario_buscar)
    
for cuenta in lista_cuentas:

    driver.get("https://www.instagram.com/")
    search=driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
    search.send_keys(Keys.ENTER)
    search.send_keys(cuenta)
    time.sleep(5)
    usuario_click=driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]/div/div[2]')
    usuario_click.click()
    time.sleep(10)
    cantidad=driver.find_element_by_xpath("//a[@href='/"+cuenta+"/followers/']").text
    cantidad_usuarios=""
    letra=""
    
    for number in cantidad:
        if number.isdigit():
            cantidad_usuarios=cantidad_usuarios+number
        elif number=="k" or number=="m":
            letra=letra+number
               
    if letra=="":
        cantidad_usuarios=int(cantidad_usuarios)
    elif letra=="k":
        cantidad_usuarios=int(cantidad_usuarios)*1000
    elif letra=="m":
        cantidad_usuarios=int(cantidad_usuarios)*1000000
        
    time.sleep(5)    
    seguidores_boton=driver.find_element_by_xpath("//a[@href='/"+cuenta+"/followers/']")
    seguidores_boton.click()
    time.sleep(5)
        
    scr1 = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
    for follower in range(int(cantidad_usuarios/11)):
        try:
            time.sleep(2)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        
        except TimeoutException:
            break
    
    
    Users=driver.find_elements_by_xpath("(//a[contains(@class,'0imsa ')])")
    
    for i in Users:
        lista_users[index].append(i.text)
        
    index +=1


lista_repetidos=[]

for user in lista_users[0]:
    if user in lista_users[1]:
        lista_repetidos.append(user)

dicc={lista_cuentas[0]:lista_users[0],lista_cuentas[1]:lista_users[1],"Repetidos":lista_repetidos}
df_usuarios1=pd.DataFrame(dicc[lista_cuentas[0]])
df_usuarios2=pd.DataFrame(dicc[lista_cuentas[1]])
df_usuarios_repetidos = pd.DataFrame(dicc["Repetidos"])

df_usuarios1.rename(columns={0:lista_cuentas[0]},inplace=True)
df_usuarios2.rename(columns={0:lista_cuentas[1]},inplace=True)
df_usuarios_repetidos.rename(columns={0:"Usuarios repetidos"},inplace=True)




with ExcelWriter(r'C:\Users\e.rios.kaliman\Downloads\'Instagram_Followers.xls') as writer:
    df_usuarios1.to_excel(writer, sheet_name=lista_cuentas[0],index=False)
    df_usuarios2.to_excel(writer, sheet_name=lista_cuentas[1],index=False)
    df_usuarios_repetidos.to_excel(writer, sheet_name="Usuarios repetidos",index=False)














