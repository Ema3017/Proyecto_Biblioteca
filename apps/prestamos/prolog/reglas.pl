% Hechos: Límites de libros por rol
max_libros(estudiante, 3).
max_libros(docente, 5).
max_libros(bibliotecario, 10). % Para uso interno/administrativo

% Regla 1: ¿Puede pedir un préstamo?
% Se aprueba si el usuario no tiene sanciones (Sanciones = 0)
% y los libros que tiene actualmente (LibrosActivos) son menores al máximo permitido para su rol.
puede_prestar(Rol, LibrosActivos, Sanciones) :-
    Sanciones == 0,
    max_libros(Rol, Max),
    LibrosActivos < Max.

% Regla 2: Sistema de Recomendaciones (Simulado para inferencia cruzada)
% Un libro es recomendable si coincide en categoría y coincide con el grado del usuario
% (Los datos reales se cruzan en engine.py alimentando la base temporal)
es_recomendable(IdLibro, CategoriaBuscada, GradoUsuario, CategoriaLibro, GradoLibro) :-
    CategoriaLibro == CategoriaBuscada,
    (GradoLibro == GradoUsuario ; GradoLibro == general).
