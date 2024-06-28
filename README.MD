Podemos asignar soportes mediante el siguiente formulario:
![alt text](imagen1.png)

donde llenamos la informacion:
Nombre: Nombre del soporte a realizar
Descripcion: una descripcion basica de lo que hay que realizar de soporte
Prioridad: (5 Mayor prioridad, 4,3,2, 1 menor prioridad)
Peso: (1 menor peso, 2, 3, 4,5 mayor peso)


En esta tabla podemos ver el listado de trabajadores con su respectivo peso acumulado:
![alt text](imagen2.png)

-----------------------------------------------------------------------------------------------------------

CREACION DE LA BASE DE DATOS:

la base de datos tiene la siguientes credenciales:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password-@localhost/Makrosoft_Test_MVallejo'

BD: Makrosoft_Test_MVallejo
User: postgres
Password: password

-----------------------------------------------------------------------------------------------------------

crear las siguientes tablas:

CREATE TABLE public.soportes (
	id int4 NOT NULL DEFAULT nextval('soportes_id_seq'::regclass),
	nombre varchar(100) NOT NULL,
	descripcion varchar(200) NOT NULL,
	prioridad int4 NOT NULL,
	peso int4 NOT NULL,
	trabajador_asignado int4 NULL,
	CONSTRAINT soportes_pk PRIMARY KEY (id),
	CONSTRAINT soportes_trabajador_id_fk FOREIGN KEY (trabajador_asignado) REFERENCES public.trabajador(id) ON DELETE SET NULL
);

CREATE TABLE public.trabajador (
	id serial4 NOT NULL,
	nombre varchar(50) NOT NULL,
	peso_acumulado int4 NULL,
	CONSTRAINT trabajador_pkey PRIMARY KEY (id)
);

-----------------------------------------------------------------------------------------------------------

Insertamos los trabajadores a la tabla trabajador:

INSERT INTO public.trabajador (nombre,peso_acumulado) VALUES
	 (1,'Pedro',0),
	 (2,'Felipe',0),
	 (3,'Andrea',0);

-----------------------------------------------------------------------------------------------------------