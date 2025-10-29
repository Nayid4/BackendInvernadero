# mediator_handlers_init.py

# Importa aquí TODOS los handlers y behaviors para CQRS/mediator
import application.usuarios.commands.create_usuario.handler
import application.usuarios.commands.update_usuario.handler
import application.usuarios.commands.delete_usuario.handler

import application.usuarios.queries.get_all_usuarios.handler
import application.usuarios.queries.get_usuario_by_id.handler
import application.usuarios.queries.get_usuario_by_correo.handler
import application.usuarios.queries.login.handler

import application.plantas.commands.create_planta.handler
import application.plantas.commands.update_planta.handler
import application.plantas.commands.delete_planta.handler
import application.plantas.queries.get_all_plantas.handler
import application.plantas.queries.get_planta_by_id.handler
# Si tienes más handlers, agrégalos aquí

import application.abanico.queries.consultar_abanico.handler
import application.abanico.queries.get_historico.handler
