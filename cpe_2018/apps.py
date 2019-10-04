from django.apps import AppConfig


class Cpe2018Config(AppConfig):
    name = 'cpe_2018'

    def ready(self):
        self.sican_name = "Módulo Formación"
        self.sican_icon = "computer"
        self.sican_description = "Proyecto formación 2018"
        self.sican_color = "light-green darken-4"
        self.sican_url = '/cpe_2018/'
        self.sican_categoria = 'Formación'
        self.sican_order = 6
        self.sican_permiso = 'usuarios.cpe_2018.ver'
