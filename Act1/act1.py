import re

def hex_to_dec(hex_str):
    # Validar numero hexa
    if re.fullmatch(r'[0-9A-Fa-f]+', hex_str):
        return str(int(hex_str, 16))
    return "0"  #Si no es valido es 0

def dec_to_hex(dec_str):
    return hex(int(dec_str))[2:].upper()

def procesarArchivo(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split(',')
            
            #Hexa a decimal
            hex_values = parts[0].split(':')
            decimal_values = [hex_to_dec(val) for val in hex_values]
            
            #Sacar segunda cadena
            text_value = parts[2] if len(parts) > 2 else ""
            
            #Decimal a hexa
            last_four_dec = parts[-1].split('.')
            hex_converted = [dec_to_hex(num) if num.isdigit() else "0" for num in last_four_dec]
            
            #Dar formato para el archivo
            output_line = f"{text_value} : {' : '.join(decimal_values)} : {'.'.join(hex_converted)}\n"
            outfile.write(output_line)

# Archivos de entrada y salida
archivoEntrada = "prueba2.txt"
archivoSalida = "correcion.txt"

procesarArchivo(archivoEntrada, archivoSalida)
print("Listo")
