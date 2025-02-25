# Sistema-de-inventario
## Descripción
Este es un sistema simple de facturación e inventario donde puedes agregar y editar productos en el inventario, generar facturas, y calcular el monto a cancelar y el cambio correspondiente, adicional a esto tambien se puede generar una factura en un archivo pdf.
### Funcionalidades:
### Inventario:
  * Agregar productos (nombre,proveedor, precio, costo, stock).
  * Editar productos (nombre,proveedor, precio, costo, stock).
  * Actualizar la lista de inventario en la tabla (nombre,proveedor, precio, costo, stock).
### Factura:
  * Seleccionar productos del inventario para generar una factura.
  * Calcular automáticamente la suma total de la factura.
  * Mostrar el monto a cancelar y el cambio según el pago realizado.
### Requisitos:
   * Python 3.x
   * Tkinter (para la interfaz gráfica)
   * SQLite (para la base de datos local)
### Instalación:
   * Clona el repositorio a tu máquina local:
   ```git clone https://github.com/andylo94/Sistema-de-inventario.git```
   * Instala las dependencias necesarias:  
   ```pip install sqlite3```  
   ```pip install tk```  
   ```pip install reportlab```
## Uso:
   * __Si no deseas instalar Python ni ejecutar el código manualmente, puedes utilizar el ```exe``` que esta en el repositorio__
   * Una vez copiado el repositorio y abierto en el editor de código de tu preferencia, el programa se ejecuta desde index.py. Desde aquí, puedes navegar por las ventanas de ventas e inventario, ver productos facturados y mirar la lista de productos en disponibles en la base de datos.
## Contribuciones
Si deseas contribuir a este proyecto, siéntete libre de hacer un fork y enviar un pull request con tus mejoras.
