WikipediaStatistics
===================

Fase I: Popular la BD a partir de los logs mediante tareas programadas
---------------

Cada día 1, 10 y 20 de cada mes se realizan las siguiente serie de tareas:

1.  Tansferir logs de días anteriores -> <a href="https://github.com/rmajasol/WikipediaStatistics/blob/master/transfer_logs.py">transfer_logs.py</a>
2.  Ejecutar wikisquilter sobre ellos (durante 10 segundos por log para pruebas) -> <a href="https://github.com/rmajasol/WikipediaStatistics/blob/master/run_wikisquilter_10sec.py">run_wikisquilter_10sec.py</a>
3.  Popular BD de analysis -> <a href="https://github.com/rmajasol/WikipediaStatistics/blob/master/populate_analysis.py">populate_analysis.py</a>
4.  Vaciar la BD squidlogs -> <a href="https://github.com/rmajasol/WikipediaStatistics/blob/master/clear_squidlogs.py">clear_squidlogs.py</a>


Fase II: Crear una aplicación web para consultas gráficas sobre la BD
----------------
