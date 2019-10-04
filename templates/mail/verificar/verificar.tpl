{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hola {{ first_name }}, bienvenido a OP+
{% endblock %}


{% block html %}
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Demystifying Email Design</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin: 0; padding: 0;">
	<table border="0" cellpadding="0" cellspacing="0" width="100%">
		<tr>
			<td style="padding: 10px 0 30px 0;">
				<table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc; border-collapse: collapse;">
					<tr>
						<td align="center" bgcolor="#025930" style="padding: 50px; color: #fff; font-size: 100px; font-weight: bold; font-family: Arial, sans-serif;">
							<img src="{{ url_base }}/static/img/op.png" alt="OP+" height="100" style="display: block;" />
						</td>
					</tr>
					<tr>
						<td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
							<table border="0" cellpadding="0" cellspacing="0" width="100%">
								<tr>
									<td style="color: #153643; font-family: Arial, sans-serif; font-size: 24px;">
										<b>Hola {{ first_name }}:</b>
									</td>
								</tr>
								<tr>
									<td style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
										Has creado una cuenta en el sistema de información OP+ usando este correo electrónico,
                                        a continuación encuentras los datos de acceso y el vinculo para verificar tu cuenta.
									</td>
								</tr>
								<tr>
									<td>
										<table border="0" cellpadding="0" cellspacing="0" width="100%">
											<tr>
												<td width="240" valign="top">
													<table border="0" cellpadding="0" cellspacing="0" width="100%">
														<tr>
															<td>
																<img src="{{ url_base }}/static/img/new_user.jpg" alt="" width="100%" height="240" style="display: block;" />
															</td>
														</tr>
													</table>
												</td>
												<td style="font-size: 0; line-height: 0;" width="20">
													&nbsp;
												</td>
												<td width="280" valign="top">
													<table border="0" cellpadding="0" cellspacing="0" width="100%">

														<tr>
															<td style="padding: 25px 0 0 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
																<p>Url: <b><a href="http://opmas.co/">http://opmas.co/</a></b></p>
                                                                <p>Email: <b>{{ email }}</b></p>
                                                                <p>Contraseña: <b>{{ password }}</b></p>
                                                                <table class="buttonwrapper" bgcolor="#025930" border="0" cellspacing="0" cellpadding="0">
                                                                    <tr>
                                                                      <td width="240" class="button" height="45" style="text-align: center; font-size: 16px; font-family: sans-serif; font-weight: bold; padding: 0 30px 0 30px;background:#025930;">
                                                                        <a href="{{ url_base }}/verificar?email={{email}}&code={{code}}" style="color: #ffffff; text-decoration: none;">Verificar cuenta</a>
                                                                      </td>
                                                                    </tr>
                                                                </table>
															</td>
														</tr>
													</table>
												</td>
											</tr>
                                        </table>

                                        <table>
                                            <tr>
                                                <td valign="top">
													<table border="0" cellpadding="0" cellspacing="0" width="100%">
														<tr>
															<td style="padding: 0px 0 0 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
																Conoce las <a href="{{ url_base }}/privacidad/" style="display:inline">politicas de privacidad</a> de tu información, si no creaste
                                                                la cuenta por favor elimina este correo.
															</td>
														</tr>
													</table>
												</td>
                                            </tr>
                                        </table>
									</td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<td bgcolor="#025930" style="padding: 30px 30px 30px 30px;">
							<table border="0" cellpadding="0" cellspacing="0" width="100%">
								<tr>
									<td style="color: #ffffff; font-family: Arial, sans-serif; font-size: 14px;" width="75%">
										&copy; 2019
									</td>
								</tr>
							</table>
						</td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
</body>
</html>
{% endblock %}