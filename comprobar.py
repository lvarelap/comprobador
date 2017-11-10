# -*- coding: utf-8 -*-
import MySQLdb


conn = MySQLdb.connect("localhost", "root", "root69", "OracleCheckList",charset='utf8')
cursor = conn.cursor()

print "====================================================================="
print "                          REVISIÓN DE SERVIDORES"
print "====================================================================="

imprimir = 0

# S1: Comprobar que todos los servidores tiene montado productos Oracle (columnas U,V y W).
print "S1: Comprobar que todos los servidores tiene montado productos Oracle (columnas U,V y W)."
print "========================================================================================="

query = "select nombre"
query = query + " from ( select distinct hostname nombre"
query = query + "          from servidores"
query = query + "         where virtualizacion = 'No virtualizado'"
query = query + "         union all"
query = query + "        select distinct hostname_virtual nombre"
query = query + "          from servidores"
query = query + "         where virtualizacion = 'Virtualización física'"
query = query + "            or virtualizacion = 'Virtualización lógica') servidor"
query = query + " where servidor.nombre not in (select distinct servidor from basedatos)"
query = query + "  and servidor.nombre not in (select distinct servidor from weblogic)"

#print query
print "***** Comprobamos que los servidores tienen productos Oracle *****"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Obcomprobar_hostnamestenemos todos los registros en unprina lista de listas
    resultados = cursor.fetchall()
    for registro in resultados:
        if imprimir == 0:
            print "Los servidores "
        servidor = registro[0]
        print "%s, " % servidor
        imprimir = 1
    if imprimir == 1:
        print "   no tienen declarados productos oracle"
        imprimir = 0
except:
    print "ERROR (S1): Comprobar que todos los servidores tiene montado productos Oracle (columnas U,V y W)."





print "****** Comporbamos que no se repiten nombres de servidores fisicos y virtuales ****"
query = "select id from servidores where hostname = hostname_virtual;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Obcomprobar_hostnamestenemos todos los registros en una lista de listas
    resultados = cursor.fetchall()
    for registro in resultados:
        if imprimir == 0:
            print "Los sevidores "
        servidor = registro[0]
        print " %s," % servidor
        imprimir = 1
    if imprimir == 1:
        print " se llama igual que el servidor virtual que lo aloja"
        imprimir = 0
except:
    print "ERROR (S1.1): Comprobar que todos los servidores tiene montado productos Oracle (columnas U,V y W)."


print "# comprobamos que no haya más de dos niveles #"
# comprobamos que no haya más de dos niveles
query = "select distinct hostname "
query = query + "  FROM servidores "
query = query + "   WHERE virtualizacion != 'No virtualizado' "
query = query + "     and hostname_virtual  in (select distinct hostname"
query = query + "                        from servidores "
query = query + "                       where virtualizacion != 'No virtualizado');"



try:
    # Ejecutamos el comando
    cursor.execute(query)
    #comprobar_hostnamestenemos todos los registros en una lista de listas
    resultados = cursor.fetchall()

    for registro in resultados:
        repeticion = registro[0]

        print "El servidor "
        print " %s " %repeticion
        print "es forma parte de una estructura de 3 niveles " 

except:
    print "Error en la revisión de los tres niveles"


query = "select hostname_virtual nombre, count(id) cantidad from servidores s1 where hostname_virtual is not null group by hostname_virtual order by cantidad desc;"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Obcomprobar_hostnamestenemos todos los registros en una lista de listas
    resultados = cursor.fetchall()

    for registro in resultados:
        repeticion = registro[1]
        servidor = registro[0]
        if repeticion >= 2:
            if imprimir == 0:
                print "Los sevidores "
            print " %s," % servidor
            imprimir = 1
    if imprimir == 1:
        print " estan repertido como servidor virtual en varias ocasiones ¿Es correcto? "
        imprimir = 0
except:
    print "ERROR (S1.2): Comprobar que todos los servidores tiene montado productos Oracle (columnas U,V y W)."


query = "select count(distinct(bd.id)) from basedatos bd, servidores sr where (sr.hostname = bd.servidor or sr.hostname_virtual = bd.servidor);"
query1 ="select count(distinct(id)) from basedatos;"

print "***** Comprobamos que se declaran las mismas BBDD en los dos hojas *****"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Obcomprobar_hostnamestenemos todos los registros en una lista de listas
    servidores = cursor.fetchall()

    cursor.execute(query1)
    basededatos = cursor.fetchall()
    if servidores[0] != basededatos[0]:
        print "No se han declarado las misas bbdd en los servidores y en las BBDD"
        print "%s Servidores " %servidores[0]
        print "%s Base de Datos" %basededatos[0]
except:
        print "Error: Comparar Servidores/BBDD"


# S2: Comprobar que todos los campos obligatorios están cumplimentados
print "S2: Comprobar que todos los campos obligatorios están cumplimentados"
print "================================================================"

query = "SELECT id "
query = query + "FROM servidores "
query = query + "WHERE (hostname IS NULL or hostname = '')"
query = query + "OR (marca IS NULL OR marca = '')"
query = query + "OR (modelo IS NULL OR modelo = '') "
query = query + "OR (tecnologia IS NULL or tecnologia = '') "
query = query + "OR cpu_fisico IS NULL "
query = query + "or prodesador_fisico IS NULL "
query = query + "or cores_fisico IS NULL "
query = query + "or (virtualizacion IS NULL OR virtualizacion ='') "
query = query + "or (so IS NULL OR so ='') "
query = query + "or (arquitectura IS NULL OR arquitectura = '');"


print "***** Comprobamos los campos Obligatorios *****"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Obcomprobar_hostnamestenemos todos los registros en una lista de listas
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Los Servidores "
        servidor = registro[0]
        print " %s," % servidor
        imprimir = 1
    if imprimir == 1:
        print " no tiene declarados todos los campos obligatorios"
        imprimir = 0
except:
    print "Error: Primero los campos obligatorios que no están sujetos a condiciones."





# Comprobar la correcta definición de las no virtualizadas
query = "select id"
query = query + "  from servidores"
query = query + " where virtualizacion = 'No virtualizado'"
query = query + "   and hostname_virtual is not null"
query = query + "    or hostname_virtual = '';"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Los servidores"
        ser = registro[0]
        print " %s," % ser
        imprimir = 1
    if imprimir == 1:
        print " definidos como no virtuales y se les ha declarado hostname_virtual"
        imprimir = 0
except:
    print "Error: servidores con hostname_virtual"



print "Comprobamos que las maquinas virtualizadas tienen tambien los cores calculados."

query = "SELECT id "
query = query + "FROM servidores "
query = query + "WHERE (virtualizacion = 'Virtualización lógica' "
query = query + "OR virtualizacion = 'Virtualización física') "
query = query + "AND ((hostname_virtual IS NULL OR hostname_virtual ='' ) "
query = query + "OR (cores_virtual IS NULL OR cores_virtual = 0) "
query = query + "OR (total_cores_virtual IS NULL or total_cores_virtual = 0))"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Los servidores "
        ser = registro[0]
        print "%s, " % ser
        imprimir = 1
    if imprimir == 1:
        print " comprobar virtualizacion"
        imprimir = 0
    # print "Error4"
except:
    print "Error: Comprobamos que las máquinas virtualizadas tienen también los cores calculados."


# Comprobamos que los Clueste estan bien definidos
query = "select id "
query = query + "from servidores "
query = query + " where arquitectura = 'Cluster'"
query = query + " and (nombre_cluster is null or tipo_cluster is null)"

try:
    # Ejecutamos el cselect id, descrip_servicio from basedatos;

    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Los servidores "
        ser = registro[0]
        print " %s," % ser
        imprimir = 1
    if imprimir == 1:
        print " tiene el cluster mal definido"
        imprimir = 0
except:
    print "Error: Comprobamos que las máquinas virtualizadas tienen también los cores calculados."

# Comprobamos que el cluester tiene 2 máquinas por lo menos.

query = "select nombre_cluster, count(hostname)"
query = query + "  from servidores"
query = query + " where arquitectura = 'Cluster'"
query = query + "   group by nombre_cluster;"

try:
	cursor.execute(query)
	resultados = cursor.fetchall()

	for registro in resultados:
		numero = registro[1]
		if numero < 2:
			print "* El cluster %s tiene menos de 1 servidor definido" %registro[0]
		

except:
	 print "Error: Comprobamos el numero de servidores por cluste."


print "S4: Comprobar que las máquinas No virtualizadas sólo aparecen una vez"
print "======================================================================"
query = "select hostname, count(id)"
query = query + " from servidores"
query = query + " where virtualizacion = 'No virtualizado'"
query = query + " group by hostname"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ser = registro[0]
        val = registro[1]
        if val > 1:
            if imprimir == 0:
                print "Los servidores "
            print "%s,  esta mas de %s veces " %(ser, val)
            imprimir = 1
    if imprimir == 1:
        print " y son máquinas no vortuales"
        imprimir = 0
except:
    print "Error (S4): comprobando los servidore no virtuales."

print "S11: Comprobar que las máquinas virtuales físicas no sobrepasen el número de cores"
print "=================================================================================="
query = "select hostname, cpu_fisico * prodesador_fisico, sum(cores_virtual)"
query = query + " from servidores"
query = query + " where virtualizacion = 'Virtualización física'"
query = query + " group by hostname, cpu_fisico * prodesador_fisico;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        ser = registro[0]
        ncf = registro[1]
        ncv = registro[2]
        cf = registro[1]
        cv = registro[2]
        if ncv > ncf:
            print "Servidor %s, tiene %s cores virtualizado y %s fisico" %(ser, cv, cf)
except:
    print "Error (S11): Cores físicos sobrepasados."

print "S11.1: Comprobar que las máquinas virtuales lógicas no sobrepasen el número de cores del servidor"
print "=================================================================================="
query = "select hostname, hostname_virtual, cpu_fisico * prodesador_fisico, cores_virtual"
query = query + " from servidores"
query = query + " where virtualizacion = 'Virtualización lógica'"
query = query + " and cpu_fisico * prodesador_fisico < cores_virtual;"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        ser = registro[0]
        hov = registro[1]
        cf = registro[2]
        cv = registro[3]
        print "Servidor %s, tiene más cores que su anfitrón fisico %s" %(hov, ser)
except:
    print "Error (S11.1): Cores físicos sobrepasados."
    print query;

# S6: Comprobar que la Tecnología coincide con las tecnologías por defecto.
print "S6: Comprobar que la Tecnología coincide con las tecnologías por defecto"
print "========================================================================"
query = "select id"
query = query + " from servidores"
query = query + " where tecnologia not in( select valor from datos where dominio = 'Tecnología servidor');"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        ser = registro[0]
        print "Servidor %s, no tiene una tecnologia correcta" %ser
except:
    print "Error (S6): Comprobar que la Tecnología coincide con las tecnologías por defecto"

# S7: Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --
print "S7: Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --"
print "========================================================================"
query = "select id"
query = query + " from servidores"
query = query + " where so = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query + "  or tipo_cluster = '-- NO ENCUENTRO MI OPCIÓN --';"


try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        ser = registro[0]
        if imprimir == 1:
            print "Los servidores "
            imprimir = 0

        print "%s," %ser
    if imprimir == 0:
        print  "tinen campos NO ENCUENTRO MI OPCION"
except:
    print "Error (S7): Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --"

# S9: Comprobar que en los Clustes al menos hay definidos 2 máquinas
print "S9: Comprobar que en los Clustes al menos hay definidos 2 máquinas"
print "========================================================================"
query = "select nombre_cluster, count(id)"
query = query + " from servidores"
query = query + " group by nombre_cluster"

try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        cluster = registro[0]
        numero = int(registro[1])
        if cluster:
            if numero == 1:
                if imprimir == 1:
                    print "Los clusters "
                    imprimir = 0
                print "%s, " %cluster
    if imprimir == 0:
        print "tendria que tener otra instancia"

except:
    print "Error (S9): Comprobar que en los Clustes al menos hay definidos 2 máquinas"


# S10: Comprobar que el tipo de Cluste está definido entre los que se han declarado
print "S10: Comprobar que el tipo de Cluste está definido entre los que se han declarado"
print "================================================================================="
query = "select id"
query = query + "  from servidores"
query = query + " where tipo_cluster not in (select valor from datos where dominio = 'Tipo de Cluster');"

try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        if imprimir == 1:
            print "Los servidores "
            imprimir = 0
        servidor = registro[0]
        print "%s," %servidor
    if imprimir == 0:
        print " tiene un tipo de cluster no definido"
except:
    print "Error (S10): Comprobar que el tipo de Cluste está definido entre los que se han declarado"


print "S10.1: Comprobar que los nodos del Cluste son iguales (marca, modelo, ....)"
print "================================================================================="
query = "select s1.hostname, s2.hostname, s1.nombre_cluster"
query = query + "  from servidores s1, servidores s2"
query = query + " where s1.nombre_cluster is not null"
query = query + "   and s2.nombre_cluster is not null"
query = query + "   and s1.nombre_cluster = s2.nombre_cluster"
query = query + "   and s1.id > s2.id"
query = query + "   and (s1.marca != s2.marca"
query = query + "     or s1.modelo != s2.modelo"
query = query + "     or s1.tecnologia != s2.tecnologia"
query = query + "     or s1.cpu_fisico != s2.cpu_fisico"
query = query + "     or s1.prodesador_fisico != s2.prodesador_fisico)"
query = query + "   order by s1.nombre_cluster;"

try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor1 = registro[0]
        servidor2 = registro[1]
        cluster   = registro[2]
        print "Los servidores "
        print servidor1
        print servidor2        
        print " forman parte del cluste "
        print cluster
        print "y están definidos de forma distinta."
except:
    print "ERROR (S10.1): Comprobar que los nodos del Cluste son iguales (marca, modelo, ....)"



# s12: Comprobar que no se repiten nombre de Servidores.
print "S12: Comprobar que no se repiten nombre de Servidores."
print "======================================================"
query = "select hostname, count(id) "
query = query + "  from servidores "
query = query + " where virtualizacion = 'No virtualizado' "
query = query + " group by hostname ;"

# En primer lugar miramos que no se repitan el nombre de los servidores No Virtuales

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor = registro[0]
        veces = int(registro[1])
        if servidor:
            if veces > 1:
                print "El servidor %s se repite %i de una vez" % (servidor,veces)
except:
    print "Error (S12): En primer lugar miramos que no se repitan el nombre de los servidores No Virtuales."

# Comprobamos ahora que un servidor físico no se repite tb como servirod virtual
query = "select sfisico.hostname"
query = query + "  from (select hostname"
query = query + "          from servidores "
query = query + "         where virtualizacion = 'No virtualizado') sfisico"
query = query + "     , (select hostname_virtual"
query = query + "         from servidores "
query = query + "        where virtualizacion = 'Virtualización física'"
query = query + "           or virtualizacion = 'Virtualización lógica') svirtual"
query = query + " where sfisico.hostname = svirtual.hostname_virtual;"

#

try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor = registro[0]
        if servidor:
            if imprimir == 1:
                print "Los servidores "
                imprimir = 0
            print "%s, " % servidor
    if imprimir == 0:
        print " se repite como fisico y virtual"

except:
    print "Error (S12.2): En primer lugar miramos que no se repitan el nombre de los servidores No Virtuales."


# s13: Comprobamos que los sevidores físicos soportan más de un servidor virtual
print "S13: Comprobamos que los sevidores físicos soportan mas de un servidor virtual"
print "======================================================"
query = "select hostname, count(id) from servidores where virtualizacion != 'No virtualizado' group by hostname;"


# En primer lugar miramos que no se repitan el nombre de los servidores No Virtuales

try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor = registro[0]
        veces = int(registro[1])
        if servidor:
            if veces <= 1:
                if imprimir == 1:
                    print "Los servidores "
                    imprimir = 0
                print "%s, " % servidor
    if imprimir == 0:
        print " solo tienen 1 servidor virtual ¿es correcto?"
except:
    print "Error (S13): Error al contar los servidores virtuales    ."


# s14: Comporbamos que servidores con la misma marca y modelo están igual definidos
print "s14: Comporbamos que servidores con la misma marca y modelo estan igual definidos"
print "======================================================"

query = "select distinct s1.modelo"
query = query + "  from servidores as s1"
query = query + "     , servidores as s2"
query = query + "  where s1.marca = s2.marca"
query = query + "   and s1.modelo = s2.modelo"
query = query + "   and (s1.tecnologia != s2.tecnologia"
query = query + "     or s1.cpu_fisico != s2.cpu_fisico"
query = query + "     or s1.prodesador_fisico != s2.prodesador_fisico);"


try:
    # Ejecutamos el comando
    imprimir = 1
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor = registro[0]
        if imprimir == 1:
            print "Los siguientes modelos de servidores están definidos de forma ambigua"
            imprimir = 0      
        print " %s" % servidor
    if imprimir == 0:
        print "¿Es correcto"
except:
    print "ERROR 14: Comporbamos que servidores con la misma marca y modelo estan igual definidos"


# s15: Comprobamos que un mismo servidor que aparece en mas de una linea esta definido de la misma forma
print "s15: Comprobamos que un mismo servidor que aparece en mas de una linea esta definido de la misma forma"
print "======================================================"

query = "select distinct s1.hostname, s1.id, s2.id"
query = query + "  from servidores s1"
query = query + "     , servidores s2"
query = query + " where s1.id != s2.id"
query = query + "   and s1.id > s2.id"
query = query + "   and s1.hostname = s2.hostname"
query = query + "   and (s1.marca != s2.marca"
query = query + "    or  s1.modelo != s2.modelo"
query = query + "    or  s1.tecnologia != s2.tecnologia"
query = query + "    or  s1.cpu_fisico != s2.cpu_fisico"
query = query + "    or  s1.prodesador_fisico != s2.prodesador_fisico"
query = query + "    or  s1.cores_fisico != s2.cores_fisico)  order by s1.hostname;"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        servidor = registro[0]
        s1 = registro[1]
        s2 = registro[2]
        print "El servidor %s esta declarado en las lineas %s, %s de forma contradictoria" % (servidor, s1, s2)
except:
    print "ERROR 15: Comprobamos que un mismo servidor que aparece en mas de una linea esta definido de la misma forma"



# COMPROBACIONES DE BBDD
# Ahora procedemos a revisar las BBDD

print "====================================================================="
print "====================================================================="
print "                          REVISIÓN DE BBDD"
print "====================================================================="

print "====================================================================="
print "BD_0: comprobamos que no hay bbdd con el mismo nombre"
print "====================================================================="

print "====================================================================="
print "BD_1: Comprobamos que las bases de datos han declarado servidores correctos."
print "====================================================================="

# BD_1: Comprobamos que las bases de datos han declarado servidores correctos.
query = "select id"
query = query + "  from basedatos"
query = query + " where servidor not in ((select hostname nombre"
query = query + "          from servidores "
query = query + "         where virtualizacion = 'No virtualizado'"
query = query + "         union all"
query = query + "        select hostname_virtual nombre"
query = query + "         from servidores "
query = query + "        where virtualizacion = 'Virtualización física'"
query = query + "           or virtualizacion = 'Virtualización lógica'));"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        basedatos = registro[0]
        if servidor:
            print "La base de datos %s no tiene un servidor correcto" % basedatos
except:
    print "Error (BD_1): Comprobamos que las bases de datos han declarado servidores correctos."


# BD_1.1: Contamos que no se haya declado 2 veces el mismo entorno.
query = "select nombre_sid, entorno, count(id) from basedatos group by nombre_sid, entorno;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    resultados = cursor.fetchall()
    for registro in resultados:
        if registro[2] > 1:
            bbdd = registro[0];
            print "* La instancia %s, " %bbdd
            intermedio = unicode(registro[1])
            entorno = intermedio.encode('utf-8')
            print "%s " %entorno
            cantidad = int(registro[2])
            print "se repite %i veces" %cantidad
except Exception as e:
    print "Error (BD_1.1): Comprobamos que las bases de datos han declarado servidores correctos."


# BD_2: Comprobar que los modelos de BBDD, están dentro de las declaradas.
print "BD_2: Comprobar que los modelos de BBDD, están dentro de las declaradas."
print "========================================================================"
query = "select id "
query = query + " from basedatos"
query = query + " where producto_oracle not in( select valor from datos where dominio = 'BBDD versiones')"
query = query + "   or version_base is null"
query = query + "    or version_parche is null;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La Base de datos %s, no tiene bien declarado el producto" %bbdd
except:
    print "Error (bd_2): Comprobar que los modelos de BBDD, están dentro de las declaradas."


# BD_19: Comprobar que los modelos de BBDD, están dentro de las declaradas.
print "BD_19: Comprobar que los modelos de BBDD, están dentro de las declaradas."
print "========================================================================"
query = "select distinct concat(nombre_sid,' ',entorno), nombre_sid, count(id)"
query = query + "  from basedatos"
query = query + " group by concat(nombre_sid,' ',entorno), nombre_sid;"



try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bd = unicode(registro[0])
        bbdd2 = bd.encode('utf-8')
        repetido = int(registro[2])
        if repetido > 1:
            print "La Base de datos %s, tiene el nombre repetido" %bbdd2
except:
    print "Error (bd_19): Comprobar que los modelos de BBDD, están dentro de las declaradas."



# BD_3: Comprobar que todos los campos obligatorios están cumplimentados
print "BD_3: Comprobar que todos los campos obligatorios estan cumplimentados"
print "========================================================================"

query = "select id"
query = query + "  from basedatos"
query = query + " where id is null"
query = query + "    or nombre_sid is null"
query = query + "    or servidor is null"
query = query + "    or producto_oracle is null"
query = query + "    or entorno is null"
query = query + "    or alta_disponibilidad is null"
query = query + "    or activo_pasivo is null"
query = query + "    or partitioning is null"
query = query + "    or criticidad is null"
query = query + "    or disponibilidad is null;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La Base de datos %s, tiene campos obligatorios en blanco" %bbdd
except:
    print "Error (BD_3): Comprobar que todos los campos obligatorios estan cumplimentados"

print "========================================================================"


query = "select id "
query = query + "from basedatos "
query = query + "where (version_base is null or version_base ='')"
query = query + "or (version_parche is null or version_parche='');"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La Base de datos %s, no tiene la vesion o el parche" %bbdd
except:
    print "Error (BD_3.2): Comprobar que todos los campos obligatorios estan cumplimentados"






# BD_4: Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --
print "BD_4: Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --"
print "========================================================================"

query = "select ID"
query = query +"  from basedatos"
query = query +" where producto_oracle = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query +"    or alta_disponibilidad = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query +"    or metodo_respaldo = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query +"    or backup = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query +"    or consola_administracion = '-- NO ENCUENTRO MI OPCIÓN --';"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La Base de datos %s, tiene valoes a -- NO ENCUENTRO MI OPCION --" %bbdd
except:
    print "Error (BD_4): Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCION --"


# BD_5: Comprobar que existe, al menos PRODUCCIÓN, PREPRODUCCIÓN, DESARROLLO
print "BD_5: Comprobar que existe, al menos PRODUCCIÓN, PREPRODUCCIÓN, DESARROLLO"
print "========================================================================"

query = "select  distinct(entorno) from basedatos;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Los entornos declarados son"
    for registro in resultados:
        bbdd = unicode(registro[0])
        bbdd1 = bbdd.encode('utf-8')
        print "* %s" %bbdd1
except:
    print "Error (BD_5): Comprobar que existe, al menos PRODUCCIÓN, PREPRODUCCIÓN, DESARROLLO"

# BD_6: Comprobar que coinciden las Criticidad y la Disponibilidad.
print "BD_6: Comprobar que coinciden las Criticidad y la Disponibilidad."
print "========================================================================"

query = "select  distinct(concat(criticidad,'' '', disponibilidad)) from basedatos order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de Criticidad y la Disponibilidad son: "
    for registro in resultados:
        bbdd = registro[0]
        print "* %s" %bbdd
except:
    print "Error (BD_6): Comprobar que coinciden las Criticidad y la Disponibilidad."

# BD_7: Comprobar posibles incoherenicas entre la Criticidad y Entorno
print "BD_7: Comprobar posibles incoherenicas entre la Criticidad y Entorno"
print "========================================================================"

query = "select  distinct(concat(entorno, ' ', criticidad)) from basedatos order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de entorno y la criticidad son: "
    for registro in resultados:
        bbdd = unicode(registro[0])
        bbdd1 = bbdd.encode('utf-8')
        print "* %s" %bbdd1
except:
    print "Error (BD_7): Comprobar posibles incoherenicas entre la Criticidad y Entorno."

# BD_7.1: Comprobar posibles incoherenicas entre la Criticidad, Entorno y disponibilidad
print "BD_7.1: Comprobar posibles incoherenicas entre la Criticidad, Entorno y disponibilidad"
print "========================================================================"

query = "select  distinct(concat(entorno, ' ', criticidad,' ' ,disponibilidad)) from basedatos order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de entorno y la criticidad son: "
    for registro in resultados:
        bbdd = unicode(registro[0])
        bbdd1 = bbdd.encode('utf-8')
        print "* %s" %bbdd1
except:
    print "Error (WL_7.1): Comprobar posibles incoherenicas entre la Criticidad, Entorno y disponibilidad."


# BD_9: Comprobar la relación entre Tipo de Nodo y el Activo/Pasivo
print "# BD_9: Comprobar la relación entre Tipo de Nodo y el Activo/Pasivo"
print "========================================================================"

query = "select id from basedatos where tipo_nodo = 'Primario' and activo_pasivo = 'Pasivo';"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, se ha declado como Pasiva" %bbdd
except:
    print "Error (BD_9): Comprobar la relación entre Tipo de Nodo y el Activo/Pasivo"


# BD_10: BBDD primarias sin tener declarado una secundaria. Si la secundaria está en centro de respaldo no es necesario
print "# BD_10: BBDD primarias sin tener declarado una secundaria. Si la secundaria esta en centro de respaldo no es necesario"
print "========================================================================"

query = "select id from basedatos  where tipo_nodo = 'Primario' and bd_relacionadas is null and alta_disponibilidad <> 'RAC (Activo-Activo)';"
print "paso 1) Comprobar que toda primaria tiene declarada una secundaria"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, es primaria y no tiene referenica a secundarias" %bbdd
except:
    print "ERROR (BD_10): BBDD primarias sin tener declarado una secundaria. Si la secundaria esta en centro de respaldo no es necesario"


query = "select id, bd_relacionadas from basedatos where tipo_nodo = 'Primario' "
query = query +"   and bd_relacionadas not in (select nombre_sid from basedatos where tipo_nodo like 'Secundario%')"
query = query +" and bd_relacionadas is not null;"

print "paso 2) Comprobar que toda primaria que tiene el campo de secundaria "
print "        apunta a una secundaria correcta"
try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        bd_relacionadas = registro[1]
        print "La BBDD " + bbdd +", es primaria pero no se encuentra la BBDD " + bd_relacionadas
except:
    print "ERROR2 (BD_10): BBDD primarias sin tener declarado una secundaria. Si la secundaria esta en centro de respaldo no es necesario"

# BD_11: BBDD secundarias que no tienen definida una primaria.
print "# BD_11: BBDD secundarias que no tienen definida una primaria."
print "========================================================================"

query = "select id"
query = query +"  from basedatos"
query = query +" where tipo_nodo like 'Secundario%'"
query = query +"   and nombre_sid not in (select b1.nombre_sid"
query = query +"                            from basedatos b1"
query = query +"                            , (select GROUP_CONCAT(bd_relacionadas SEPARATOR ',') as nombre_basedatos "
query = query +"                                 FROM basedatos where tipo_nodo = 'Primario') b2"
query = query +"                                where b2.nombre_basedatos like CONCAT('%',b1.nombre_sid,'%')"
query = query +"                                  and tipo_nodo like 'Secundario%');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, es secundaria y no se corresponde con una primaria" %bbdd
except:
    print "ERROR (BD_11): BBDD secundarias que no tienen definida una primaria."



# BD_12: Comprobaciones del RAC
print "# BD_13: Comprobar que hay cluste"
print "========================================================================"

query = "select count(id)"
query = query + "  from basedatos"
query = query + " where alta_disponibilidad like 'RAC%';"

query1 = "select count(id)"
query1 = query1 + "  from servidores"
query1 = query1 + " where arquitectura = 'Cluster';"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    if resultados > 0:
        # Ejecutamos el comando
        cursor.execute(query)
        #Comprobamos los campos virtualizados
        resultados = cursor.fetchall()
        if resultados == 0:
            print "Se han declarado RAC sin Cluster"
except:
    print "ERROR (BD_13): Comprobar que hay cluste"

# BD_15: Comprobar si el RAC es activo-activo, que todos los "Tipo de nodo" son PRIMARIOS
print "# BD_15.A: Comprobar si el RAC es activo-activo, que todos los ''Tipo de nodo'' son PRIMARIOS"
print "========================================================================"

query = "SELECT id FROM basedatos WHERE alta_disponibilidad = 'RAC (Activo-Activo)' AND activo_pasivo = 'Pasivo';"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, no puede ser pasiva, forma parte de un rac (act-act)" %bbdd
except:
    print "ERROR (BD_15.A): Comprobar si el RAC es activo-activo, que todos los ''Tipo de nodo'' son PRIMARIOS"

#
#print "# BD_15.B: Comprobar si el RAC es activo-activo, que todos los ''Tipo de nodo'' son PRIMARIOS"
#print "========================================================================"
#
#query = "SELECT id FROM basedatos WHERE alta_disponibilidad = 'RAC (Activo-Activo)' AND (tipo_nodo <> 'Primario' OR tipo_nodo <> 'Secundario/RAC');"
#
#try:
#    # Ejecutamos el comando
#    cursor.execute(query)
#    #Comprobamos los campos virtualizados
#    resultados = cursor.fetchall()
#
#    for registro in resultados:
#        bbdd = registro[0]
#        print "La BBDD %s, no puede ser distinto de primaria, forma parte de un rac (act-act)" %bbdd
#except:
#    print "ERROR (BD_15.B): Comprobar si el RAC es activo-activo, que todos los ''Primario'' son PRIMARIOS"
#

# BD_17: Comprobar que el RAC está montado en las máquinas del cluster
print "# BD_17: Comprobar que el RAC esta montado en las máquinas del cluster"
print "========================================================================"

query = "select id"
query = query + "  from basedatos"
query = query + " where alta_disponibilidad like 'RAC%'"
query = query + "   and servidor not in (select hostname"
query = query + "                          from servidores"
query = query + "                         where arquitectura = 'Cluster')"
query = query + "   and servidor not in (select hostname_virtual"
query = query + "                          from servidores"
query = query + "                         where arquitectura = 'Cluster');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, estan en RAC, pero el servidor no forma parte de un Cluster" %bbdd
except:
    print "ERROR (BD_17): Comprobar que el RAC esta montado en las máquinas del cluster"


# BD_18: Comprobamos que la consola está bien declarada
print "# BD_18: Comprobamos que la consola está bien declarada"
print "========================================================================"

query = "select id from basedatos where consola_administracion not in (select valor from datos where dominio like 'Consola de Administraci_n') "

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, tiene mal declarada la consolo de administracion" %bbdd
except:
    print "ERROR (BD_18): Consola de administracion"
    print query

# BD_19: Comprobamos que el método de respaldo
print "# BD_19: Comprobamos que el metodo de respaldo"
print "========================================================================"

query = "select * "
query = query + "from basedatos "
query = query +"where metodo_respaldo not in (select valor from datos where dominio like 'M_todo de respaldo') "
query = query +"or  metodo_respaldo is null;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Las BBDDs "
            imprimir = 1
        bbdd = registro[0]
        print " %s," %bbdd
    if imprimir == 1:
        print " tiene mal declarada el metodo de respaldo (o está puesto a NULL) ¿Es correcto?"
        imprimir = 0
except:
    print "ERROR (BD_19): Metodo de respaldo"
    print query


query = "select nombre_sid from basedatos where entorno = 'PRODUCCIÓN' and (metodo_respaldo is null or  metodo_respaldo = 'Sin Respaldo');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Las BBDD "
        bbdd = registro[0]
        print "%s, " %bbdd
        imprimir = 1
    if imprimir == 1:
        print "son de produccion y no tiene declarado un metodo de respaldo. ¿Es correcto?"
        imprimir = 0
except:
    print "ERROR (BD_19): Metodo de respaldo"
    print query



# BD_20: Comprobamos que el método de respaldo
print "# BD_20: Comprobamos los Fail-Over, tiene que haber un activo y un pasivo"
print "========================================================================"

query = "select id "
query = query + "  from basedatos"
query = query + "   where alta_disponibilidad like 'Failover Activo-Pasivo%'"
query = query + "     and activo_pasivo = 'Pasivo'"
query = query + "     and nombre_sid not in (select bd_relacionadas"
query = query + "                              from basedatos"
query = query + "                             where alta_disponibilidad like 'Failover Activo-Pasivo%'"
query = query + "                             and activo_pasivo = 'Activo');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Las BBDDs"
        bbdd = registro[0]
        print " %s," %bbdd
        imprimir = 1
    if imprimir == 1:
        print " es secundaria pero no esta relacionada ¿Es correcto?"
except:
    print "ERROR (BD_20): Fial-Over"
    print query

# BD_20: Comprobamos que el método de respaldo
print "# BD_21: Comprobamos los Fail-Over, que el activo es el primario"
print "========================================================================"

query = "select id "
query = query + "   from basedatos"
query = query + " where alta_disponibilidad like 'Failover Activo-Pasivo%'"
query = query + "  and activo_pasivo = 'Activo'"
query = query + "  and tipo_nodo <> 'Primario' and tipo_nodo <> 'Standalone';"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Las BBDDs "
        bbdd = registro[0]
        print " %s," %bbdd
        imprimir = 1
    if imprimir == 1:
        print "es Activo y no es el primario"
        imprimir = 0
except:
    print "ERROR (BD_21): Fial-Over"
    print query

# BD_20: Comprobamos que el método de respaldo
print "# BD_22: Comprobamos los Fail-Over, que el activo es el primario"
print "========================================================================"

query = "select id "
query = query + "   from basedatos"
query = query + " where alta_disponibilidad like 'Failover Activo-Pasivo%'"
query = query + "  and activo_pasivo = 'Pasivo'"
query = query + "  and tipo_nodo  in ('Primario','Standalone');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        bbdd = registro[0]
        print "La BBDD %s, es Pasiva y es el primaria" %bbdd
except:
    print "ERROR (BD_22): Fial-Over"
    print query



# BD_22: Comprobamos los entornos
print "# BD_22: Comprobamos los entornos"
print "========================================================================"
#print "Por base de datas"
#query = "select bd1.nombre_sid, concat('\t\t', bd1.entorno), count(*) from basedatos bd1 group by nombre_sid, entorno;"
#try:
    #print "BBDD        Entorno"
    #print "__________________________________________________________________"
    ## Ejecutamos el comando
    #cursor.execute(query)
    #bbddprint = ""
    ##Comprobamos los campos virtualizados
    #resultados = cursor.fetchall()

    #for registro in resultados:
        #bbdd = registro[0]
        #entorno1 = unicode(registro[1])
        #entorno = entorno1.encode('utf-8')
        #if bbdd <> bbddprint:
            #bbddprint = bbdd
            #print "%s" %bbddprint
            #print "        %s" %entorno
        #else:
            #print "        %s" %entorno


#except:
    #print "BD_22: Comprobamos los entornos"
    #print query

#print "Por aplicaciones -------------------------"
query = "select bd1.nombre_ser_ti, concat('\t\t', bd1.entorno), count(*) from basedatos bd1 where  bd1.nombre_ser_ti is not null group by nombre_ser_ti, entorno;"
try:
    print "BBDD        Entorno"
    print "__________________________________________________________________"
    # Ejecutamos el comando
    cursor.execute(query)
    bbddprint = ""
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        bd = unicode(registro[0])
        bbdd = bd.encode('utf-8')
        entorno1 = unicode(registro[1])
        entorno = entorno1.encode('utf-8')
        if bbdd <> bbddprint:
            bbddprint = bbdd
            print "%s" %bbddprint
            print "        %s" %entorno
        else:
            print "        %s" %entorno
except:
    print "BD_22: Comprobamos los entornos"
    print query


print "# BD_23: Comrpobamos los nombre de los servicios TI"
print "========================================================================"

query = "select nombre_sid from basedatos where nombre_ser_ti is null;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        if imprimir == 0:
            print "Las BBDDs "
            imprimir = 1
        bbdd = registro[0]
        print " %s," %bbdd
    if imprimir == 1:
        print  " no tienen declarados el nombre del servicio TI"

except:
    print "ERROR (BD_23): Nombre del Servicio TI"
    print query


print "# BD_24: Comprobamos que las BBDD que estan sobre Standalone no se hayan montado sobre servidores con HD"
print "========================================================================"

query = "select distinct s2.nombre_cluster, ser.hostname"
query = query + "  from basedatos"
query = query + "     , servidores s2"
query = query + "     , (select distinct hostname"
query = query + "          from servidores ser"
query = query + "         where nombre_cluster is not null"
query = query + "           and virtualizacion = 'No virtualizado'"
query = query + "         Union all    "
query = query + "         select distinct hostname_virtual"
query = query + "           from servidores ser"
query = query + "          where nombre_cluster is not null"
query = query + "          and virtualizacion <> 'No virtualizado') ser"
query = query + " where tipo_nodo = 'Standalone'"
query = query + "   and ser.hostname = servidor"
query = query + "   and (ser.hostname = s2.hostname OR ser.hostname = s2.hostname_virtual)"
query = query + "order by s2.nombre_cluster, hostname;"


try:
    imprimir = 2
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    cluster2 = ""

    for registro in resultados:
        servidor = registro[1]
        cluster = registro[0]
        if imprimir == 2:
            # Sólo la primera vez que entramos
            cluster2 = cluster
            imprimir = 0
        if cluster <> cluster2:
            print "(cluster %s)" %cluster2
            print " Sin embargo, en la pestaña '"'Oracle Database'"' las "
            print " instancias de BBDD que corren en cada uno de estos servidores aparecen "
            print "como '"'Singleinstance'"', es decir no existe alta disponibilidad"
            print " de tipo failover entre los servidores del cluster. ¿Es correcto?"
            imprimir = 0
            cluster2 = cluster
        if imprimir == 0:
            print "* En la pestaña servidores, se ha indicado que los siguientes servidores están configurados en cluster: "
            imprimir = 1
        print " %s," %servidor

    if imprimir == 1:
        print "(cluster %s)" %cluster2
        print " Sin embargo, en la pestaña '"'Oracle Database'"' las "
        print " instancias de BBDD que corren en cada uno de estos servidores aparecen "
        print "como '"'Singleinstance'"', es decir no existe alta disponibilidad"
        print " de tipo failover entre los servidores del cluster. ¿Es correcto?"

except:
    print "ERROR (BD_24): Comprobamos que las BBDD que estan sobre Standalone no se hayan montado sobre servidores con HD"
    print query




print "# BD_25: Comprobamos que BBDD primaria y secundaria tengan el mismo producto"
print "========================================================================"

query = "select prim.nombre_sid, prim.producto_oracle, secu.nombre_sid, secu.producto_oracle"
query = query + "  from basedatos prim"
query = query + "     , basedatos secu"
query = query + " where prim.tipo_nodo = 'Primario'"
query = query + "   and secu.tipo_nodo like 'Secundari%'"
query = query + "   and secu.nombre_sid = prim.bd_relacionadas"
query = query + "   and secu.producto_oracle <> prim.producto_oracle;"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        basedatosprimario = registro[0]
        productoprimario = registro[1]
        productosecundario = registro[3]
        print "* La instancia %s aparece con version %s mientras su nodo secundario aparece como %s" %(basedatosprimario, productoprimario, productosecundario)
except:
    print "ERROR (BD_25): Comprobamos que BBDD primaria y secundaria tengan el mismo producto"
    print query


print ""
print ""
print "====================================================================="
print "                          REVISION DE Servidores"
print "====================================================================="

# OW1: Comprobar que los servidores en los que se montan las OWeblogic están declarados como Servidores
print "# OW1: Comprobar que los servidores en los que se montan las OWeblogic están declarados como Servidores"
print "========================================================================"

query = "select id"
query = query + "  from weblogic"
query = query + " where servidor not in (select distinct hostname nombre"
query = query + "           from servidores"
query = query + "          where virtualizacion = 'No virtualizado'"
query = query + "          union all"
query = query + "          select distinct hostname_virtual nombre"
query = query + "            from servidores"
query = query + "           where virtualizacion = 'Virtualización física'"
query = query + "              or virtualizacion = 'Virtualización lógica');"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, no tiene un servidor correcto" %ow
except:
    print "ERROR (OW1): Comprobar que los servidores en los que se montan las OWeblogic están declarados como Servidores"


print "# OW2: Comprobar que las Columnas E, F y G están cumplimentadas."
print "========================================================================"
query = "select id"
query = query + "  from weblogic"
query = query + " where producto is null"
query = query + "    or version_base is null"
query = query + "    or version_parche is null"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, no tiene el producto, la version base o la version parche cumplimentada" %ow
except:
    print "ERROR (OW2): Comprobar que las Columnas E, F y G están cumplimentadas."


print "# OW3: Comprobar que las Columnas M y N están cumplimentadas."
print "========================================================================"
query = "select id"
query = query + "    from weblogic"
query = query + " where forms_report <> 'NO INSTALADO'"
query = query + "   and forms_report <> '-- NO ENCUENTRO MI OPCIÓN --'"
query = query + "   and ((fr_version_base is null or fr_version_base ='')"
query = query + "     or (fr_version_parche is null or fr_version_parche =''));"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, no tiene cumplimentada las columnas M y N" %ow
except:
    print "ERROR (OW3): Comprobar que las Columnas M y N están cumplimentadas."


print "# OW4: Comprobar que todos los campos obligatorios están cumplimentados"
print "========================================================================"
query = "select id"
query = query + "  from weblogic"
query = query + " where (servidor is null or servidor = '')"
query = query + "    or (producto_version is null or producto_version = '')"
query = query + "    or (producto is null or producto = '')"
query = query + "    or (version_base is null or version_base = '')"
query = query + "    or (version_parche is null or version_parche = '')"
query = query + "    or (entorno is null or entorno = '')"
query = query + "    or (activo_pasivo is null or activo_pasivo = '')"
query = query + "    or (forms_report is null or forms_report = '')"
query = query + "    or (criticidad is null or criticidad = '')"
query = query + "    or (disponibilidad is null or disponibilidad = '');"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, tiene campos obligatorios sin cumplimentar" %ow
except:
    print "ERROR (OW4): Comprobar que todos los campos obligatorios están cumplimentados"



print "========================================================================"
query = "select id"
query = query + "  from weblogic"
query = query + " where (producto is null or producto = '')"
query = query + "    or (version_base is null or version_base = '')"
query = query + "    or (version_parche is null or version_parche = '');"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, tiene los campos ocultos sin valor" %ow
except:
    print "ERROR (OW4): Comprobar que todos los campos obligatorios están cumplimentados"


print "# OW5: Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --"
print "========================================================================"
query = "select id"
query = query + "    from weblogic"
query = query + " where producto_version = '-- NO ENCUENTRO MI OPCIÓN --'"
query = query + "    or forms_report = '-- NO ENCUENTRO MI OPCIÓN --';"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El Weblogic %s, tiene -- NO ENCUENTRO MI OPCION --" %ow
except:
    print "ERROR (OW5): Comprobar los campos en los que aparece -- NO ENCUENTRO MI OPCIÓN --"


print "# OW6: Comprobamos que la versión de servidor está indicada por oracle"
print "========================================================================"
query = "select id from weblogic where producto_version not in (select valor from datos where dominio = 'Servidores Versiones');"


try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        ow = registro[0]
        print "El servidro Weblogic %s, tiene un producto desconocido" %ow
except:
    print "ERROR (OW6): Comprobamos que la versión de servidor está indicada por oracle"


# BD_6: Comprobar que coinciden las Criticidad y la Disponibilidad.
print "# wl_7: Comprobar que coinciden las Criticidad y la Disponibilidad."
print "========================================================================"

query = "select  distinct(concat(criticidad,'' '', disponibilidad)) from weblogic order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de Criticidad y la Disponibilidad son: "
    for registro in resultados:
        bbdd = registro[0]
        print "* %s" %bbdd
except:
    print "Error (WL_7): Comprobar que coinciden las Criticidad y la Disponibilidad."

# WL_8: Comprobar posibles incoherenicas entre la Criticidad y Entorno
print "#WL_8: Comprobar posibles incoherenicas entre la Criticidad y Entorno"
print "========================================================================"

query = "select  distinct(concat(entorno, ' ', criticidad)) from weblogic order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de entorno y la criticidad son: "
    for registro in resultados:
        bbdd = unicode(registro[0])
        bbdd1 = bbdd.encode('utf-8')
        print "* %s" %bbdd1
except:
    print "Error (WL_8): Comprobar posibles incoherenicas entre la Criticidad y Entorno."


# WL_9: Comprobar posibles incoherenicas entre la Criticidad, Entorno y disponibilidad
print "#WL_9: Comprobar posibles incoherenicas entre la Criticidad y Entorno"
print "========================================================================"

query = "select  distinct(concat(entorno, ' ', criticidad,' ' ,disponibilidad)) from weblogic order by 1;"

try:
    # Ejecutamos el comando
    cursor.execute(query)
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()
    print "Las duplas de entorno y la criticidad son: "
    for registro in resultados:
        bbdd = unicode(registro[0])
        bbdd1 = bbdd.encode('utf-8')
        print "* %s" %bbdd1
except:
    print "Error (WL_9): Comprobar posibles incoherenicas entre la Criticidad y Entorno."


# WL_22: Comprobamos los entornos
print "# WL_22: Comprobamos los entornos"
print "========================================================================"

query = "select  serv_ti, concat('\t\t', entorno), count(*) from weblogic group by serv_ti desc, entorno ;"
try:
    print "SVWL        Entorno"
    print "__________________________________________________________________"
    # Ejecutamos el comando
    cursor.execute(query)
    svprint = ""
    #Comprobamos los campos virtualizados
    resultados = cursor.fetchall()

    for registro in resultados:
        sv1 = registro[0]
        sv = sv1.encode('utf-8')
        entornosv1 = unicode(registro[1])
        entornosv = entornosv1.encode('utf-8')
        if sv <> svprint:
            svprint = sv
            print "%s" %svprint
            print "%s" %entornosv
        else:
            print "%s" %entornosv

except:
    print "BD_22: ERROR Comprobamos los entornos"
    print query



conn.close()
