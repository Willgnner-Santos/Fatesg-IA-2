from flask import request, jsonify, Blueprint
from app.Utils.decorators import token_required
from app.Models.notification_model import Notification
from app.Models.user_model import User
from bson.objectid import ObjectId

notification_blueprint = Blueprint("notification", __name__)
notification_model = Notification()
user_model = User()


@notification_blueprint.route("/notifications", methods=["GET"])
@token_required
def get_notifications(current_user):
    """
    Listar notificações do usuário
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: unread_only
        schema:
          type: boolean
          example: false
        description: Filtrar apenas não lidas
      - in: query
        name: limit
        schema:
          type: integer
          example: 20
        description: Número máximo de notificações
      - in: query
        name: skip
        schema:
          type: integer
          example: 0
        description: Número de notificações a pular
    responses:
      200:
        description: Lista de notificações
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            data:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: string
                    example: "507f1f77bcf86cd799439017"
                  title:
                    type: string
                    example: "Nova Mensagem"
                  message:
                    type: string
                    example: "Você recebeu uma nova mensagem do Professor Silva"
                  type:
                    type: string
                    example: "info"
                  priority:
                    type: string
                    example: "medium"
                  read:
                    type: boolean
                    example: false
                  created_at:
                    type: string
                    format: date-time
                    example: "2024-01-15T10:30:00Z"
                  action_url:
                    type: string
                    example: "/messages/123"
                  action_text:
                    type: string
                    example: "Ver Mensagem"
            unread_count:
              type: integer
              example: 5
      401:
        description: Token inválido
    """
    try:
        unread_only = request.args.get("unread_only", "false").lower() == "true"
        limit = int(request.args.get("limit", 20))
        skip = int(request.args.get("skip", 0))

        notifications = notification_model.get_user_notifications(
            str(current_user["_id"]), unread_only, limit, skip
        )

        unread_count = notification_model.get_unread_count(str(current_user["_id"]))

        processed_notifications = []
        for notif in notifications:
            processed_notifications.append(
                {
                    "_id": str(notif["_id"]),
                    "title": notif["title"],
                    "message": notif["message"],
                    "type": notif["type"],
                    "priority": notif.get("priority", "medium"),
                    "read": notif["read"],
                    "action_url": notif.get("action_url"),
                    "action_text": notif.get("action_text"),
                    "related_to": str(notif["related_to"])
                    if notif.get("related_to")
                    else None,
                    "related_type": notif.get("related_type"),
                    "created_at": notif["created_at"].isoformat(),
                    "read_at": notif.get("read_at", {}).isoformat()
                    if notif.get("read_at")
                    else None,
                }
            )

        return jsonify(
            {
                "status": "sucesso",
                "data": processed_notifications,
                "unread_count": unread_count,
                "total": len(notifications),
            }
        ), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


@notification_blueprint.route("/notifications/<notification_id>/read", methods=["PUT"])
@token_required
def mark_notification_read(current_user, notification_id):
    """
    Marcar notificação como lida
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: notification_id
        required: true
        schema:
          type: string
          example: "507f1f77bcf86cd799439017"
    responses:
      200:
        description: Notificação marcada como lida
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            message:
              type: string
              example: "Notificação marcada como lida"
      404:
        description: Notificação não encontrada
    """
    try:
        result = notification_model.mark_as_read(
            notification_id, str(current_user["_id"])
        )

        if result.modified_count == 0:
            return jsonify(
                {
                    "status": "erro",
                    "message": "Notificação não encontrada ou já está lida",
                }
            ), 404

        return jsonify(
            {"status": "sucesso", "message": "Notificação marcada como lida"}
        ), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


@notification_blueprint.route("/notifications/read-all", methods=["PUT"])
@token_required
def mark_all_notifications_read(current_user):
    """
    Marcar todas as notificações como lidas
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    responses:
      200:
        description: Todas as notificações marcadas como lidas
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            message:
              type: string
              example: "Todas as notificações marcadas como lidas"
            marked_count:
              type: integer
              example: 5
    """
    try:
        result = notification_model.mark_all_as_read(str(current_user["_id"]))

        return jsonify(
            {
                "status": "sucesso",
                "message": "Todas as notificações marcadas como lidas",
                "marked_count": result.modified_count,
            }
        ), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


@notification_blueprint.route("/notifications/<notification_id>", methods=["DELETE"])
@token_required
def delete_notification(current_user, notification_id):
    """
    Excluir uma notificação
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: notification_id
        required: true
        schema:
          type: string
          example: "507f1f77bcf86cd799439017"
    responses:
      200:
        description: Notificação excluída
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            message:
              type: string
              example: "Notificação excluída com sucesso"
      404:
        description: Notificação não encontrada
    """
    try:
        result = notification_model.delete_notification(
            notification_id, str(current_user["_id"])
        )

        if result.deleted_count == 0:
            return jsonify(
                {"status": "erro", "message": "Notificação não encontrada"}
            ), 404

        return jsonify(
            {"status": "sucesso", "message": "Notificação excluída com sucesso"}
        ), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


@notification_blueprint.route("/notifications/unread-count", methods=["GET"])
@token_required
def get_unread_count(current_user):
    """
    Obter contagem de notificações não lidas
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    responses:
      200:
        description: Contagem de notificações não lidas
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            count:
              type: integer
              example: 3
    """
    try:
        count = notification_model.get_unread_count(str(current_user["_id"]))

        return jsonify({"status": "sucesso", "count": count}), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


@notification_blueprint.route("/notifications/recent", methods=["GET"])
@token_required
def get_recent_notifications(current_user):
    """
    Obter notificações recentes (últimas 24 horas)
    ---
    tags:
      - Notificações
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: hours
        schema:
          type: integer
          example: 24
        description: Período em horas para buscar notificações
    responses:
      200:
        description: Notificações recentes
        schema:
          type: object
          properties:
            status:
              type: string
              example: "sucesso"
            data:
              type: array
              items:
                $ref: '#/definitions/Notification'
    """
    try:
        hours = int(request.args.get("hours", 24))
        notifications = notification_model.get_recent_notifications(
            str(current_user["_id"]), hours
        )

        processed_notifications = []
        for notif in notifications:
            processed_notifications.append(
                {
                    "_id": str(notif["_id"]),
                    "title": notif["title"],
                    "message": notif["message"],
                    "type": notif["type"],
                    "read": notif["read"],
                    "created_at": notif["created_at"].isoformat(),
                }
            )

        return jsonify({"status": "sucesso", "data": processed_notifications}), 200

    except Exception as e:
        return jsonify({"status": "erro", "message": str(e)}), 500


# Serviço utilitário para criar notificações automaticamente
class NotificationService:
    @staticmethod
    def notify_new_message(recipient_id, sender_name, message_preview, message_id):
        """Notificar sobre nova mensagem"""
        notification_data = {
            "title": "Nova Mensagem",
            "message": f"Você recebeu uma nova mensagem de {sender_name}: {message_preview[:50]}...",
            "type": "info",
            "user_id": recipient_id,
            "related_to": message_id,
            "related_type": "message",
            "action_url": f"/messages/{message_id}",
            "action_text": "Ver Mensagem",
            "priority": "medium",
        }
        return notification_model.create_notification(notification_data)

    @staticmethod
    def notify_new_grade(student_id, assignment_title, score, assignment_id):
        """Notificar sobre nova nota"""
        notification_data = {
            "title": "Nova Nota",
            "message": f'Sua nota na avaliação "{assignment_title}": {score}',
            "type": "info",
            "user_id": student_id,
            "related_to": assignment_id,
            "related_type": "grade",
            "action_url": f"/grades/assignments/{assignment_id}",
            "action_text": "Ver Detalhes",
            "priority": "medium",
        }
        return notification_model.create_notification(notification_data)

    @staticmethod
    def notify_upcoming_event(user_id, event_title, event_time, event_id):
        """Notificar sobre evento próximo"""
        notification_data = {
            "title": "Evento Próximo",
            "message": f'Evento "{event_title}" começa em {event_time}',
            "type": "warning",
            "user_id": user_id,
            "related_to": event_id,
            "related_type": "event",
            "action_url": f"/schedule/events/{event_id}",
            "action_text": "Ver Evento",
            "priority": "high",
        }
        return notification_model.create_notification(notification_data)

    @staticmethod
    def notify_system_announcement(user_id, title, message, priority="medium"):
        """Notificação do sistema"""
        notification_data = {
            "title": title,
            "message": message,
            "type": "system",
            "user_id": user_id,
            "priority": priority,
            "action_text": "Ver Detalhes",
        }
        return notification_model.create_notification(notification_data)
