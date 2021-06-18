### 0.1.4
#### February 15 2020

Added support for enum valiation in schema file. These go into an "extra" data section of the YAML. Note that these have to be unpacked along with the other information now.

### 0.1.3
#### December 1 2020

Fixed parsing of URLs, the ":" delimiter was messing up the string splitting.

### 0.1.4.1
#### June 1 2021

Fixed parser to accept 3 args instead of 2.

### 0.1.4.2
#### June 2 2021

Removed line separators from entries.py in markdown converter.
Fixed line separators issue. (no excessive line breaks in order to generate html properly)

### 0.1.5
#### June 8 2021

The program now runs with all the needed columns and parameters with both types of variables.
It took one week but we did it.
Two interns on a language they barely knew.
Lets hope work keeps up!

More changes have been made:
- Now the mandatory variable is itself mandatory else it throws an exception
- Now the variables are put in alphabetical order

### NEEDED CHANGES

- Poder adicionar os niveis que quisermos(verificar identação)
- Adicionar mapas(criar nova tabela)
- Embed tables para mais que um nivel
- Adicionar hiperligações para tipos complexos(na tabela principal)