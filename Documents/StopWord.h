#ifndef STOPWORD_H
#define STOPWORD_H
#include <iostream>
#include <fstream>
#include <string.h>
using namespace std;
#include <vector>

class StopWord
{
   public:
     typedef vector<string> documento;
     typedef documento::iterator iterador;
     typedef string::iterator iterador2;

      documento stopwords;
      vector<char> signos;
     StopWord (documento copia);
     int cantidad_signos(string& palabra);
     bool verifica(string& palabra, iterador2 & it);
     void elimina(string& palabra);
     bool encontrar(string palabra);
     void guardar_vocabulario(documento& vocabulario, documento texto);
};

StopWord :: StopWord (documento copia)
{
  stopwords = copia;
    signos.push_back(',');
    signos.push_back(';');
    signos.push_back('.');
    signos.push_back(':');
    signos.push_back('-');
    signos.push_back('{');
    signos.push_back('}');
    signos.push_back('+');
    signos.push_back('-');
    signos.push_back('[');
    signos.push_back(']');
    signos.push_back('*');
    signos.push_back('/');
    signos.push_back('¿');
    signos.push_back('?');
    signos.push_back('¡');
    signos.push_back('!');
    signos.push_back('"');
    signos.push_back('1');
    signos.push_back('2');
    signos.push_back('3');
    signos.push_back('4');
    signos.push_back('5');
    signos.push_back('6');
    signos.push_back('7');
    signos.push_back('8');
    signos.push_back('9');
    signos.push_back('0');
}

int StopWord :: cantidad_signos(string& palabra)
{
  int con = 0;
    for(int i = 0; i<palabra.size(); i++)
    {
        for(int j=0; j<signos.size(); j++)
        {
           if(palabra[i]==signos[j]) con++;
        }
    }
    return con;
}

bool StopWord :: verifica(string& palabra, iterador2 & it)
{
  it = palabra.begin();
  for(int i=0; i<palabra.size(); i++ , it++)
   {
      for(int j=0; j<signos.size(); j++)
      {
         if(palabra[i]==signos[j]) return true;
      }
   }
  return false;
}

void StopWord :: elimina(string& palabra)
{
  int con = cantidad_signos(palabra);
   while(con>0)
   {
      iterador2 it;
      if(verifica(palabra, it))
       {
         palabra.erase(it);
       }
       con--;
   }
}

bool StopWord :: encontrar(string palabra)
{
  iterador it;
  for(it=stopwords.begin(); it!=stopwords.end();it++)
   {
     if(*it==palabra) return true;
   }
  return false;
}

void StopWord :: guardar_vocabulario(documento& vocabulario, documento texto)
{
  iterador it;
  for(it=texto.begin(); it!=texto.end(); it++)
  {
     if(!encontrar(*it))
     {
       vocabulario.push_back(*it);
     }
  }
}

#endif
