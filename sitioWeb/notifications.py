import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

def enviar_notificacion_limite(config, total_aspirantes, ultimo_aspirante=None):
    """
    Envía una notificación por correo electrónico al administrador cuando
    se alcanza el límite máximo de aspirantes registrados en el sistema.
    """
    destinatario = config.email_notificaciones
    limite = config.limite_inscripciones
    asunto = f"[Colegio Águilas] Límite de Inscripciones Alcanzado ({total_aspirantes}/{limite})"

    detalles_ultimo = ""
    if ultimo_aspirante:
        detalles_ultimo = f"""
ÚLTIMO ASPIRANTE REGISTRADO:
- Nombre: {ultimo_aspirante.nombre}
- Correo: {ultimo_aspirante.email}
- Teléfono: {ultimo_aspirante.telefono}
- Carrera: {ultimo_aspirante.carrera}
- Promedio: {ultimo_aspirante.promedio}
"""

    cuerpo_texto = f"""Estimado Administrador,

Le informamos que el sistema del Colegio Águilas ha alcanzado el límite máximo configurado de aspirantes registrados.

RESUMEN DEL ESTADO:
- Límite configurado: {limite} personas
- Total de aspirantes registrados: {total_aspirantes}
- Estado del formulario público: BLOQUEADO AUTOMÁTICAMENTE
{detalles_ultimo}
A partir de este momento, ningún aspirante adicional podrá registrarse en la página web pública hasta que se aumente el límite de cupos desde el panel administrativo.

Para ampliar el límite de personas o gestionar las solicitudes, ingrese al Panel de Administración:
http://localhost:8000/admin-panel/?tab=configuracion

Atentamente,
Colegio Águilas - Sistema Automatizado de Admisiones
"""

    cuerpo_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8f6f2; padding: 25px; margin: 0; color: #2c2530;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0d8ce; box-shadow: 0 4px 12px rgba(0,0,0,0.06); max-width: 100%;">
            <tr>
                <td style="background-color: #220d2a; padding: 25px; text-align: center;">
                    <h1 style="color: #c9a84c; margin: 0; font-size: 24px; font-family: Georgia, serif;">Colegio Águilas</h1>
                    <span style="color: #dfd5c7; font-size: 12px; letter-spacing: 2px; text-transform: uppercase;">Notificación del Sistema de Admisiones</span>
                </td>
            </tr>
            <tr>
                <td style="padding: 30px;">
                    <div style="background-color: #fcf8e3; border: 1px solid #faebcc; border-left: 5px solid #8a6d3b; padding: 15px; border-radius: 4px; margin-bottom: 25px;">
                        <strong style="color: #8a6d3b; font-size: 16px;">Límite de Cupos Alcanzado</strong>
                        <p style="margin: 6px 0 0; color: #8a6d3b; font-size: 14px;">
                            Se ha alcanzado la cuota límite de <strong>{limite} personas registradas</strong>. El formulario público de inscripciones ha sido bloqueado automáticamente.
                        </p>
                    </div>

                    <h3 style="color: #220d2a; margin-top: 0; border-bottom: 2px solid #f0e6d6; padding-bottom: 8px;">Estado del Sistema</h3>
                    <table width="100%" style="font-size: 14px; margin-bottom: 20px; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px 0; color: #666;">Límite establecido:</td>
                            <td style="padding: 10px 0; text-align: right; font-weight: bold; color: #220d2a;">{limite} personas</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px 0; color: #666;">Total registrados en BD:</td>
                            <td style="padding: 10px 0; text-align: right; font-weight: bold; color: #c0392b;">{total_aspirantes} aspirantes</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #eee;">
                            <td style="padding: 10px 0; color: #666;">Estado de inscripciones:</td>
                            <td style="padding: 10px 0; text-align: right; font-weight: bold; color: #c0392b;">BLOQUEADO</td>
                        </tr>
                    </table>
                    """ + (f"""
                    <div style="background-color: #fdfaf6; border: 1px solid #e0d8ce; border-radius: 6px; padding: 16px; margin: 20px 0;">
                        <h4 style="margin: 0 0 10px; color: #220d2a; font-size: 14px; text-transform: uppercase;">Último aspirante registrado:</h4>
                        <table width="100%" style="font-size: 13px; color: #444;">
                            <tr><td style="padding: 4px 0; width: 120px;"><strong>Nombre:</strong></td><td>{ultimo_aspirante.nombre}</td></tr>
                            <tr><td style="padding: 4px 0;"><strong>Correo:</strong></td><td>{ultimo_aspirante.email}</td></tr>
                            <tr><td style="padding: 4px 0;"><strong>Teléfono:</strong></td><td>{ultimo_aspirante.telefono}</td></tr>
                            <tr><td style="padding: 4px 0;"><strong>Carrera:</strong></td><td>{ultimo_aspirante.carrera}</td></tr>
                            <tr><td style="padding: 4px 0;"><strong>Promedio:</strong></td><td>{ultimo_aspirante.promedio}</td></tr>
                        </table>
                    </div>
                    """ if ultimo_aspirante else "") + f"""
                    <div style="margin-top: 30px; text-align: center;">
                        <p style="font-size: 14px; color: #666; margin-bottom: 15px;">Para ampliar el cupo permitido o gestionar las inscripciones, ingresa al Panel de Administración:</p>
                        <a href="http://localhost:8000/admin-panel/?tab=configuracion" style="background-color: #220d2a; color: #c9a84c; text-decoration: none; padding: 12px 28px; border-radius: 4px; font-weight: bold; display: inline-block;">
                            Ir al Panel de Control
                        </a>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="background-color: #f8f6f2; border-top: 1px solid #e0d8ce; padding: 15px; text-align: center; font-size: 12px; color: #888;">
                    Notificación automática enviada a <strong>{destinatario}</strong> por el Sistema de Admisiones del Colegio Águilas.
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Colegio Águilas <admisiones@colegioaguilas.edu.mx>')
        send_mail(
            subject=asunto,
            message=cuerpo_texto,
            from_email=from_email,
            recipient_list=[destinatario],
            html_message=cuerpo_html,
            fail_silently=False,
        )
        logger.info(f"Correo de notificación de límite enviado exitosamente a {destinatario}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo de notificación a {destinatario}: {e}")
        # En caso de fallo con backend SMTP, intentar backend de consola para no perder la alerta
        try:
            from django.core.mail.backends.console import EmailBackend as ConsoleBackend
            from django.core.mail import EmailMultiAlternatives
            console = ConsoleBackend()
            msg = EmailMultiAlternatives(asunto, cuerpo_texto, from_email, [destinatario], connection=console)
            msg.attach_alternative(cuerpo_html, "text/html")
            msg.send()
        except Exception:
            pass
        return False
