import jinja2
import pdfkit
import random
import datetime

def certificado(nombres,apellidos,tipo_documento,nro_documento,direccion,lugar_muestra,tipo_muestra,fecha_obtencion,fecha_resultado,analisis,metodo,resultado,valores,rango):
    num_chars=10
    chars = "0123456789"
    fecha = datetime.datetime.now()
    fecha_actual = fecha.strftime("%c")
    for i in range(0, num_chars):
        numero_ale = str(random.randint(0, len(chars)))
    infor_resultado="IFR-"+ numero_ale
    name_paciente = nombres + " " + apellidos
    context = {'ifr_resultado':infor_resultado,'name_paciente':name_paciente,'tipodoc_paciente':tipo_documento,'nrodoc_paciente':nro_documento,'direccion_paciente':direccion,'lugar_prueba':lugar_muestra,'tipo_muestra':tipo_muestra,'fecha_muestra':fecha_obtencion,'fecha_resultado':fecha_resultado,'analisis_prueba':analisis,'metodo_prueba':metodo,'resultados_prueba':resultado,'decision_clinica':valores,'rango_referencia':rango,'fecha_actual':fecha_actual}
    template_loader =jinja2.FileSystemLoader('./')
    template_env = jinja2.Environment(loader=template_loader)
    
    html_template = "src/templates/certificado.html"
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config =pdfkit.configuration(wkhtmltopdf='C://Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_pdf = f'src/static/Resultado.pdf'
    pdfkit.from_string(output_text,output_pdf,configuration=config,css="src/static/css/certificado.css")

    
