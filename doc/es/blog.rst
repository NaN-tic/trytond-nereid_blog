====
Blog
====

Gestión de nuestros posts para blogs o notícias clasificados por categorías o por tags.

Categorias
==========

En |menu_blog_category| crearemos nuestras categorías de nuestro blog. Estas categorías
son un poco la estructura de las URL's de nuestros posts.

El campo |cat_uri| es el campo identificador de nuestra categoría. El nombre del campo
|cat_uri| debe ser único.

Los posts por categorías se puede personalizar la plantilla en que se muestra. De esta forma,
los posts de la categoría *Tecnología* pueden contener una estética de listado diferente
que los posts de otra categoría. Por defecto el nombre de la plantilla es **blog-category.jinja**.
Consulte con su técnico para saber que otras plantillas dispone en vuestra web. Es importante
que la plantilla exista en nuestra web ya que si no obtendremos un error al no poder
encontrarla.

Todos los pots por categoría los podemos consultar en la URL:

 * http://domain.com/es/blog/URI

.. |menu_blog_category| tryref:: nereid_blog.menu_blog_category_form/complete_name
.. |cat_uri| field:: nereid.blog.category/uri

Posts
=====

En |menu_blog_post| crearemos nuestras posts. Igual que en las categorías disponemos
del campo |post_uri| que es el identificador de nuestro post y debe ser único.

Los posts los podemos relacionar con varias categorías. Por cada categoría se mostrará
el post.

.. |menu_blog_post| tryref:: nereid_blog.menu_blog_post_form/complete_name
.. |post_uri| field:: nereid.blog.post/uri

Aunque no son requeridos los campos Metakeywords, MetaDescription y MetaTitle se
recomienda su personalización para SEO. el campo MetaDescription se usa para las
descripciones de los buscadores y recomiendan que sean únicas -no haya más de dos
páginas con la misma descripción-. En el caso de no añadir el campo MetaDescription,
se usará el nombre del post como descripción del post para los buscadores.

El post se puede personalizar la plantilla en que se muestra. Por defecto el nombre
de la plantilla es **blog-post.jinja**. Consulte con su diseñador gráfico para saber que otras 
lantillas dispone en vuestra web. Es importante que la plantilla exista en nuestra
web ya que si no obtendremos un error al no poder encontrarla.

Para acceder a un post podemos consultar en la URL:

 * http://domain.com/es/blog/post/URI

Para la generación de tags, se generan a partir de las palabras clave (MetaKeywords).
Las palabras clave se separan mediante la coma ",". A partir de estas palabras, se generan
vínculos para filtrar otros posts con las mismas palabras clave.

Formato HTML
============

Para dar contenido gráfico a la descripción del post, podemos usar tags wiki para dar formato.
Dispone de ejemplos como usar estos tags en `Wiki Editor`_

.. _Wiki Editor: http://doc.zikzakmedia.com/Django/WikiEditor

Añadiendo estos tags en su contenido le permite:

* Publicaremos páginas HTML con código limpio.
* Evitaremos transformaciones de código HTML debido al copiar-pegar desde documentos de ofimática
* Crearás contenidos enrequecidos de contenido, sin preocuparte de la forma. 

Imagenes
========

Los posts podemos relacionar con varias imagenes de nuestro ERP. Depende de nuestro
diseño de plantilla, estas imagenes se visualizarán con un tipo de galería o otro.
