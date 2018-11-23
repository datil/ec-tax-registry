ec-tax-registry
==============================================

Es un servicio web de consulta de RUCs a partir del catastro de contribuyentes del Servicio de Rentas Internas.

Cómo empezar
------------

* Descarga los [Catastros del Registro Único de Contribuyentes (RUC)](http://www.sri.gob.ec/web/guest/catastros) de las provincias que requieras.

* Codifica en UTF-8 los archivos del catastro:

```shell
iconv -f iso-8859-1 -t UTF-8 NOMBRE_DEL_ARCHIVO.txt > NOMBRE_DEL_ARCHIVO-UTF-8.txt
```

* Crea un bucket S3 y coloca los archivos codificados del paso anterior.

* Crea una base de datos en Athena direccionada al repositorio del paso anterior. Revisa esta [guía](http://www.devdailyhash.com/2017/09/aws-athena-to-query-csv-files-in-s3.html).

What Should I Do Before Running My Project in Production?
------------------

AWS recommends you review the security best practices recommended by the framework
author of your selected sample application before running it in production. You
should also regularly review and apply any available patches or associated security
advisories for dependencies used within your application.

Best Practices: https://docs.aws.amazon.com/codestar/latest/userguide/best-practices.html?icmpid=docs_acs_rm_sec
